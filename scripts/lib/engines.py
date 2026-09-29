#!/usr/bin/env python3
"""Xray / sing-box config builders + engine routing rules.

Engine routing (both cores are used):
  - http / socks proxies           -> direct curl (no engine needed)
  - hysteria2 / hysteria / tuic    -> sing-box (xray does not support them)
  - anything with network=h2(http) -> sing-box (xray 26.x removed plain h2 transport)
  - xhttp transport                -> xray (sing-box does not support xhttp)
  - everything else (vless/vmess/trojan/ss, tcp/ws/grpc/httpupgrade)
                                    -> xray primary, sing-box as fallback retry
"""
import copy

XRAY_PROTOS = {"vmess", "vless", "trojan", "ss", "socks", "http"}
SB_PROTOS = {"vmess", "vless", "trojan", "ss", "socks", "http", "hysteria2", "hysteria", "tuic"}
SB_NETWORKS = {"tcp", "ws", "grpc", "http", "httpupgrade"}

# Shadowsocks methods loadable by MODERN xray/sing-box (AEAD + 2022).
# Legacy ciphers (rc4-md5, *-cfb, chacha20-ietf, ...) are rejected by both
# cores at config-load time and poison whole batches, so we never test them.
# Empirically verified against xray 26.x and sing-box 1.14:
#   - both accept the *-ietf-poly1305 spellings
#   - xray also accepts the short aliases (normalized below for sing-box)
#   - 2022-blake3-* additionally require a valid base64 key of the right length
SS_MODERN_METHODS = {
    "aes-128-gcm", "aes-256-gcm",
    "chacha20-ietf-poly1305", "xchacha20-ietf-poly1305",
    "chacha20-poly1305", "xchacha20-poly1305",   # aliases -> normalized
    "2022-blake3-aes-128-gcm", "2022-blake3-aes-256-gcm",
    "2022-blake3-chacha20-poly1305",
}
SS_ALIAS = {
    "chacha20-poly1305": "chacha20-ietf-poly1305",
    "xchacha20-poly1305": "xchacha20-ietf-poly1305",
}


def _ss_method_ok(p):
    m = (p.get("method") or "").lower()
    if m not in SS_MODERN_METHODS:
        return False
    if m.startswith("2022-"):
        import base64
        need = 16 if "aes-128" in m else 32
        try:
            key = base64.b64decode(p.get("password") or "", validate=True)
            return len(key) == need
        except Exception:
            return False
    return True


def _norm_ss_method(m):
    return SS_ALIAS.get((m or "").lower(), (m or "").lower())


def primary_engine(p):
    proto = p.get("proto")
    if proto in ("http", "socks", "socks5"):
        return "direct"
    if proto in ("hysteria2", "hysteria", "tuic"):
        return "singbox"
    net = p.get("network") or "tcp"
    if net in ("http", "h2"):
        return "singbox"
    return "xray"


def engine_supports(engine, p):
    proto = p.get("proto")
    net = p.get("network") or "tcp"
    if engine == "direct":
        return proto in ("http", "socks", "socks5")
    if proto == "ss":
        if not _ss_method_ok(p):
            return False
    if engine == "xray":
        if proto not in XRAY_PROTOS:
            return False
        if net in ("http", "h2", "kcp", "quic"):
            return False
        return True
    if engine == "singbox":
        if proto in ("hysteria2", "hysteria", "tuic"):
            return True
        if proto in ("vmess", "vless", "trojan", "ss", "socks", "http"):
            return net in SB_NETWORKS
    return False


def _alpn_list(p):
    a = [x.strip().lower() for x in str(p.get("alpn") or "").split(",") if x.strip()]
    return a or None


# ----------------------------------------------------------------- xray -----

def xray_stream_settings(p):
    net = p.get("network") or "tcp"
    security = p.get("security") or "none"
    ss = {"network": net, "security": security}
    if security == "tls":
        tls = {"serverName": p.get("sni") or p.get("host") or p.get("server"),
               "insecure": True}
        if p.get("fingerprint"):
            tls["fingerprint"] = p["fingerprint"]
        alpn = _alpn_list(p)
        if alpn:
            tls["alpn"] = alpn
        ss["tlsSettings"] = tls
    elif security == "reality":
        ss["realitySettings"] = {
            "serverName": p.get("sni") or p.get("server"),
            "publicKey": p.get("pbk") or "",
            "shortId": p.get("sid") or "",
            "fingerprint": p.get("fingerprint") or "chrome",
            "spiderX": "",
        }
    if net == "ws":
        w = {"path": p.get("path") or "/"}
        if p.get("host"):
            w["headers"] = {"Host": p["host"]}
        ss["wsSettings"] = w
    elif net == "grpc":
        ss["grpcSettings"] = {"serviceName": p.get("service_name") or "",
                              "multiMode": p.get("grpc_mode") == "multi"}
    elif net == "httpupgrade":
        h = {"path": p.get("path") or "/"}
        if p.get("host"):
            h["host"] = p["host"]
        ss["httpupgradeSettings"] = h
    elif net == "xhttp":
        x = {"path": p.get("path") or "/", "mode": p.get("grpc_mode") or "auto"}
        if p.get("host"):
            x["host"] = p["host"]
        ss["xhttpSettings"] = x
    elif net == "http":
        h = {}
        if p.get("path"):
            h["path"] = p["path"]
        if p.get("host"):
            h["host"] = [p["host"]]
        ss["httpSettings"] = h
    elif net == "tcp" and p.get("header_type") == "http":
        req = {"version": "1.1", "method": "GET", "path": [p.get("path") or "/"]}
        if p.get("host"):
            req["headers"] = {"Host": [p["host"]]}
        ss["tcpSettings"] = {"header": {"type": "http", "request": req}}
    return ss


def xray_outbound(p, tag):
    proto = p["proto"]
    addr, port = p["server"], p["port"]
    if proto == "vmess":
        st = {"vnext": [{"address": addr, "port": port, "users": [
            {"id": p.get("uuid", ""), "security": p.get("security_cipher") or "auto",
             "alterId": p.get("alter_id", 0) or 0}]}]}
        xp = "vmess"
    elif proto == "vless":
        user = {"id": p.get("uuid", ""), "encryption": "none"}
        if p.get("flow"):
            user["flow"] = p["flow"]
        st = {"vnext": [{"address": addr, "port": port, "users": [user]}]}
        xp = "vless"
    elif proto == "trojan":
        srv = {"address": addr, "port": port, "password": p.get("password", "")}
        st = {"servers": [srv]}
        xp = "trojan"
    elif proto == "ss":
        srv = {"address": addr, "port": port, "method": _norm_ss_method(p.get("method")),
               "password": p.get("password", "")}
        if p.get("plugin"):
            srv["plugin"] = p["plugin"]
            srv["pluginOpts"] = p.get("plugin_opts") or ""
        st = {"servers": [srv]}
        xp = "shadowsocks"
    elif proto in ("socks", "socks5"):
        srv = {"address": addr, "port": port}
        if p.get("user"):
            srv["users"] = [{"user": p["user"], "pass": p.get("password", "")}]
        st = {"servers": [srv]}
        xp = "socks"
    elif proto == "http":
        srv = {"address": addr, "port": port}
        if p.get("user"):
            srv["users"] = [{"user": p["user"], "pass": p.get("password", "")}]
        st = {"servers": [srv]}
        xp = "http"
    else:
        raise ValueError(f"xray: unsupported proto {proto}")
    ob = {"tag": tag, "protocol": xp, "settings": st, "mux": {"enabled": False}}
    if xp in ("vmess", "vless", "trojan"):
        ob["streamSettings"] = xray_stream_settings(p)
    return ob


def build_xray_config(items, ports):
    """items: list of proxy dicts; ports: matching list of local socks ports."""
    inbounds, outbounds, rules = [], [], []
    for i, (p, port) in enumerate(zip(items, ports)):
        inbounds.append({"tag": f"in{i}", "listen": "127.0.0.1", "port": port,
                         "protocol": "socks", "settings": {"auth": "noauth", "udp": False},
                         "sniffing": {"enabled": False}})
        outbounds.append(xray_outbound(p, f"p{i}"))
        rules.append({"type": "field", "inboundTag": [f"in{i}"],
                      "outboundTag": f"p{i}", "network": "tcp,udp"})
    outbounds.append({"tag": "direct", "protocol": "freedom"})
    return {"log": {"loglevel": "error"}, "inbounds": inbounds, "outbounds": outbounds,
            "routing": {"domainStrategy": "AsIs", "rules": rules}}


# ------------------------------------------------------------- sing-box -----

def sb_tls(p, always=False, default_alpn=None):
    security = p.get("security")
    if not always and security not in ("tls", "reality"):
        return None
    tls = {"enabled": True, "insecure": True,
           "server_name": p.get("sni") or p.get("host") or p.get("server")}
    alpn = _alpn_list(p) or default_alpn
    if alpn:
        tls["alpn"] = alpn
    if p.get("fingerprint"):
        tls["utls"] = {"enabled": True, "fingerprint": p["fingerprint"]}
    if security == "reality":
        tls["utls"] = {"enabled": True, "fingerprint": p.get("fingerprint") or "chrome"}
        tls["reality"] = {"enabled": True, "public_key": p.get("pbk") or "",
                          "short_id": p.get("sid") or ""}
    return tls


def sb_transport(p):
    net = p.get("network") or "tcp"
    if net in ("tcp", "xhttp", "kcp", "quic"):
        return None
    if net == "ws":
        t = {"type": "ws", "path": p.get("path") or "/"}
        if p.get("host"):
            t["headers"] = {"Host": p["host"]}
        return t
    if net == "grpc":
        return {"type": "grpc", "service_name": p.get("service_name") or ""}
    if net == "http":
        t = {"type": "http", "path": p.get("path") or "/"}
        if p.get("host"):
            t["host"] = [p["host"]]
        return t
    if net == "httpupgrade":
        t = {"type": "httpupgrade", "path": p.get("path") or "/"}
        if p.get("host"):
            t["host"] = p["host"]
        return t
    return None


def sb_outbound(p, tag, domain_resolver=None):
    proto = p["proto"]
    ob = {"tag": tag, "server": p["server"], "server_port": p["port"]}
    if proto == "ss":
        ob["type"] = "shadowsocks"
        ob["method"] = _norm_ss_method(p.get("method"))
        ob["password"] = p.get("password", "")
        if p.get("plugin"):
            ob["plugin"] = p["plugin"]
            ob["plugin_opts"] = p.get("plugin_opts") or ""
    elif proto in ("vmess", "vless"):
        ob["type"] = proto
        ob["uuid"] = p.get("uuid", "")
        if proto == "vmess":
            ob["security"] = p.get("security_cipher") or "auto"
            ob["alter_id"] = p.get("alter_id", 0) or 0
        else:
            if p.get("flow"):
                ob["flow"] = p["flow"]
        tls = sb_tls(p)
        if tls:
            ob["tls"] = tls
        tr = sb_transport(p)
        if tr:
            ob["transport"] = tr
    elif proto == "trojan":
        ob["type"] = "trojan"
        ob["password"] = p.get("password", "")
        ob["tls"] = sb_tls(p, always=True)
        tr = sb_transport(p)
        if tr:
            ob["transport"] = tr
    elif proto == "hysteria2":
        ob["type"] = "hysteria2"
        ob["password"] = p.get("password", "")
        ob["tls"] = sb_tls(p, always=True, default_alpn=["h3"])
        if p.get("obfs"):
            ob["obfs"] = {"type": p["obfs"], "password": p.get("obfs_password") or ""}
    elif proto == "hysteria":
        ob["type"] = "hysteria"
        ob["up_mbps"] = p.get("up_mbps") or 100
        ob["down_mbps"] = p.get("down_mbps") or 100
        if p.get("auth"):
            ob["auth_str"] = p["auth"]
        elif p.get("password"):
            ob["auth_str"] = p["password"]
        ob["tls"] = sb_tls(p, always=True, default_alpn=["h3"])
    elif proto == "tuic":
        ob["type"] = "tuic"
        ob["uuid"] = p.get("uuid", "")
        ob["password"] = p.get("password", "")
        ob["congestion_control"] = p.get("cc_alg") or "bbr"
        ob["udp_relay_mode"] = p.get("udp_relay_mode") or "native"
        ob["tls"] = sb_tls(p, always=True, default_alpn=["h3"])
    elif proto in ("socks", "socks5"):
        ob["type"] = "socks"
        ob["version"] = "5"
        if p.get("user"):
            ob["username"] = p["user"]
            ob["password"] = p.get("password", "")
    elif proto == "http":
        ob["type"] = "http"
        if p.get("user"):
            ob["username"] = p["user"]
            ob["password"] = p.get("password", "")
    else:
        raise ValueError(f"sing-box: unsupported proto {proto}")
    if domain_resolver and not _is_ip(ob["server"]):
        ob["domain_resolver"] = domain_resolver
    return ob


def _is_ip(host):
    import re
    return bool(re.match(r'^[\d.]+$', host)) or ":" in host and "[" not in host


def build_singbox_config(items, ports, use_dns=True):
    """items: list of proxy dicts; ports: matching local socks ports."""
    dns = {"servers": [{"type": "udp", "server": "1.1.1.1", "tag": "res0"}]} if use_dns else None
    resolver = "res0" if use_dns else None
    inbounds, outbounds, rules = [], [], []
    for i, (p, port) in enumerate(zip(items, ports)):
        inbounds.append({"type": "socks", "tag": f"in{i}", "listen": "127.0.0.1",
                         "listen_port": port})
        outbounds.append(sb_outbound(p, f"p{i}", resolver))
        rules.append({"inbound": [f"in{i}"], "outbound": f"p{i}"})
    outbounds.append({"type": "direct", "tag": "direct"})
    route = {"rules": rules, "final": "direct"}
    if use_dns:  # sing-box 1.12+: domains in outbounds resolve via this
        route["default_domain_resolver"] = {"server": "res0"}
    cfg = {"log": {"level": "error", "timestamp": True}, "inbounds": inbounds,
           "outbounds": outbounds, "route": route}
    if dns:
        cfg["dns"] = dns
    return cfg


# -------------------------------------------------- client-facing configs ----

def singbox_client_config(proxies, tags, max_urltest=200):
    """Ready-to-run sing-box config: mixed inbound + selector + urltest."""
    outs = []
    for p, tag in zip(proxies, tags):
        try:
            outs.append(sb_outbound(p, tag))
        except Exception:
            continue
    selector = {"type": "selector", "tag": "\U0001F41F proxy", "outbounds":
                ["\u26A1 auto"] + [o["tag"] for o in outs] + ["direct"], "default": "\u26A1 auto"}
    urltest = {"type": "urltest", "tag": "\u26A1 auto",
               "outbounds": [o["tag"] for o in outs[:max_urltest]],
               "url": "https://www.gstatic.com/generate_204", "interval": "10m"}
    direct = {"type": "direct", "tag": "direct"}
    return {
        "log": {"level": "warn", "timestamp": True},
        "dns": {"servers": [{"type": "udp", "server": "1.1.1.1", "tag": "res-0"},
                            {"type": "udp", "server": "8.8.8.8", "tag": "res-1"}]},
        "inbounds": [{"type": "mixed", "tag": "mixed-in", "listen": "127.0.0.1",
                      "listen_port": 2080}],
        "outbounds": [selector, urltest] + outs + [direct],
        "route": {"final": "\U0001F41F proxy",
                  "default_domain_resolver": {"server": "res-0"}},
    }


def xray_client_config(proxies, tags):
    """Ready-to-run xray config: socks inbound + all outbounds."""
    outs = []
    for p, tag in zip(proxies, tags):
        try:
            outs.append(xray_outbound(p, tag))
        except Exception:
            continue
    outs.append({"tag": "direct", "protocol": "freedom"})
    return {
        "log": {"loglevel": "warning"},
        "inbounds": [{"tag": "socks-in", "listen": "127.0.0.1", "port": 2080,
                      "protocol": "socks", "settings": {"auth": "noauth", "udp": True}}],
        "outbounds": outs,
    }
