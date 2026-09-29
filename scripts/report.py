#!/usr/bin/env python3
"""Stage 4: REPORT - render README.md as the living report, publish working
proxies as many separated subscription files, badges, and history.

Outputs:
  README.md                        the living report
  subs/all.txt                     ALL working proxies, ranked by speed
  subs/all.base64.txt              same, base64-encoded (classic sub format)
  subs/top150.txt                  top 150 ranked
  subs/top150.base64.txt           same, base64
  subs/by-proto/<proto>.txt        per-protocol working lists (+ .base64.txt)
  subs/by-engine/allxray.txt       verified through Xray core   (+ .base64.txt)
  subs/by-engine/allsingbox.txt    verified through sing-box     (+ .base64.txt)
  subs/by-engine/alldirect.txt     plain http/socks via curl     (+ .base64.txt)
  subs/by-country/<CC>.txt         per exit-country working lists (+ .base64.txt)
  subs/sing-box-client.json        ready-to-run sing-box client config (top 150)
  subs/xray-client.json            ready-to-run xray client config (top 150)
  badges/*.json                    shields.io endpoint badges
  data/history.jsonl               one line per run (appended)
  data/last_run.json               compact results kept in git (full -> logs/)
"""
import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.proxy import uri_from_proxy, fmt_name, flag  # noqa: E402
from lib import engines  # noqa: E402
from lib.geo import COUNTRIES  # noqa: E402
from lib.states import load_json, save_json, append_jsonl, load_jsonl  # noqa: E402

TOP_SUB = 150        # top-N ranked list (top150.txt + client configs)
TOP_TABLE = 25       # rows shown in README top table


def log(msg):
    print(f"[report] {msg}", flush=True)


def country(cc):
    return COUNTRIES.get(cc, cc or "unknown")


def cc_file(cc):
    """Safe filename for a country code."""
    if cc and len(cc) == 2 and cc.isalpha():
        return cc.upper()
    return "unknown"


def median(vals):
    if not vals:
        return None
    s = sorted(vals)
    return s[len(s) // 2]


def pct90(vals):
    if not vals:
        return None
    s = sorted(vals)
    return s[min(len(s) - 1, int(round(0.9 * (len(s) - 1))))]


def clean_txt(d):
    """Remove stale generated .txt files from a directory."""
    if not os.path.isdir(d):
        return
    for fn in os.listdir(d):
        if fn.endswith(".txt"):
            try:
                os.unlink(os.path.join(d, fn))
            except OSError:
                pass


def write_list(path, uris, also_base64=True):
    """Write a plain URI list; optionally a sibling .base64.txt."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(uris) + ("\n" if uris else ""))
    if also_base64:
        b = base64.b64encode("\n".join(uris).encode()).decode()
        with open(path[:-len(".txt")] + ".base64.txt", "w", encoding="utf-8") as f:
            f.write(b + ("\n" if b else ""))


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(root, "data")
    state_dir = os.path.join(root, "state")
    subs_dir = os.path.join(root, "subs")
    badges_dir = os.path.join(root, "badges")
    logs_dir = os.path.join(root, "logs")
    subdirs = [os.path.join(subs_dir, s) for s in
               ("by-proto", "by-engine", "by-country")]
    for d in [subs_dir, badges_dir, logs_dir] + subdirs:
        os.makedirs(d, exist_ok=True)

    cstats = load_json(os.path.join(data_dir, "collect_stats.json"), {})
    tstats = load_json(os.path.join(data_dir, "test_stats.json"), {})
    results = load_json(os.path.join(data_dir, "results.json"), [])
    plan = {p["phash"]: p for p in load_json(os.path.join(data_dir, "test_plan.json"), [])}
    sources = load_json(os.path.join(state_dir, "sources.json"), {})
    now = time.time()

    # ------------------------------------------------ rank working proxies --
    working = [r for r in results if r.get("work")]
    working.sort(key=lambda r: (-(r.get("speed_kbps") or 0),
                                r.get("latency_ms") or 9999))
    for i, r in enumerate(working, 1):
        r["rank"] = i

    # name every working proxy once, keep (result, uri) pairs
    pairs = []
    for r in working:
        p = plan.get(r["phash"])
        if not p:
            continue
        u = uri_from_proxy(p, name=fmt_name(r["rank"], r.get("cc", ""),
                                            r.get("exit_cc", "")))
        if u:
            pairs.append((r, u))
    log(f"{len(pairs)} working proxies to publish")

    # ------------------------------------------------------ subscriptions --
    # stale generated files from previous runs must not linger
    for d in subdirs:
        clean_txt(d)
    for legacy in ("base64.txt",):   # renamed -> all.base64.txt
        try:
            os.unlink(os.path.join(subs_dir, legacy))
        except OSError:
            pass

    write_list(os.path.join(subs_dir, "all.txt"), [u for _, u in pairs])
    write_list(os.path.join(subs_dir, "top150.txt"), [u for _, u in pairs[:TOP_SUB]])

    by_proto, by_engine, by_country = {}, {}, {}
    for r, u in pairs:
        by_proto.setdefault(r["proto"], []).append(u)
        eng = r.get("engine") or "direct"
        by_engine.setdefault(eng, []).append(u)
        by_country.setdefault(cc_file(r.get("exit_cc")), []).append(u)

    for proto, lst in by_proto.items():
        write_list(os.path.join(subs_dir, "by-proto", f"{proto}.txt"), lst)
    eng_files = {"xray": "allxray.txt", "singbox": "allsingbox.txt",
                 "direct": "alldirect.txt"}
    for eng, lst in by_engine.items():
        write_list(os.path.join(subs_dir, "by-engine",
                                eng_files.get(eng, f"{eng}.txt")), lst)
    for cc, lst in by_country.items():
        write_list(os.path.join(subs_dir, "by-country", f"{cc_file(cc)}.txt"), lst)

    top_pairs = pairs[:TOP_SUB]
    top_proxies = [plan[r["phash"]] for r, _ in top_pairs if r["phash"] in plan]
    tags = [fmt_name(r["rank"], r.get("cc", ""), r.get("exit_cc", ""))
            for r, _ in top_pairs if r["phash"] in plan]
    if top_proxies:
        sb_cfg = engines.singbox_client_config(top_proxies, tags)
        with open(os.path.join(subs_dir, "sing-box-client.json"), "w",
                  encoding="utf-8") as f:
            json.dump(sb_cfg, f, ensure_ascii=False, indent=1)
        xr_cfg = engines.xray_client_config(top_proxies, tags)
        with open(os.path.join(subs_dir, "xray-client.json"), "w",
                  encoding="utf-8") as f:
            json.dump(xr_cfg, f, ensure_ascii=False, indent=1)
    log(f"subscriptions: all={len(pairs)} top{TOP_SUB}={len(top_pairs)} "
        f"protos={len(by_proto)} engines={len(by_engine)} countries={len(by_country)}")

    # ------------------------------------------------------------- badges --
    def badge(name, label, message, color):
        save_json(os.path.join(badges_dir, name + ".json"),
                  {"schemaVersion": 1, "label": label, "message": str(message),
                   "color": color})

    avg = tstats.get("avg_speed_kbps") or 0
    mx = tstats.get("max_speed_kbps") or 0
    badge("working", "working", f"{len(working)}/{tstats.get('tested', 0)}",
          "brightgreen" if len(working) > 50 else ("green" if working else "red"))
    badge("alive", "alive (204 OK)", tstats.get("alive", 0), "blue")
    badge("speed", "avg speed", f"{avg/1000:.1f} Mbps" if avg else "n/a",
          "blueviolet")
    badge("max-speed", "max speed", f"{mx/1000:.1f} Mbps" if mx else "n/a",
          "purple")
    badge("countries", "exit countries", len(by_country), "teal")
    badge("sources", "sources",
          f"{cstats.get('url_ok', 0)}+{cstats.get('tg_ok', 0)} ok",
          "informational")
    badge("updated", "updated", time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(now)),
          "lightgrey")

    # ------------------------------------------------------------ history --
    hist_path = os.path.join(data_dir, "history.jsonl")
    entry = {
        "ts": int(now), "date": time.strftime("%Y-%m-%d %H:%M", time.gmtime(now)),
        "tested": tstats.get("tested", 0), "alive": tstats.get("alive", 0),
        "working": len(working), "unique": cstats.get("unique_proxies", 0),
        "avg_kbps": avg, "max_kbps": mx,
        "duration_s": tstats.get("duration_s", 0),
    }
    hist = load_jsonl(hist_path)
    if not hist or hist[-1].get("date") != entry["date"]:
        append_jsonl(hist_path, entry)
        hist.append(entry)
    hist = hist[-30:]

    def spark(vals, lo=None, hi=None):
        if not vals:
            return ""
        lo = lo if lo is not None else min(vals)
        hi = hi if hi is not None else max(vals)
        rng = (hi - lo) or 1
        blocks = "▁▂▃▄▅▆▇█"
        return "".join(blocks[min(7, int((v - lo) * 8 / rng))] for v in vals)

    # ------------------------------------------------------ README data ----
    tested = tstats.get("tested", 0)
    alive_n = tstats.get("alive", 0)
    leaks = alive_n - len(working)
    proto_rows = proto_distribution(results)
    cc_rows = exit_country_distribution(working)
    src_rows = source_rows(sources)
    eng_counts = {"xray": 0, "singbox": 0, "direct": 0}
    for r, _ in pairs:
        eng_counts[r.get("engine") or "direct"] = \
            eng_counts.get(r.get("engine") or "direct", 0) + 1
    lats = [r["latency_ms"] for r in working if r.get("latency_ms")]
    med_lat, p90_lat = median(lats), pct90(lats)
    speeds = [(r.get("speed_kbps") or 0) for r in working]
    tiers = [
        (">= 5 Mbps", sum(1 for s in speeds if s >= 5000)),
        ("1 - 5 Mbps", sum(1 for s in speeds if 1000 <= s < 5000)),
        ("0.25 - 1 Mbps", sum(1 for s in speeds if 250 <= s < 1000)),
        ("< 0.25 Mbps", sum(1 for s in speeds if 0 < s < 250)),
        ("unmeasured", sum(1 for s in speeds if s <= 0)),
    ]

    # ---------------------------------------------------------- README.md --
    L = []
    A = L.append
    A("# Free Proxy Scanner")
    A("")
    A("> **Really tested** free proxy aggregator. Every proxy below was fetched from "
      "public sources, tunneled through with Xray/sing-box, and verified to actually "
      "change your egress IP. No CSV-validation theater, no blind relisting.")
    A("")
    A(f"![working](badges/working.json) ![alive](badges/alive.json) "
      f"![speed](badges/speed.json) ![max-speed](badges/max-speed.json) "
      f"![countries](badges/countries.json) ![sources](badges/sources.json) "
      f"![updated](badges/updated.json)")
    A("")

    A("## What this is")
    A("")
    A(f"A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy "
      f"configs from **{cstats.get('url_sources_total', 0)} URL subscriptions** and "
      f"**{cstats.get('tg_channels_total', 0)} Telegram channels**, parses 9 protocols "
      f"(vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), "
      f"deduplicates them, and **actually connects through every single one** to "
      f"separate working proxies from dead ones.")
    A("")
    A(f"Latest run: **{cstats.get('ts_iso', '?')}** — "
      f"{cstats.get('unique_proxies', 0)} unique proxies collected from "
      f"{cstats.get('url_ok', 0)}/{cstats.get('url_sources_active', 0)} URL sources and "
      f"{cstats.get('tg_ok', 0)}/{cstats.get('tg_channels_active', 0)} Telegram channels; "
      f"**{tested}** endpoints really tested, **{alive_n}** reachable, "
      f"**{len(working)}** verified working (egress IP confirmed changed) across "
      f"**{len(cc_rows)} exit countries**.")
    A("")

    A("## How the testing works (the *really* part)")
    A("")
    A("```mermaid")
    A("flowchart LR")
    A("  S1[URL subs<br/>+ Telegram] --> F[fetch &<br/>parse]")
    A("  F --> C[clean &<br/>dedupe]")
    A("  C --> T1[phase 1<br/>connectivity<br/>gstatic 204]")
    A("  T1 -->|reachable| T2[phase 2<br/>exit IP check<br/>ip-api]")
    A("  T1 -->|dead| X[drop]")
    A("  T2 -->|egress changed| T3[1 MB speed<br/>test]")
    A("  T2 -->|same IP| X2[mark leak]")
    A("  T3 --> R[README + subs<br/>+ badges]")
    A("```")
    A("")
    A("1. **Phase 1 — connectivity.** Each proxy is loaded as an outbound into a real "
      "Xray or sing-box instance (or used directly via `curl -x` for plain http/socks). "
      "An HTTPS request to `gstatic.com/generate_204` goes through the tunnel with "
      "**DNS resolved on the proxy side**. Only an HTTP 204 counts as reachable.")
    A("2. **Phase 2 — egress verification.** An ip-api request through the same tunnel "
      "must return an exit IP **different from the runner's own IP**, plus its country "
      "and AS. Proxies that pass phase 1 but keep your IP are marked as leaks and "
      "excluded from the working list. Server country vs exit country mismatches are "
      "flagged in the tables.")
    A("3. **Throughput.** Working proxies download 1 MB from `speed.cloudflare.com` "
      "through the tunnel; the measured rate is the speed you see in the tables.")
    A("4. **Engine fallback.** If a proxy fails on Xray, it is retried on sing-box "
      "(and vice versa) before being declared dead — some configs only work on one core.")
    A("")

    A("## Top working proxies")
    A("")
    A(f"All {len(working)} working proxies are published in "
      f"[`subs/all.txt`](subs/all.txt); this table shows the top "
      f"{min(TOP_TABLE, len(working))}.")
    A("")
    A("| # | proxy | proto | server | exit | latency | speed | engine |")
    A("|---|-------|-------|--------|------|---------|-------|--------|")
    for r in working[:TOP_TABLE]:
        lat = f"{r['latency_ms']} ms" if r.get("latency_ms") is not None else "-"
        spd = f"{r['speed_kbps']/1000:.1f} Mbps" if r.get("speed_kbps") else "-"
        A(f"| {r['rank']} | {fmt_name(r['rank'], r.get('cc'), r.get('exit_cc'))} "
          f"| `{r['proto']}` | `{r['server']}:{r['port']}` "
          f"| {country(r.get('exit_cc'))} | {lat} | {spd} | {r.get('engine') or '-'} |")
    A("")

    A("## Exit locations — which countries work")
    A("")
    A("Every working proxy, grouped by the country of its **verified exit IP** "
      "(phase 2), with a dedicated subscription file per country. "
      f"Currently {len(cc_rows)} countries have at least one working exit.")
    A("")
    A("| country | working | avg speed | best latency | share | list |")
    A("|---------|--------:|----------:|-------------:|------:|------|")
    for cc, n, avgc, best_lat in cc_rows:
        fn = cc_file(cc)
        spd = f"{avgc/1000:.1f} Mbps" if avgc else "-"
        bl = f"{best_lat} ms" if best_lat is not None else "-"
        share = f"{100 * n / len(working):.0f}%" if working else "-"
        A(f"| {flag(cc)} {country(cc)} | {n} | {spd} | {bl} | {share} "
          f"| [`{fn}.txt`](subs/by-country/{fn}.txt) |")
    A("")
    A("A `??` exit means the geo lookup could not resolve the exit IP. "
      "Base64 variants of every country file sit next to them as "
      "`<CC>.base64.txt`.")
    A("")

    A("## Protocol distribution")
    A("")
    A("| protocol | tested | alive | working | alive rate |")
    A("|----------|-------:|------:|--------:|-----------:|")
    for proto, t, a, w in proto_rows:
        rate = f"{100 * a / t:.0f}%" if t else "-"
        A(f"| `{proto}` | {t} | {a} | {w} | {rate} |")
    A("")
    A("Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) "
      "(one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).")
    A("")

    A("## Engine breakdown")
    A("")
    A("Which core verified each working proxy. The engine fallback means a proxy "
      "that failed on its primary core got a second chance on the other one.")
    A("")
    A("| engine | working | note |")
    A("|--------|--------:|------|")
    A(f"| Xray-core | {eng_counts.get('xray', 0)} | "
      f"[`allxray.txt`](subs/by-engine/allxray.txt) |")
    A(f"| sing-box | {eng_counts.get('singbox', 0)} | "
      f"[`allsingbox.txt`](subs/by-engine/allsingbox.txt) |")
    A(f"| direct (curl) | {eng_counts.get('direct', 0)} | plain http/socks, "
      f"[`alldirect.txt`](subs/by-engine/alldirect.txt) |")
    A("")

    A("## Speed & latency profile")
    A("")
    A("| speed tier | proxies |")
    A("|-----------|--------:|")
    for label, n in tiers:
        A(f"| {label} | {n} |")
    A("")
    A(f"Latency (phase-1 HTTPS round trip): median **{med_lat if med_lat is not None else '-'} ms**, "
      f"p90 **{p90_lat if p90_lat is not None else '-'} ms**. "
      f"{leaks} proxies passed connectivity but failed egress verification "
      "(leaked the runner IP or broke on the exit check) and are excluded.")
    A("")

    A("## Source health")
    A("")
    retired = [s for s, e in sources.items() if e.get("retired")]
    A(f"{len(sources) - len(retired)} active, {len(retired)} auto-retired "
      f"(10 fetch failures / 10 all-dead runs / 10 days without anything new). "
      f"Best contributors this run:")
    A("")
    A("| source | kind | tested | alive | new this run |")
    A("|--------|------|-------:|------:|-------------:|")
    for name, kind, t, a, new in src_rows:
        A(f"| `{name}` | {kind} | {t} | {a} | {new} |")
    A("")

    A("## History")
    A("")
    A(f"working per run (last {len(hist)}): {spark([h.get('working', 0) for h in hist], 0, None)}")
    A("")
    A("| date (UTC) | tested | alive | working | avg | max |")
    A("|------------|-------:|------:|--------:|----:|----:|")
    for h in reversed(hist[-15:]):
        avg_h = f"{h.get('avg_kbps', 0)/1000:.1f}M" if h.get("avg_kbps") else "-"
        mx_h = f"{h.get('max_kbps', 0)/1000:.1f}M" if h.get("max_kbps") else "-"
        A(f"| {h.get('date', '?')} | {h.get('tested', 0)} | {h.get('alive', 0)} "
          f"| {h.get('working', 0)} | {avg_h} | {mx_h} |")
    A("")

    A("## Subscription files")
    A("")
    A("Everything under [`subs/`](subs/) is regenerated every run. "
      "Plain lists are one proxy URI per line; `.base64.txt` variants are the "
      "same list base64-encoded for clients that need the classic sub format.")
    A("")
    A("| file | contents | direct subscription URL |")
    A("|------|----------|--------------------------|")
    A(f"| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed "
      f"({len(pairs)}) | `{raw_url('subs/all.txt')}` |")
    A(f"| [`all.base64.txt`](subs/all.base64.txt) | same, base64 "
      f"| `{raw_url('subs/all.base64.txt')}` |")
    A(f"| [`top150.txt`](subs/top150.txt) | top {TOP_SUB} ranked "
      f"({min(TOP_SUB, len(pairs))}) | `{raw_url('subs/top150.txt')}` |")
    A(f"| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 "
      f"| `{raw_url('subs/top150.base64.txt')}` |")
    A(f"| [`by-proto/`](subs/by-proto/) | one list per protocol "
      f"({len(by_proto)} protocols) | ...`/subs/by-proto/<proto>.txt` |")
    A(f"| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray "
      f"({eng_counts.get('xray', 0)}) | `{raw_url('subs/by-engine/allxray.txt')}` |")
    A(f"| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on "
      f"sing-box ({eng_counts.get('singbox', 0)}) | "
      f"`{raw_url('subs/by-engine/allsingbox.txt')}` |")
    A(f"| [`by-country/`](subs/by-country/) | one list per exit country "
      f"({len(by_country)} countries, e.g. "
      f"[`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) "
      f"| ...`/subs/by-country/<CC>.txt` |")
    A(f"| [`sing-box-client.json`](subs/sing-box-client.json) | top {TOP_SUB} as a "
      f"ready-to-run sing-box client config | `{raw_url('subs/sing-box-client.json')}` |")
    A(f"| [`xray-client.json`](subs/xray-client.json) | top {TOP_SUB} as a "
      f"ready-to-run xray client config | `{raw_url('subs/xray-client.json')}` |")
    A(f"| [`archive/`](archive/) | gz snapshot of every collection (30 kept) | — |")
    A("")

    A("## Use the proxies")
    A("")
    A("- **v2rayN / v2rayNG / Nekobox / Hiddify / Shadowrocket**: add subscription "
      f"`{raw_url('subs/all.base64.txt')}` (everything working) or "
      f"`{raw_url('subs/top150.base64.txt')}` (curated top 150).")
    A("- **Want a specific country?** Grab `subs/by-country/<CC>.txt` (see the "
      "Exit locations table above) — e.g. "
      f"`{raw_url('subs/by-country/US.txt')}`, "
      f"`{raw_url('subs/by-country/DE.txt')}`.")
    A("- **Only one protocol?** `subs/by-proto/<proto>.txt` — e.g. "
      f"`{raw_url('subs/by-proto/vless.txt')}`, "
      f"`{raw_url('subs/by-proto/hysteria2.txt')}`.")
    A("- **sing-box**: download [`subs/sing-box-client.json`]"
      "(subs/sing-box-client.json) and run `sing-box run -c sing-box-client.json` "
      "— it listens on `127.0.0.1:2080` (mixed) with a selector + auto urltest group.")
    A("- **Xray**: download [`subs/xray-client.json`](subs/xray-client.json), "
      "socks inbound on `127.0.0.1:2080`.")
    A("- Raw snapshots of every collection: [`archive/`](archive/) (30 kept).")
    A("")

    A("## Repository layout")
    A("")
    A("```")
    A("sources/            url_subs.yml + telegram.yml (scannable source lists)")
    A("scripts/            collect.py, test.py, report.py + lib/")
    A("state/              source health, alive-recall pool, geo cache (committed)")
    A("data/               stats, history, compact last-run results")
    A("subs/               THE PRODUCT: verified working proxies, split by")
    A("                    proto / engine / exit country + all + top150 lists")
    A("badges/             shields.io endpoint badges")
    A("archive/            gz snapshots of every collection")
    A("```")
    A("")

    A("## Why most \"free proxy lists\" lie")
    A("")
    A("The typical aggregator relists whatever it scraped, so 80-95% of entries are "
    "dead within hours"
    + (f" — this run found **{100 * (tested - alive_n) / tested:.0f}% unreachable** "
       f"and **{100 * (tested - len(working)) / tested:.0f}% unusable** overall."
       if tested else ".")
    + " Only tunnels that completed a real HTTPS handshake, returned a verifiable "
      "foreign exit IP, and pushed a 1 MB download are counted as working here.")
    A("")

    A("## Disclaimers")
    A("")
    A("- Free proxies are **public and untrusted**. Anything you send through them "
      "can be observed or modified by their operators. Never use them for "
      "authentication, payments, or anything sensitive.")
    A("- All configs are collected from publicly posted sources (GitHub "
      "subscriptions and public Telegram channels); no credentials are guessed or "
      "brute-forced. Removal requests: open an issue.")
    A("- Availability is transient: the working list is re-verified every 6 hours, "
      "and past performance never guarantees future availability.")
    A("")

    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    log("README.md written")

    # ------------------------------------------------- compact + cleanup ----
    # keep a compact, git-friendly copy of the alive subset
    compact = [{k: r.get(k) for k in
                ("phash", "rank", "proto", "server", "port", "cc", "exit_cc",
                 "exit_as", "latency_ms", "speed_kbps", "engine", "alive", "work")}
               for r in results if r.get("alive")]
    save_json(os.path.join(data_dir, "last_run.json"), {
        "ts": now, "ts_iso": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now)),
        "collect": cstats, "test": {k: v for k, v in tstats.items() if k != "errors"},
        "alive": compact})
    # full results move to logs/ (gitignored, but uploaded as artifact)
    try:
        os.replace(os.path.join(data_dir, "results.json"),
                   os.path.join(logs_dir, "results.json"))
    except OSError:
        pass

    # GitHub Actions step summary
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write("\n## Free Proxy Scanner — run report\n\n"
                    f"- collected: **{cstats.get('unique_proxies', 0)}** unique "
                    f"({cstats.get('url_ok', 0)} url + {cstats.get('tg_ok', 0)} tg sources ok)\n"
                    f"- tested: **{tested}** endpoints (real tunnels)\n"
                    f"- alive: **{alive_n}** | verified working: **{len(working)}** "
                    f"across **{len(cc_rows)}** exit countries\n"
                    f"- avg speed: **{avg/1000:.1f} Mbps**, max: **{mx/1000:.1f} Mbps**\n"
                    f"- files: all={len(pairs)}, by-proto={len(by_proto)}, "
                    f"by-country={len(by_country)}, by-engine={len(by_engine)}\n"
                    f"- duration: {tstats.get('duration_s', 0)}s test + "
                    f"top errors: {tstats.get('errors', {})}\n")
    log("done")


def raw_url(path):
    repo = os.environ.get("GH_REPO", "G1010yzd10/proxy-scanner")
    return f"https://raw.githubusercontent.com/{repo}/main/{path}"


def proto_distribution(results):
    agg = {}
    for r in results:
        d = agg.setdefault(r["proto"], [0, 0, 0])
        d[0] += 1
        d[1] += 1 if r.get("alive") else 0
        d[2] += 1 if r.get("work") else 0
    return sorted(((k, *v) for k, v in agg.items()), key=lambda x: -x[3])


def exit_country_distribution(working):
    """(cc, count, avg_speed, best_latency) for every exit country."""
    agg = {}
    for r in working:
        cc = r.get("exit_cc") or "??"
        d = agg.setdefault(cc, {"n": 0, "sp": [], "lat": []})
        d["n"] += 1
        if r.get("speed_kbps"):
            d["sp"].append(r["speed_kbps"])
        if r.get("latency_ms") is not None:
            d["lat"].append(r["latency_ms"])
    rows = [(cc, d["n"], int(sum(d["sp"]) / len(d["sp"])) if d["sp"] else 0,
             min(d["lat"]) if d["lat"] else None)
            for cc, d in agg.items()]
    return sorted(rows, key=lambda x: -x[1])


def source_rows(sources, n=20):
    rows = []
    for name, e in sources.items():
        if e.get("retired"):
            continue
        rows.append((name, e.get("kind", "?"), e.get("tested", 0),
                     e.get("alive", 0), e.get("new", 0)))
    rows.sort(key=lambda r: (-r[3], -r[4]))
    return rows[:n]


if __name__ == "__main__":
    main()
