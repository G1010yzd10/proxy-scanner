#!/usr/bin/env python3
"""Proxy URI parsing, cleaning, canonical hashing and serialization.

Internal proxy representation (dict):
  proto: ss|vmess|vless|trojan|hysteria2|hysteria|tuic|socks|http
  server, port, name, + protocol specific fields
"""
import base64
import hashlib
import json
import re
import urllib.parse

SCHEME_RE = re.compile(
    r'(?i)\b((?:vless|vmess|trojan|ssr|ss|hysteria2|hysteria|hy2|tuic|juicity|snell|'
    r'brook|wireguard|socks5|socks|https|http)://[^\s"\'<>`\\]+)')

KNOWN_NETWORKS = {"tcp", "ws", "grpc", "http", "httpupgrade", "xhttp", "quic", "kcp"}
UUID_RE = re.compile(r'^[0-9a-f]{32}$')
PRIVATE_RE = re.compile(
    r'^(127\.|10\.|192\.168\.|169\.254\.|0\.0\.0\.0$|::1$|localhost$|'
    r'172\.(1[6-9]|2\d|3[01])\.)')

# canonical field order for hashing (name/sources/timestamps excluded on purpose:
# the hash identifies the *proxy*, not its label)
CANON_KEYS = [
    "proto", "server", "port", "uuid", "password", "method", "plugin", "plugin_opts",
    "alter_id", "security_cipher", "network", "header_type", "host", "path",
    "service_name", "grpc_mode", "security", "sni", "alpn", "fingerprint", "flow",
    "pbk", "sid", "obfs", "obfs_password", "up_mbps", "down_mbps", "cc_alg",
    "udp_relay_mode", "user", "version",
]


def b64d(s: str):
    """Lenient base64 decoder (standard or urlsafe, padded or not)."""
    if not s:
        return None
    s = "".join(s.split())
    s = s.replace("-", "+").replace("_", "/")
    s += "=" * ((4 - len(s) % 4) % 4)
    try:
        return base64.b64decode(s, validate=False)
    except Exception:
        return None


def _split_host_port(hp: str):
    hp = (hp or "").strip()
    if not hp:
        return None, None
    if hp.startswith("["):  # ipv6
        host, _, rest = hp[1:].partition("]")
        port = None
        if rest.startswith(":"):
            port = rest[1:]
        return host, port
    host, sep, port = hp.rpartition(":")
    if not sep:
        return hp, None
    return host, port


def _int_or(v, d=None):
    try:
        return int(str(v).strip())
    except Exception:
        return d


def _unq(v):
    return urllib.parse.unquote(v) if v else v


# ---------------------------------------------------------------- parsers ---

def _base(proto, server, port, name=""):
    return {"proto": proto, "server": (server or "").strip(), "port": port,
            "name": (name or "").strip()[:80]}


def parse_ss(uri):
    body = uri[5:]
    frag = ""
    if "#" in body:
        body, frag = body.split("#", 1)
    frag = _unq(frag)
    query = {}
    if "?" in body:
        body, qs = body.split("?", 1)
        query = urllib.parse.parse_qs(qs, keep_blank_values=True)
    method = password = None
    if "@" in body:
        userinfo, hostport = body.rsplit("@", 1)
        userinfo = _unq(userinfo)
        if ":" in userinfo:  # plain method:pass
            method, password = userinfo.split(":", 1)
        else:                # base64(method:pass)
            dec = b64d(userinfo)
            cred = dec.decode("utf-8", "replace") if dec else ""
            if ":" in cred:
                method, password = cred.split(":", 1)
        hp = hostport
    else:
        dec = b64d(body)
        if not dec:
            return None
        s = dec.decode("utf-8", "replace")
        if "@" not in s:
            return None
        cred, hp = s.rsplit("@", 1)
        method, password = cred.split(":", 1) if ":" in cred else (cred, "")
    host, port = _split_host_port(hp)
    if not host:
        return None
    p = _base("ss", host, _int_or(port), frag)
    p.update({"method": (method or "").strip(), "password": password or ""})
    pl = _unq(query.get("plugin", [None])[0]) if query.get("plugin") else None
    if pl:
        parts = pl.split(";")
        p["plugin"] = parts[0].strip() or None
        opts = ";".join(parts[1:]).strip()
        p["plugin_opts"] = opts or None
    return p


def parse_vmess(uri):
    body = uri[8:].split("#", 1)[0]
    dec = b64d(body)
    if not dec:
        return None
    try:
        j = json.loads(dec)
    except Exception:
        return None
    if not isinstance(j, dict):
        return None
    host = str(j.get("add", "") or "").strip()
    if not host:
        return None
    net = str(j.get("net", "tcp") or "tcp").lower()
    if net in ("h2", "h2c"):
        net = "http"
    if net == "splithttp":
        net = "xhttp"
    if net not in KNOWN_NETWORKS:
        net = "tcp"
    tls = str(j.get("tls", "") or "").strip().lower()
    security = "tls" if tls == "tls" else ("reality" if tls == "reality" else "none")
    p = _base("vmess", host, _int_or(j.get("port"), 443), str(j.get("ps", "") or ""))
    p.update({
        "uuid": str(j.get("id", "") or "").strip().lower(),
        "alter_id": _int_or(j.get("aid"), 0) or 0,
        "security_cipher": str(j.get("scy", "auto") or "auto"),
        "network": net,
        "header_type": str(j.get("type", "none") or "none").lower(),
        "host": str(j.get("host", "") or "").strip(),
        "path": str(j.get("path", "") or ""),
        "security": security,
        "sni": str(j.get("sni", "") or "").strip(),
        "alpn": str(j.get("alpn", "") or ""),
        "fingerprint": str(j.get("fp", "") or "").strip(),
    })
    return p


def _parse_urlish(uri, proto, default_port, is_password_userinfo=False):
    try:
        u = urllib.parse.urlsplit(uri)
    except Exception:
        return None
    if not u.hostname:
        return None
    q = urllib.parse.parse_qs(u.query, keep_blank_values=True)

    def g(k, d=""):
        v = q.get(k)
        return v[0] if v else d

    net = (g("type") or "tcp").lower()
    if net in ("", "none", "raw"):
        net = "tcp"
    if net == "h2":
        net = "http"
    if net in ("splithttp",):
        net = "xhttp"
    if net not in KNOWN_NETWORKS:
        net = "tcp"
    security = g("security").lower()
    if proto == "trojan" and not security:
        security = "tls"
    if proto == "vless" and not security:
        security = "tls" if (g("sni") or g("alpn") or g("fp")) else "none"
    insecure = g("allowInsecure") in ("1", "true") or g("insecure") in ("1", "true") \
        or g("allow_insecure") in ("1", "true")
    p = _base(proto, u.hostname, u.port or default_port, _unq(u.fragment))
    p.update({
        "network": net,
        "header_type": (g("headerType") or "").lower(),
        "host": _unq(g("host")).strip(),
        "path": _unq(g("path")),
        "service_name": _unq(g("serviceName")),
        "grpc_mode": g("mode").lower() if g("mode") else "",
        "security": security,
        "sni": g("sni").strip(),
        "alpn": g("alpn"),
        "fingerprint": g("fp").strip(),
        "flow": g("flow").strip(),
        "pbk": g("pbk"),
        "sid": g("sid"),
        "insecure": insecure,
    })
    userinfo = _unq(u.username or "")
    if proto == "vless":
        p["uuid"] = (userinfo or "").strip().lower()
    elif proto == "trojan":
        p["password"] = userinfo or ""
    return p


def parse_vless(uri):
    return _parse_urlish(uri, "vless", 443)


def parse_trojan(uri):
    return _parse_urlish(uri, "trojan", 443)


def parse_hysteria2(uri):
    try:
        u = urllib.parse.urlsplit(uri)
    except Exception:
        return None
    if not u.hostname:
        return None
    q = urllib.parse.parse_qs(u.query, keep_blank_values=True)

    def g(k, d=""):
        v = q.get(k)
        return v[0] if v else d

    p = _base("hysteria2", u.hostname, u.port or 443, _unq(u.fragment))
    p.update({
        "password": _unq(u.username or ""),
        "sni": g("sni").strip(),
        "insecure": g("insecure") in ("1", "true") or g("allowInsecure") in ("1", "true"),
        "obfs": g("obfs"),
        "obfs_password": g("obfs-password"),
    })
    return p


def parse_hysteria(uri):
    try:
        u = urllib.parse.urlsplit(uri)
    except Exception:
        return None
    if not u.hostname:
        return None
    q = urllib.parse.parse_qs(u.query, keep_blank_values=True)

    def g(k, d=""):
        v = q.get(k)
        return v[0] if v else d

    p = _base("hysteria", u.hostname, u.port or 443, _unq(u.fragment))
    p.update({
        "password": _unq(u.username or ""),
        "auth": g("auth"),
        "sni": (g("peer") or g("sni")).strip(),
        "insecure": g("insecure") in ("1", "true"),
        "obfs": g("obfs"),
        "up_mbps": _int_or(g("upmbps"), 100) or 100,
        "down_mbps": _int_or(g("downmbps"), 100) or 100,
        "alpn": g("alpn") or "h3",
    })
    return p


def parse_tuic(uri, proto="tuic"):
    try:
        u = urllib.parse.urlsplit(uri)
    except Exception:
        return None
    if not u.hostname:
        return None
    q = urllib.parse.parse_qs(u.query, keep_blank_values=True)

    def g(k, d=""):
        v = q.get(k)
        return v[0] if v else d

    user = _unq(u.username or "")
    password = _unq(u.password or "")
    p = _base(proto, u.hostname, u.port or 443, _unq(u.fragment))
    p.update({
        "uuid": (user or "").lower(),
        "password": password,
        "sni": g("sni").strip(),
        "insecure": g("allow_insecure") in ("1", "true") or g("insecure") in ("1", "true"),
        "cc_alg": g("congestion_control") or "bbr",
        "udp_relay_mode": g("udp_relay_mode") or "native",
        "alpn": g("alpn") or "h3",
    })
    return p


def parse_socks(uri, proto="socks"):
    try:
        u = urllib.parse.urlsplit(uri)
    except Exception:
        return None
    if not u.hostname:
        return None
    user = _unq(u.username or "")
    if user and ":" not in user:
        dec = b64d(user)
        if dec:
            s = dec.decode("utf-8", "replace")
            if ":" in s:
                user = s.split(":", 1)[0]
                u = urllib.parse.SplitResult(u.scheme, f"{_quote_userinfo(user, s.split(':', 1)[1])}@{u.netloc.split('@')[-1]}", u.path, u.query, u.fragment)
    p = _base(proto, u.hostname, u.port or 1080, _unq(u.fragment))
    p["user"] = user
    p["password"] = _unq(u.password or "")
    p["version"] = "5" if proto in ("socks", "socks5") else "4"
    return p


def _quote_userinfo(u, p):
    return urllib.parse.quote(u, safe="") + ":" + urllib.parse.quote(p, safe="")


def parse_http_proxy(uri):
    try:
        u = urllib.parse.urlsplit(uri)
    except Exception:
        return None
    if not u.hostname:
        return None
    p = _base("http", u.hostname, u.port or 8080, _unq(u.fragment))
    p["user"] = _unq(u.username or "")
    p["password"] = _unq(u.password or "")
    return p


PARSERS = {
    "ss": parse_ss, "vmess": parse_vmess, "vless": parse_vless, "trojan": parse_trojan,
    "hysteria2": parse_hysteria2, "hy2": parse_hysteria2, "hysteria": parse_hysteria,
    "tuic": parse_tuic, "socks": parse_socks, "socks5": parse_socks,
    "http": parse_http_proxy, "https": parse_http_proxy,
}


def parse_uri(uri):
    """Parse a proxy URI into an internal dict, or None."""
    uri = uri.strip().rstrip(".,;)]}>\"'")
    m = re.match(r'^([a-zA-Z0-9+]+)://', uri)
    if not m:
        return None
    scheme = m.group(1).lower()
    fn = PARSERS.get(scheme)
    if fn is None:
        return None
    try:
        return fn(uri)
    except Exception:
        return None


# ------------------------------------------------------------------ clean ---

def clean_proxy(p):
    """Validate/normalize a parsed proxy. Returns (proxy|None, error_reason)."""
    if not p:
        return None, "unparsable"
    server = (p.get("server") or "").strip().lower()
    if not server or len(server) > 253:
        return None, "bad_server"
    if not re.match(r'^[a-z0-9.\[\]_-]+$', server):
        return None, "bad_server_chars"
    if PRIVATE_RE.match(server):
        return None, "private_ip"
    port = _int_or(p.get("port"))
    if port is None or not (1 <= port <= 65535):
        return None, "bad_port"
    p["server"] = server
    p["port"] = port
    proto = p.get("proto")
    if proto in ("vless", "vmess", "tuic"):
        uuid = re.sub(r'[-]', '', p.get("uuid") or "").lower()
        if not UUID_RE.match(uuid or ""):
            return None, "bad_uuid"
    if proto == "ss":
        if not p.get("method"):
            return None, "no_method"
        if not p.get("password"):
            return None, "no_password"
    for k in ("host", "path", "sni", "service_name"):
        if len(str(p.get(k) or "")) > 512:
            p[k] = str(p[k])[:512]
    if p.get("network") not in KNOWN_NETWORKS:
        p["network"] = "tcp"
    p["name"] = re.sub(r'[\r\n\t]+', ' ', str(p.get("name") or "")).strip()[:80]
    return p, None


# ------------------------------------------------------------------ hash ----

def _canon_val(v):
    if isinstance(v, str):
        v = v.strip()
        if "," in v and "/" not in v:  # alpn-like list
            parts = sorted(x.strip().lower() for x in v.split(",") if x.strip())
            return ",".join(parts)
        return v.lower() if re.fullmatch(r'[0-9a-fA-F:\-]{32,45}', v) or "." not in v and len(v) < 12 else v
    return v


def canonical_json(p):
    d = {}
    for k in CANON_KEYS:
        v = p.get(k)
        if v in (None, "", []):
            continue
        if k == "server":
            v = str(v).strip().lower()
        elif k in ("uuid", "sni"):
            v = str(v).strip().lower()
        elif k == "alpn":
            v = ",".join(sorted(x.strip().lower() for x in str(v).split(",") if x.strip()))
        d[k] = v
    return json.dumps(d, sort_keys=True, ensure_ascii=False)


def phash(p):
    return hashlib.sha256(canonical_json(p).encode("utf-8")).hexdigest()[:20]


# ------------------------------------------------------------ serialize -----

def _b64e(s, urlsafe=True):
    raw = s.encode("utf-8")
    if urlsafe:
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")
    return base64.b64encode(raw).decode()


def uri_from_proxy(p, name=None, default_scheme=None):
    """Serialize internal proxy back to a URI. name=None -> name stripped (ban list)."""
    proto = p.get("proto")
    nm = p.get("name") if name is None else name
    frag = urllib.parse.quote(nm, safe="") if nm else ""
    host = p.get("server", "")
    port = p.get("port", "")
    if proto == "ss":
        userinfo = _b64e(f"{p.get('method','')}:{p.get('password','')}")
        uri = f"ss://{userinfo}@{host}:{port}"
        if p.get("plugin"):
            pl = p["plugin"] + (";" + p["plugin_opts"] if p.get("plugin_opts") else "")
            uri += "?" + urllib.parse.urlencode({"plugin": pl})
    elif proto == "vmess":
        j = {"v": "2", "ps": nm or "", "add": host, "port": str(port),
             "id": p.get("uuid", ""), "aid": str(p.get("alter_id", 0)),
             "scy": p.get("security_cipher", "auto"), "net": p.get("network", "tcp"),
             "type": p.get("header_type", "none"), "host": p.get("host", ""),
             "path": p.get("path", ""), "tls": p.get("security") if p.get("security") in ("tls", "reality") else "",
             "sni": p.get("sni", ""), "alpn": p.get("alpn", ""), "fp": p.get("fingerprint", "")}
        return "vmess://" + _b64e(json.dumps(j, ensure_ascii=False, separators=(",", ":")), urlsafe=False)
    elif proto == "vless":
        q = {"encryption": "none", "security": p.get("security") or "none",
             "type": p.get("network", "tcp")}
        for k_src, k_dst in (("sni", "sni"), ("fingerprint", "fp"), ("flow", "flow"),
                              ("pbk", "pbk"), ("sid", "sid"), ("alpn", "alpn"),
                              ("host", "host"), ("path", "path"),
                              ("service_name", "serviceName"), ("grpc_mode", "mode"),
                              ("header_type", "headerType")):
            if p.get(k_src):
                q[k_dst] = p[k_src]
        uri = f"vless://{p.get('uuid','')}@{host}:{port}?" + urllib.parse.urlencode(q)
    elif proto == "trojan":
        q = {"security": p.get("security") or "tls", "type": p.get("network", "tcp")}
        for k_src, k_dst in (("sni", "sni"), ("fingerprint", "fp"), ("alpn", "alpn"),
                              ("host", "host"), ("path", "path"),
                              ("service_name", "serviceName"), ("grpc_mode", "mode")):
            if p.get(k_src):
                q[k_dst] = p[k_src]
        uri = f"trojan://{urllib.parse.quote(str(p.get('password','')), safe='') }@{host}:{port}?" + urllib.parse.urlencode(q)
    elif proto == "hysteria2":
        q = {}
        if p.get("sni"):
            q["sni"] = p["sni"]
        if p.get("insecure"):
            q["insecure"] = "1"
        if p.get("obfs"):
            q["obfs"] = p["obfs"]
        if p.get("obfs_password"):
            q["obfs-password"] = p["obfs_password"]
        uri = f"hysteria2://{urllib.parse.quote(str(p.get('password','')), safe='')}@{host}:{port}"
        if q:
            uri += "?" + urllib.parse.urlencode(q)
    elif proto == "hysteria":
        q = {"upmbps": str(p.get("up_mbps", 100)), "downmbps": str(p.get("down_mbps", 100))}
        if p.get("auth"):
            q["auth"] = p["auth"]
        if p.get("sni"):
            q["peer"] = p["sni"]
        if p.get("insecure"):
            q["insecure"] = "1"
        uri = f"hysteria://{host}:{port}?" + urllib.parse.urlencode(q)
    elif proto == "tuic":
        q = {"congestion_control": p.get("cc_alg", "bbr"),
             "udp_relay_mode": p.get("udp_relay_mode", "native")}
        if p.get("sni"):
            q["sni"] = p["sni"]
        if p.get("alpn"):
            q["alpn"] = p["alpn"]
        if p.get("insecure"):
            q["allow_insecure"] = "1"
        uri = f"tuic://{p.get('uuid','')}:{urllib.parse.quote(str(p.get('password','')), safe='')}@{host}:{port}?" + urllib.parse.urlencode(q)
    elif proto in ("socks", "socks5"):
        userinfo = ""
        if p.get("user"):
            userinfo = _b64e(f"{p['user']}:{p.get('password','')}") + "@"
        uri = f"socks://{userinfo}{host}:{port}"
    elif proto == "http":
        userinfo = ""
        if p.get("user"):
            userinfo = urllib.parse.quote(p["user"], safe="") + ":" + \
                urllib.parse.quote(str(p.get("password", "")), safe="") + "@"
        uri = f"http://{userinfo}{host}:{port}"
    else:
        return None
    if frag and proto not in ("vmess",):
        uri += "#" + frag
    return uri


# ------------------------------------------------------------------ misc ----

_CC_CACHE = {}


def flag(cc):
    if not cc or len(cc) != 2 or not cc.isalpha():
        return "\U0001F3F3"
    cc = cc.upper()
    if cc not in _CC_CACHE:
        _CC_CACHE[cc] = "".join(chr(0x1F1E6 + ord(c) - 65) for c in cc)
    return _CC_CACHE[cc]


def fmt_name(pid, in_cc, out_cc):
    """Display name: '#ID INBOUND -> OUTBOUND' e.g. '#42 US -> DE'."""
    def side(cc):
        return f"{flag(cc)} {cc.upper()}" if cc and len(cc) == 2 else "\u2753 ??"
    return f"#{pid} {side(in_cc)} \u2192 {side(out_cc)}"
