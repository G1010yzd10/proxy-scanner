#!/usr/bin/env python3
"""Unit tests for the proxy-scanner libs (no network, no engines needed)."""
import base64
import json
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from lib import proxy as P  # noqa: E402
from lib import engines as E  # noqa: E402
from lib import tgparse as T  # noqa: E402
from lib import states as S  # noqa: E402


# ------------------------------------------------------------------ ss ------

def test_ss_plain_userinfo():
    p = P.parse_uri("ss://aes-256-gcm:pass123@1.2.3.4:8388#Tokyo")
    assert p and p["proto"] == "ss" and p["server"] == "1.2.3.4"
    assert p["port"] == 8388 and p["method"] == "aes-256-gcm"
    assert p["password"] == "pass123" and p["name"] == "Tokyo"


def test_ss_b64_userinfo():
    cred = base64.urlsafe_b64encode(b"chacha20:p w@:x").decode().rstrip("=")
    p = P.parse_uri(f"ss://{cred}@example.com:443")
    assert p and p["method"] == "chacha20" and p["password"] == "p w@:x"


def test_ss_full_b64_body():
    body = base64.b64encode(b"aes-128-gcm:pw@5.6.7.8:9999").decode()
    p = P.parse_uri(f"ss://{body}")
    assert p and p["server"] == "5.6.7.8" and p["port"] == 9999


def test_ss_plugin():
    p = P.parse_uri(
        "ss://aes-256-gcm:pw@1.1.1.1:80?plugin=v2ray-plugin%3Bmode%3Dwebsocket%3Btls")
    assert p and p["plugin"] == "v2ray-plugin"
    assert "mode=websocket" in p["plugin_opts"]


# ---------------------------------------------------------------- vmess -----

def _vmess_uri(**over):
    j = {"v": "2", "ps": "test node", "add": "vm.example.org", "port": "443",
         "id": "12345678-1234-1234-1234-123456789abc", "aid": "0",
         "scy": "auto", "net": "ws", "type": "none", "host": "cdn.example.org",
         "path": "/ws", "tls": "tls", "sni": "vm.example.org"}
    j.update(over)
    return "vmess://" + base64.b64encode(json.dumps(j).encode()).decode()


def test_vmess_full():
    p = P.parse_uri(_vmess_uri())
    assert p and p["proto"] == "vmess" and p["server"] == "vm.example.org"
    assert p["port"] == 443 and p["network"] == "ws" and p["security"] == "tls"
    assert p["uuid"] == "12345678-1234-1234-1234-123456789abc"
    assert p["host"] == "cdn.example.org" and p["path"] == "/ws"


def test_vmess_bad_b64():
    assert P.parse_uri("vmess://!!!not-base64!!!") is None


def test_vmess_h2_becomes_http():
    p = P.parse_uri(_vmess_uri(net="h2"))
    assert p["network"] == "http"


# ---------------------------------------------------------------- vless -----

def test_vless_reality():
    u = ("vless://11111111-2222-3333-4444-555555555555@re.example.com:443"
         "?encryption=none&security=reality&sni=x.com&fp=chrome&pbk=PUBKEY&sid=ab12"
         "&type=tcp&flow=xtls-rprx-vision#reality-node")
    p = P.parse_uri(u)
    assert p and p["proto"] == "vless" and p["security"] == "reality"
    assert p["pbk"] == "PUBKEY" and p["sid"] == "ab12" and p["flow"]
    assert p["fingerprint"] == "chrome"


def test_vless_grpc():
    u = ("vless://11111111-2222-3333-4444-555555555555@g.example.com:443"
         "?type=grpc&security=tls&serviceName=svc&mode=gun#grpc-node")
    p = P.parse_uri(u)
    assert p and p["network"] == "grpc" and p["service_name"] == "svc"


# ---------------------------------------------------------------- trojan ----

def test_trojan_defaults_tls():
    p = P.parse_uri("trojan://secretpw@t.example.com:443#tr")
    assert p and p["security"] == "tls" and p["password"] == "secretpw"


# ------------------------------------------------------------- hysteria2 ----

def test_hysteria2():
    u = "hysteria2://pw@h.example.com:8443?sni=h.example.com&insecure=1&obfs=salamander&obfs-password=ob#hy2"
    p = P.parse_uri(u)
    assert p and p["proto"] == "hysteria2" and p["insecure"] is True
    assert p["obfs"] == "salamander" and p["obfs_password"] == "ob"


# ------------------------------------------------------------------ tuic ----

def test_tuic():
    u = "tuic://11111111-2222-3333-4444-555555555555:pw@t.example.com:8443?congestion_control=bbr&alpn=h3"
    p = P.parse_uri(u)
    assert p and p["proto"] == "tuic" and p["cc_alg"] == "bbr"
    assert p["uuid"] == "11111111-2222-3333-4444-555555555555"


# ----------------------------------------------------------- socks / http ---

def test_socks():
    p = P.parse_uri("socks://1.2.3.4:1080#plain")
    assert p and p["proto"] == "socks" and p["port"] == 1080 and p["version"] == "5"


def test_http_proxy():
    p = P.parse_uri("http://user:pass@5.6.7.8:8080#hp")
    assert p and p["proto"] == "http" and p["user"] == "user"


# ---------------------------------------------------------------- clean -----

def test_clean_rejects_private_and_bad_ports():
    p, why = P.clean_proxy(P.parse_uri("socks://192.168.1.1:1080"))
    assert p is None and why == "private_ip"
    p, why = P.clean_proxy(P.parse_uri("socks://1.2.3.4:99999"))
    assert p is None and why in ("bad_port", "unparsable")
    p, why = P.clean_proxy(P.parse_uri("vless://not-a-uuid@1.2.3.4:443"))
    assert p is None and why == "bad_uuid"
    p, why = P.clean_proxy(P.parse_uri("ss://:pw@1.2.3.4:80"))
    assert p is None


def test_clean_normalizes():
    p, _ = P.clean_proxy(P.parse_uri("socks://EXAMPLE.com:1080"))
    assert p["server"] == "example.com"


# ----------------------------------------------------------------- hash -----

def test_phash_stable_and_name_independent():
    a = P.parse_uri("ss://aes-256-gcm:pw@9.9.9.9:1234#NameOne")
    b = P.parse_uri("ss://aes-256-gcm:pw@9.9.9.9:1234#DifferentName")
    assert P.phash(a) == P.phash(b)
    c = P.parse_uri("ss://aes-256-gcm:other@9.9.9.9:1234")
    assert P.phash(a) != P.phash(c)


# --------------------------------------------------------------- roundtrip ---

def test_roundtrip_ss():
    u0 = "ss://aes-256-gcm:pass123@1.2.3.4:8388#n"
    p = P.parse_uri(u0)
    u1 = P.uri_from_proxy(p)
    q = P.parse_uri(u1)
    assert q["server"] == "1.2.3.4" and q["port"] == 8388
    assert q["method"] == "aes-256-gcm" and q["password"] == "pass123"


def test_roundtrip_vmess():
    p = P.parse_uri(_vmess_uri())
    u1 = P.uri_from_proxy(p)
    q = P.parse_uri(u1)
    for k in ("server", "port", "uuid", "network", "security", "host", "path"):
        assert q[k] == p[k], k


def test_roundtrip_trojan_vless_hy2_tuic():
    for u in ("trojan://pw@t.com:443?sni=t.com#x",
              "vless://11111111-2222-3333-4444-555555555555@v.com:443?security=tls&sni=v.com&type=ws&path=/p#x",
              "hysteria2://pw@h.com:8443?sni=h.com&insecure=1#x",
              "tuic://11111111-2222-3333-4444-555555555555:pw@t.com:8443?alpn=h3#x"):
        p = P.parse_uri(u)
        q = P.parse_uri(P.uri_from_proxy(p))
        assert q and q["server"] == p["server"] and q["port"] == p["port"]
        assert q["proto"] == p["proto"]


# --------------------------------------------------------------- engines -----

def test_primary_engine_routing():
    assert E.primary_engine(P.parse_uri("http://1.1.1.1:8080")) == "direct"
    assert E.primary_engine(
        P.parse_uri("hysteria2://pw@1.1.1.1:8443")) == "singbox"
    assert E.primary_engine(P.parse_uri(_vmess_uri(net="tcp"))) == "xray"
    assert E.primary_engine(P.parse_uri(_vmess_uri(net="h2"))) == "singbox"


def test_engine_supports_matrix():
    p = P.parse_uri(_vmess_uri(net="ws"))
    assert E.engine_supports("xray", p) and E.engine_supports("singbox", p)
    p = P.parse_uri(_vmess_uri(net="xhttp"))
    assert E.engine_supports("xray", p) and not E.engine_supports("singbox", p)


def test_build_xray_config_shape():
    p1 = P.parse_uri(_vmess_uri())
    p2 = P.parse_uri("trojan://pw@t.com:443?sni=t.com")
    cfg = E.build_xray_config([p1, p2], [30001, 30002])
    assert len(cfg["inbounds"]) == 2 and len(cfg["outbounds"]) == 3
    tags = {r["outboundTag"] for r in cfg["routing"]["rules"]}
    assert tags == {"p0", "p1"}
    assert cfg["outbounds"][0]["protocol"] == "vmess"
    assert cfg["outbounds"][0]["streamSettings"]["network"] == "ws"


def test_build_singbox_config_shape():
    p1 = P.parse_uri("hysteria2://pw@h.com:8443?sni=h.com&insecure=1")
    p2 = P.parse_uri(_vmess_uri())
    cfg = E.build_singbox_config([p1, p2], [31001, 31002])
    assert cfg["route"]["default_domain_resolver"]["server"] == "res0"
    types = {o["type"] for o in cfg["outbounds"]}
    assert {"hysteria2", "vmess", "direct"} <= types
    hy2 = next(o for o in cfg["outbounds"] if o["type"] == "hysteria2")
    assert hy2["tls"]["enabled"] and hy2["tls"]["insecure"]


def test_client_configs_valid_json():
    ps = [P.parse_uri(_vmess_uri()), P.parse_uri("trojan://pw@t.com:443")]
    sb = E.singbox_client_config(ps, ["a", "b"])
    assert sb["route"]["final"] == "\U0001F41F proxy"
    assert sb["outbounds"][0]["type"] == "selector"
    xr = E.xray_client_config(ps, ["a", "b"])
    assert any(o["protocol"] == "freedom" for o in xr["outbounds"])
    json.dumps(sb)
    json.dumps(xr)


# ---------------------------------------------------------------- tgparse ---

def test_extract_uris_plain():
    txt = ("check this out:\nvless://11111111-2222-3333-4444-555555555555@a.com:443"
           "?security=tls&type=tcp#one\nand ss://aes-256-gcm:pw@b.com:80")
    uris = T.extract_uris(txt)
    assert len(uris) == 2 and uris[0].startswith("vless://")


def test_extract_uris_base64_blob():
    inner = "ss://aes-256-gcm:pw@1.2.3.4:8388#x\ntrojan://pw@5.6.7.8:443#y"
    blob = base64.b64encode(inner.encode()).decode()
    uris = T.extract_uris(blob)
    assert len(uris) == 2


def test_channel_html():
    html = """
    <div class="tgme_widget_message_text js-message_text" dir="auto">
      new configs!<br><a href="vless://11111111-2222-3333-4444-555555555555@c.io:443?security=tls#cfg">
      vless link</a></div><time datetime="2026-09-28T10:00:00+00:00"></time>
    """
    uris, latest, subs = T.parse_channel_html(html)
    assert len(uris) == 1 and uris[0].startswith("vless://")
    assert latest and latest.startswith("2026-09-28")
    assert subs == []


def test_clash_yaml():
    yml = """
proxies:
  - name: "clashnode"
    type: ss
    server: 3.4.5.6
    port: 8388
    cipher: aes-256-gcm
    password: pw123
  - name: "tr"
    type: trojan
    server: t.example.com
    port: 443
    password: tpw
    sni: t.example.com
"""
    try:
        import yaml  # noqa: F401
    except ImportError:
        return  # regex fallback path can't do clash; skip when yaml absent
    ps = T.proxies_from_structured(yml)
    assert len(ps) == 2
    ss = [p for p in ps if p["proto"] == "ss"][0]
    assert ss["server"] == "3.4.5.6" and ss["method"] == "aes-256-gcm"


# ---------------------------------------------------------------- states ----

def test_source_states_retirement():
    path = os.path.join(tempfile.mkdtemp(), "sources.json")
    st = S.SourceStates(path)
    for i in range(S.RETIRE_FAIL_STREAK):
        st.record_fetch("deadsrc", ok=False, n_uris=0, new_hashes=[])
    assert "fetch failures" in st.retire_reason("deadsrc")
    st.refresh_retirements()
    assert st.s["deadsrc"]["retired"]
    assert "deadsrc" not in st.active_names()

    st2 = S.SourceStates(path)
    st2.record_fetch("good", True, 10, ["h1"], "url", "http://x")
    st2.record_fetch("good", True, 10, ["h1", "h2"], "url", "http://x")
    assert st2.s["good"]["total_new"] == 2
    assert st2.s["good"]["seen"] == ["h1", "h2"]


def test_registry_observe():
    r = S.Registry(os.path.join(tempfile.mkdtemp(), "known.json"))
    p = P.parse_uri("socks://7.7.7.7:1080")
    assert r.observe(p, "h1", "srcA") is True   # new
    assert r.observe(p, "h1", "srcB") is False  # known
    assert r.sources_of("h1") == ["srcA", "srcB"]


def test_alive_recall_roundtrip():
    path = os.path.join(tempfile.mkdtemp(), "alive_recall.json")
    p = P.parse_uri("socks://7.7.7.7:1080")
    results = [{"phash": "h1", "proxy": p, "alive": True, "latency_ms": 120,
                "exit_cc": "DE", "engine": "xray"},
               {"phash": "h2", "proxy": p, "alive": False}]
    pool = S.update_alive_recall(path, results)
    assert "h1" in pool and "h2" not in pool
    # expired entries get pruned
    pool2 = S.load_alive_recall(path)
    pool2["h1"]["alive"] = time.time() - (S.ALIVE_RECALL_DAYS + 1) * 86400
    S.save_json(path, pool2)
    pool3 = S.update_alive_recall(path, [])
    assert "h1" not in pool3


def test_jsonl_roundtrip():
    path = os.path.join(tempfile.mkdtemp(), "h.jsonl")
    S.append_jsonl(path, {"a": 1})
    S.append_jsonl(path, {"a": 2})
    rows = S.load_jsonl(path)
    assert [r["a"] for r in rows] == [1, 2]


# ----------------------------------------------------------------- misc -----

def test_flag_and_name():
    assert P.flag("DE") == "\U0001F1E9\U0001F1EA"
    assert P.flag("") == "\U0001F3F3"
    n = P.fmt_name(7, "US", "DE")
    assert n.startswith("#7") and "US" in n and "DE" in n
