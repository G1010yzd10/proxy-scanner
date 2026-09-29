#!/usr/bin/env python3
"""Stage 1-2: COLLECT - fetch every source (URL subscriptions + Telegram public
channels), extract proxy URIs, parse, clean, deduplicate, log, archive.

Outputs:
  state/known.json        job-local registry (phash -> proxy + sources)
  state/sources.json      per-source health update (new counts, failures)
  data/test_plan.json     candidate proxies for the tester (deduped by endpoint)
  data/raw/last_collect.jsonl  one fetch-log line per source
  archive/collected_<ts>.txt.gz   gz snapshot of the unique URI list
  data/collect_stats.json quick numbers for the README
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.proxy import parse_uri, clean_proxy, phash, uri_from_proxy  # noqa: E402
from lib.tgparse import extract_uris, proxies_from_structured, parse_channel_html  # noqa: E402
from lib.states import SourceStates, Registry, load_json, save_json, append_jsonl  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
FETCH_TIMEOUT = 25
FETCH_WORKERS = 16
TG_WORKERS = 8
MAX_BODY = 24 * 1024 * 1024
IPPORT_RE = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3}):(\d{2,5})$')
ARCHIVE_KEEP = 30          # gz snapshots retained
MIN_UNIQUE = 200           # hard guard: run fails below this
CANDIDATE_CAP = 4500       # max endpoints offered to the tester
RECALL_EXTRA = 600         # extra revived-recall endpoints beyond the cap


def log(msg):
    print(f"[collect] {msg}", flush=True)


def http_get(url, timeout=FETCH_TIMEOUT):
    """GET with browser-ish UA. Returns (status, text) - status 0 on exception."""
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read(MAX_BODY)
        return r.status, body.decode("utf-8", "replace")


# ----------------------------------------------------------------- parse ----

def parse_source_body(text, fmt, default_scheme):
    """Extract internal proxy dicts from a source body."""
    proxies = []
    if fmt:
        proxies.extend(proxies_from_structured(text, fmt=fmt))
    uris = extract_uris(text)
    if default_scheme:
        for line in text.splitlines():
            m = IPPORT_RE.match(line.strip())
            if m:
                uris.append(f"{default_scheme}://{m.group(1)}:{m.group(2)}")
    for u in uris:
        p = parse_uri(u)
        if p:
            proxies.append(p)
    return proxies


def parse_telegram_html(html_text):
    uris, latest, sub_urls = parse_channel_html(html_text)
    proxies = [parse_uri(u) for u in uris]
    proxies = [p for p in proxies if p]
    return proxies, latest, sub_urls


# ------------------------------------------------------------------ main ----

def load_yaml_sources(path):
    """Minimal loader for our flat sources yml (no pyyaml dependency needed)."""
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return (yaml.safe_load(f) or {}).get("sources") or []
    except ImportError:
        out = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(
                    r'name\s*:\s*([A-Za-z0-9_\-]+)\s*,\s*url\s*:\s*"([^"]+)"'
                    r'(?:.*?default_scheme\s*:\s*([a-z0-9]+))?', line)
                if line.strip().startswith("- {") and m:
                    out.append({"name": m.group(1), "url": m.group(2),
                                "default_scheme": m.group(3)})
        return out


def load_yaml_channels(path):
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return (yaml.safe_load(f) or {}).get("channels") or []
    except ImportError:
        out = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r'name\s*:\s*([A-Za-z0-9_\-]+)\s*,\s*category\s*:\s*([a-z\-]+)', line)
                if line.strip().startswith("- {") and m:
                    out.append({"name": m.group(1), "category": m.group(2)})
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--min-unique", type=int, default=MIN_UNIQUE)
    args = ap.parse_args()
    root = args.root
    state_dir = os.path.join(root, "state")
    data_dir = os.path.join(root, "data")
    os.makedirs(state_dir, exist_ok=True)
    os.makedirs(os.path.join(data_dir, "raw"), exist_ok=True)

    now = time.time()
    states = SourceStates(os.path.join(state_dir, "sources.json"))
    registry = Registry(os.path.join(state_dir, "known.json"))
    states.refresh_retirements()

    srcs = load_yaml_sources(os.path.join(root, "sources", "url_subs.yml"))
    chans = load_yaml_channels(os.path.join(root, "sources", "telegram.yml"))
    active = [s for s in srcs if not states.s.get(s["name"], {}).get("retired")]
    active_ch = [c for c in chans if not states.s.get("TG:" + c["name"], {}).get("retired")]
    log(f"sources: {len(active)}/{len(srcs)} url subs active, "
        f"{len(active_ch)}/{len(chans)} telegram channels active "
        f"({len(srcs) + len(chans) - len(active) - len(active_ch)} retired)")

    results = []
    new_by_source = {}

    def work(src):
        name, url = src["name"], src["url"]
        fmt, ds = src.get("format"), src.get("default_scheme")
        status, text, err = 0, "", ""
        for attempt in (1, 2):
            try:
                status, text = http_get(url)
                break
            except Exception as e:
                err = str(e)[:120]
                if attempt == 2:
                    break
                time.sleep(1.5)
        if status != 200 or not text:
            states.record_fetch(name, False, 0, [], "url", url)
            return {"name": name, "kind": "url", "url": url, "ok": False,
                    "status": status, "err": err, "ts": now}
        proxies = parse_source_body(text, fmt, ds)
        cleaned = []
        for p in proxies:
            p2, _ = clean_proxy(p)
            if p2:
                cleaned.append(p2)
        hashes = [phash(p) for p in cleaned]
        is_new = []
        for p, h in zip(cleaned, hashes):
            if registry.observe(p, h, name, now):
                is_new.append(h)
        states.record_fetch(name, True, len(cleaned), is_new, "url", url)
        new_by_source[name] = is_new
        sha = hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:16]
        return {"name": name, "kind": "url", "url": url, "ok": True, "status": status,
                "bytes": len(text), "sha256": sha, "uris": len(cleaned),
                "new": len(is_new), "ts": now}

    def work_tg(ch):
        cname, cat = "TG:" + ch["name"], ch.get("category", "misc")
        url = f"https://t.me/s/{ch['name']}"
        status, text, err = 0, "", ""
        try:
            status, text = http_get(url)
        except Exception as e:
            err = str(e)[:120]
        if status != 200 or not text or "tgme_widget_message" not in text:
            states.record_fetch(cname, False, 0, [], "tg", url)
            return {"name": ch["name"], "kind": "tg", "category": cat, "url": url,
                    "ok": False, "status": status, "err": err or "no preview", "ts": now}
        proxies, latest, sub_urls = parse_telegram_html(text)
        cleaned = []
        for p in proxies:
            p2, _ = clean_proxy(p)
            if p2:
                cleaned.append(p2)
        is_new = []
        for p in cleaned:
            h = phash(p)
            if registry.observe(p, h, cname, now):
                is_new.append(h)
        # candidate sub-urls found in channel -> fetch them too (depth 1)
        extra = 0
        for su in sub_urls[:4]:
            try:
                st2, t2 = http_get(su)
                if st2 == 200 and t2:
                    for p in parse_source_body(t2, None, None):
                        p2, _ = clean_proxy(p)
                        if p2:
                            extra += 1
                            h = phash(p2)
                            if registry.observe(p2, h, cname, now):
                                is_new.append(h)
            except Exception:
                pass
        states.record_fetch(cname, True, len(cleaned) + extra, is_new, "tg", url)
        new_by_source[cname] = is_new
        return {"name": ch["name"], "kind": "tg", "category": cat, "url": url,
                "ok": True, "status": status, "bytes": len(text),
                "uris": len(cleaned) + extra, "new": len(is_new),
                "latest_post": latest, "ts": now}

    with ThreadPoolExecutor(max_workers=FETCH_WORKERS) as ex:
        results = list(ex.map(work, active))
    with ThreadPoolExecutor(max_workers=TG_WORKERS) as ex:
        results += list(ex.map(work_tg, active_ch))

    # ---------------------------------------------------------- summaries ---
    ok_urls = [r for r in results if r["kind"] == "url"]
    ok_tgs = [r for r in results if r["kind"] == "tg"]
    uniq = len(registry.m)
    log(f"fetched ok: {len(ok_urls)}/{len(active)} url, {len(ok_tgs)}/{len(active_ch)} tg; "
        f"clean unique proxies in registry: {uniq}")

    if uniq < args.min_unique:
        log(f"FATAL: only {uniq} unique proxies (< {args.min_unique}); aborting")
        states.save()
        registry.save()
        sys.exit(2)

    # ------------------------------------------------- test plan (dedupe) ---
    # one candidate per (server, port); prefer configs seen in more sources,
    # then recently-alive recall entries, then newest.
    recall = load_json(os.path.join(state_dir, "alive_recall.json"), {})
    recall_keys = set(recall)

    def cand_key(h):
        e = registry.m[h]
        p = e["p"]
        recall_bonus = 1 if h in recall_keys else 0
        return (recall_bonus, len(e["srcs"]), e["last"])

    by_endpoint = {}
    for h, e in registry.m.items():
        p = e["p"]
        ep = (p["server"], p["port"])
        if ep not in by_endpoint or cand_key(h) > cand_key(by_endpoint[ep]):
            by_endpoint[ep] = h
    ranked = sorted(by_endpoint.values(), key=cand_key, reverse=True)
    plan_hashes = ranked[:CANDIDATE_CAP]
    plan = []
    for h in plan_hashes:
        e = registry.m[h]
        p = dict(e["p"])
        p["phash"] = h
        p["nsrc"] = len(e["srcs"])
        p["srcs"] = e["srcs"][:8]
        plan.append(p)

    # add recall entries whose endpoint vanished from current lists
    have_eps = {(p["server"], p["port"]) for p in plan}
    for h, e in recall.items():
        p = e.get("p") or {}
        if (p.get("server"), p.get("port")) in have_eps:
            continue
        if len(plan) >= CANDIDATE_CAP + RECALL_EXTRA:
            break
        q = dict(p)
        q["phash"] = h
        q["nsrc"] = 0
        q["srcs"] = []
        q["recall"] = True
        plan.append(q)

    save_json(os.path.join(data_dir, "test_plan.json"), plan)
    log(f"test plan: {len(plan)} endpoints "
        f"({len(plan_hashes)} current + {len(plan) - len(plan_hashes)} revived)")

    # ---------------------------------------------------------- archive -----
    arc_dir = os.path.join(root, "archive")
    os.makedirs(arc_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(now))
    lines = sorted(uri_from_proxy(e["p"]) or "" for e in registry.m.values())
    arc_path = os.path.join(arc_dir, f"collected_{stamp}.txt.gz")
    with gzip.open(arc_path, "wt", encoding="utf-8") as f:
        f.write("\n".join(lines))
    old = sorted(x for x in os.listdir(arc_dir) if x.startswith("collected_"))
    for x in old[:-ARCHIVE_KEEP]:
        try:
            os.remove(os.path.join(arc_dir, x))
        except OSError:
            pass

    # ------------------------------------------------------------- outputs --
    with open(os.path.join(data_dir, "raw", "last_collect.jsonl"), "w", encoding="utf-8") as f:
        for r in sorted(results, key=lambda r: (r["kind"], r["name"])):
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")

    stats = {
        "ts": now, "ts_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now)),
        "url_sources_active": len(active), "url_sources_total": len(srcs),
        "tg_channels_active": len(active_ch), "tg_channels_total": len(chans),
        "url_ok": len(ok_urls), "tg_ok": len(ok_tgs),
        "unique_proxies": uniq, "endpoints": len(by_endpoint),
        "uris_parsed": sum(r.get("uris", 0) for r in results),
        "plan_size": len(plan), "archive": os.path.basename(arc_path),
    }
    save_json(os.path.join(data_dir, "collect_stats.json"), stats)
    states.save()
    registry.save()
    log(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
