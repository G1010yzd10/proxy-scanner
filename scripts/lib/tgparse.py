#!/usr/bin/env python3
"""Telegram public-channel scraping (t.me/s/<channel>) and URI extraction
from arbitrary subscription content (plain text, base64, HTML, JSON, clash YAML)."""
import base64
import html as ihtml
import json
import re

from .proxy import SCHEME_RE, b64d

B64_LINE_RE = re.compile(r'^[A-Za-z0-9+/=_-]{120,}$')
MSG_RE = re.compile(
    r'<div[^>]*class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', re.S)
TIME_RE = re.compile(r'<time[^>]*datetime="([^"]+)"', re.S)
HREF_RE = re.compile(r'href="([^"]+)"', re.S)
SUBURL_RE = re.compile(
    r'https?://[^\s"\'<>\[\]{}|\\^`]+', re.I)
TG_BLACKLIST = ("t.me/", "telegram.me", "telegram.org", "youtu", "twitter.com/",
                "x.com/", "instagram.com", "facebook.com", "whatsapp.com",
                "google.com/", "apple.com", "microsoft.com", "amazon.com", "wikipedia.org")

MAX_TEXT = 8 * 1024 * 1024


def parse_channel_html(html_text):
    """Extract (uris, latest_sub_iso, candidate_sub_urls) from a t.me/s page."""
    if not html_text or len(html_text) > MAX_TEXT:
        return [], None, []
    hrefs = [ihtml.unescape(h) for h in HREF_RE.findall(html_text)]
    messages = []
    for m in MSG_RE.finditer(html_text):
        # timestamp: nearest <time> before this message end
        start = m.start()
        times = TIME_RE.findall(html_text[:start])[-1:] or \
            TIME_RE.findall(html_text[m.end():m.end() + 3000])[:1]
        raw = m.group(1)
        text = ihtml.unescape(re.sub(r'<br\s*/?>', '\n', raw))
        text = re.sub(r'<[^>]+>', ' ', text).replace('\\/', '/')
        messages.append((times[0] if times else None, text))
    corpus = text_all = ihtml.unescape(
        re.sub(r'<[^>]+>', ' ', html_text)).replace('\\/', '/')
    hrefs_text = " ".join(hrefs).replace('\\/', '/')
    uris = extract_uris(corpus + "\n" + hrefs_text)

    latest = None
    for ts, text in messages:
        if ts and extract_uris(text.replace('\\/', '/')):
            if latest is None or ts > latest:
                latest = ts
    if latest is None and messages:
        # fall back to latest message time at all
        for ts, _ in messages:
            if ts and (latest is None or ts > latest):
                latest = ts

    sub_urls = []
    for h in hrefs:
        h = h.strip().rstrip('.,;)')
        if not h.lower().startswith(("http://", "https://")):
            continue
        if any(b in h.lower() for b in TG_BLACKLIST):
            continue
        if SCHEME_RE.search(h):  # it's a proxy link, not a sub
            continue
        sub_urls.append(h)
    return uris, latest, sub_urls[:8]


def _strip_html(text):
    if "<" in text and ">" in text and ("</" in text or "/>" in text or "<br" in text.lower()):
        hrefs = " ".join(ihtml.unescape(h) for h in HREF_RE.findall(text))
        t = ihtml.unescape(re.sub(r'<[^>]+>', ' ', text))
        return t + "\n" + hrefs
    return text


def extract_uris(text, depth=0):
    """Find proxy URIs in text (also decodes base64 chunks, recursively)."""
    if not text:
        return []
    text = _strip_html(text)
    text = text.replace('\\/', '/')
    found = []
    for m in SCHEME_RE.finditer(text):
        u = m.group(1).strip().rstrip('.,;)]}>\"\'')
        if u:
            found.append(u)
    if depth >= 2:
        return found
    # whole-text base64 blob
    if not found:
        compact = "".join(text.split())
        if len(compact) >= 80 and re.fullmatch(r'[A-Za-z0-9+/=_-]+', compact):
            dec = b64d(compact)
            if dec:
                try:
                    t = dec.decode("utf-8")
                    if "://" in t:
                        found = extract_uris(t, depth + 1)
                except Exception:
                    pass
    # per-line base64 (subscription chunks)
    if not found:
        for line in text.splitlines():
            line = line.strip()
            if 120 <= len(line) <= 65536 and B64_LINE_RE.match(line):
                dec = b64d(line)
                if dec:
                    try:
                        t = dec.decode("utf-8")
                        if "://" in t:
                            found.extend(extract_uris(t, depth + 1))
                    except Exception:
                        pass
    return found


# ------------------------------------------------------ structured formats ---

def proxies_from_structured(text, fmt=None):
    """Parse clash YAML / xray JSON / nekobox JSON into internal proxy dicts."""
    text = text.strip()
    if not text:
        return []
    fmt = fmt or _detect_format(text)
    if fmt == "xrayjson":
        return _from_xray_json(text)
    if fmt == "nekobox":
        return _from_nekobox(text)
    if fmt == "clash":
        return _from_clash(text)
    return []


def _detect_format(text):
    t = text.lstrip()
    if t.startswith("{") or t.startswith("["):
        try:
            j = json.loads(text)
        except Exception:
            return None
        if isinstance(j, dict) and isinstance(j.get("outbounds"), list):
            return "xrayjson"
        if isinstance(j, list) and j and isinstance(j[0], dict) and "server" in j[0]:
            return "nekobox"
        return None
    if re.search(r'(?m)^\s*proxies\s*:', text):
        return "clash"
    return None


def _from_xray_json(text):
    import urllib.parse
    from .proxy import parse_uri
    try:
        j = json.loads(text)
    except Exception:
        return []
    out = []
    for ob in j.get("outbounds", []):
        proto = ob.get("protocol", "")
        ss = ob.get("streamSettings", {}) or {}
        if proto in ("vmess", "vless"):
            vnext = (ob.get("settings", {}).get("vnext") or [None])[0]
            if not vnext:
                continue
            user = (vnext.get("users") or [{}])[0]
            net = ss.get("network", "tcp")
            tls = ss.get("security", "none")
            if net == "splithttp":
                net = "xhttp"
            q = {"type": net, "security": tls}
            ws = ss.get("wsSettings") or {}
            if ws.get("path"):
                q["path"] = ws.get("path")
            host = (ws.get("headers") or {}).get("Host", "")
            if host:
                q["host"] = host
            grpc = ss.get("grpcSettings") or {}
            if grpc.get("serviceName"):
                q["serviceName"] = grpc["serviceName"]
            ts = ss.get("tlsSettings") or {}
            if ts.get("serverName"):
                q["sni"] = ts.get("serverName")
            rs = ss.get("realitySettings") or {}
            if rs.get("publicKey"):
                q["pbk"] = rs["publicKey"]
                q["security"] = "reality"
            if rs.get("shortId"):
                q["sid"] = rs["shortId"]
            if rs.get("fingerprint"):
                q["fp"] = rs["fingerprint"]
            if user.get("flow"):
                q["flow"] = user["flow"]
            frag = ob.get("tag", "")
            if proto == "vmess":
                j2 = {"v": "2", "ps": frag, "add": vnext["address"], "port": vnext.get("port", 443),
                      "id": user.get("id", ""), "aid": user.get("alterId", 0),
                      "scy": user.get("security", "auto"), "net": net, "type": "none",
                      "host": host, "path": ws.get("path", ""),
                      "tls": tls if tls in ("tls", "reality") else "",
                      "sni": ts.get("serverName", ""), "fp": rs.get("fingerprint", "")}
                uri = "vmess://" + base64.b64encode(
                    json.dumps(j2, ensure_ascii=False).encode()).decode()
            else:
                uri = (f"vless://{user.get('id','')}@{vnext['address']}:{vnext.get('port',443)}?"
                       + urllib.parse.urlencode(q))
                if frag:
                    uri += "#" + urllib.parse.quote(frag)
            p = parse_uri(uri)
            if p:
                out.append(p)
        elif proto in ("trojan", "shadowsocks", "socks", "http"):
            srv = (ob.get("settings", {}).get("servers") or [None])[0]
            if not srv:
                continue
            if proto == "trojan":
                uri = f"trojan://{srv.get('password','')}@{srv['address']}:{srv.get('port',443)}?security=tls&type=tcp"
            elif proto == "shadowsocks":
                cred = base64.urlsafe_b64encode(
                    f"{srv.get('method','')}:{srv.get('password','')}".encode()).decode().rstrip("=")
                uri = f"ss://{cred}@{srv['address']}:{srv.get('port',8388)}"
            elif proto == "socks":
                uri = f"socks://{srv['address']}:{srv.get('port',1080)}"
            else:
                uri = f"http://{srv['address']}:{srv.get('port',8080)}"
            if ob.get("tag"):
                uri += "#" + urllib.parse.quote(ob["tag"])
            p = parse_uri(uri)
            if p:
                out.append(p)
    return out


def _from_nekobox(text):
    from .proxy import parse_uri
    try:
        arr = json.loads(text)
    except Exception:
        return []
    out = []
    if not isinstance(arr, list):
        return out
    for e in arr:
        try:
            t = (e.get("type") or "").lower()
            srv, port = e.get("server"), e.get("server_port")
            if not srv or not port:
                continue
            if t == "shadowsocks":
                cred = base64.urlsafe_b64encode(
                    f"{e.get('method','')}:{e.get('password','')}".encode()).decode().rstrip("=")
                uri = f"ss://{cred}@{srv}:{port}"
            elif t in ("socks", "socks5"):
                uri = f"socks://{srv}:{port}"
            elif t == "http":
                uri = f"http://{srv}:{port}"
            elif t in ("vmess", "vless", "trojan", "hysteria2", "tuic"):
                uuid_or_pass = e.get("uuid") or e.get("password") or ""
                scheme = t
                if t in ("vmess", "vless"):
                    uri = f"{scheme}://{uuid_or_pass}@{srv}:{port}?security=tls&type=tcp"
                elif t == "trojan":
                    uri = f"trojan://{uuid_or_pass}@{srv}:{port}?security=tls&type=tcp"
                else:
                    uri = f"{scheme}://{uuid_or_pass}@{srv}:{port}?insecure=1"
            else:
                continue
            if e.get("name"):
                uri += "#" + urllib.parse.quote(str(e["name"]))
            p = parse_uri(uri)
            if p:
                out.append(p)
        except Exception:
            continue
    return out


def _from_clash(text):
    import urllib.parse
    try:
        import yaml
        j = yaml.safe_load(text)
    except Exception:
        return []
    if not isinstance(j, dict):
        return []
    proxies = j.get("proxies") or []
    out = []
    for e in proxies:
        try:
            if not isinstance(e, dict):
                continue
            t = (e.get("type") or "").lower()
            srv, port = e.get("server"), e.get("port")
            if not srv or not port:
                continue
            name = urllib.parse.quote(str(e.get("name") or "clash"))
            if t == "ss":
                cred = base64.urlsafe_b64encode(
                    f"{e.get('cipher','')}:{e.get('password','')}".encode()).decode().rstrip("=")
                uri = f"ss://{cred}@{srv}:{port}"
                pl = e.get("plugin")
                if pl == "obfs":
                    po = e.get("plugin-opts") or {}
                    opts = f"obfs={po.get('mode','http')}"
                    if po.get("host"):
                        opts += f";obfs-host={po['host']}"
                    uri += "?plugin=" + urllib.parse.quote(f"obfs-local;{opts}")
                elif pl == "v2ray-plugin":
                    po = e.get("plugin-opts") or {}
                    opts = "mode=websocket"
                    if po.get("tls"):
                        opts += ";tls"
                    if po.get("host"):
                        opts += f";host={po['host']}"
                    if po.get("path"):
                        opts += f";path={po['path']}"
                    uri += "?plugin=" + urllib.parse.quote(f"v2ray-plugin;{opts}")
            elif t == "vmess":
                uri = "vmess://" + base64.b64encode(json.dumps({
                    "v": "2", "ps": e.get("name", ""), "add": srv, "port": str(port),
                    "id": e.get("uuid", ""), "aid": e.get("alterId", 0) or 0,
                    "scy": e.get("cipher", "auto"), "net": e.get("network", "tcp"),
                    "type": "none", "host": (e.get("ws-opts") or {}).get("headers", {}).get("Host", ""),
                    "path": (e.get("ws-opts") or {}).get("path", ""),
                    "tls": "tls" if e.get("tls") else "",
                    "sni": e.get("servername", "")}).encode()).decode()
            elif t == "vless":
                q = {"security": "tls" if e.get("tls") else "none",
                     "type": e.get("network", "tcp")}
                sn = e.get("servername") or e.get("sni")
                if sn:
                    q["sni"] = sn
                ws = e.get("ws-opts") or {}
                if ws.get("path"):
                    q["path"] = ws["path"]
                h = (ws.get("headers") or {}).get("Host")
                if h:
                    q["host"] = h
                gs = e.get("grpc-opts") or {}
                if gs.get("grpc-service-name"):
                    q["serviceName"] = gs["grpc-service-name"]
                ro = e.get("reality-opts") or {}
                if ro.get("public-key"):
                    q["security"] = "reality"
                    q["pbk"] = ro["public-key"]
                if ro.get("short-id"):
                    q["sid"] = ro["short-id"]
                if e.get("client-fingerprint"):
                    q["fp"] = e["client-fingerprint"]
                if e.get("flow"):
                    q["flow"] = e["flow"]
                uri = f"vless://{e.get('uuid','')}@{srv}:{port}?" + urllib.parse.urlencode(q)
            elif t == "trojan":
                uri = f"trojan://{e.get('password','')}@{srv}:{port}?security=tls&type={(e.get('network') or 'tcp')}"
                if e.get("sni"):
                    uri += "&sni=" + urllib.parse.quote(e["sni"])
            elif t in ("hysteria2", "hysteria"):
                q = "insecure=1"
                if e.get("sni"):
                    q += "&sni=" + urllib.parse.quote(e["sni"])
                uri = f"{t}://{urllib.parse.quote(str(e.get('password','')), safe='')}@{srv}:{port}?{q}"
            elif t == "tuic":
                uri = (f"tuic://{e.get('uuid','')}:{urllib.parse.quote(str(e.get('password','')), safe='')}"
                       f"@{srv}:{port}?congestion_control={e.get('congestion-controller','bbr')}&alpn=h3")
            elif t in ("socks5", "socks"):
                uri = f"socks://{srv}:{port}"
            elif t == "http":
                uri = f"http://{srv}:{port}"
            else:
                continue
            if t != "vmess":
                uri += "#" + name
            from .proxy import parse_uri
            p = parse_uri(uri)
            if p:
                out.append(p)
        except Exception:
            continue
    return out
