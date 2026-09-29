# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy listed by this pipeline is
> fetched from public sources, tunneled through with real Xray / sing-box cores,
> and verified to actually change your egress IP. No CSV-validation theater,
> no blind relisting.

🚀 **This repository just bootstrapped — the first Actions run is building the
live report right now. Reload this page in ~30–50 minutes to see the first
verified results.**

## What this is

A GitHub Actions pipeline (runs every 6 hours) that:

1. **Collects** free proxy configs from **~180 URL subscriptions** and **~90
   Telegram channels** — 9 protocols: `vless / vmess / trojan / ss / hysteria2 /
   hysteria / tuic / socks / http`.
2. **Cleans & dedupes** them (structure hash, independent of display names).
3. **Really tests** every candidate: each proxy is loaded as an outbound into a
   real Xray or sing-box instance on the runner, then
   - **Phase 1 — connectivity:** HTTPS `generate_204` through the tunnel with
     DNS resolved on the proxy side,
   - **Phase 2 — egress verification:** the exit IP seen by `ip-api` must
     **differ from the runner's own IP** (leaks are excluded),
   - **Throughput:** 1 MB download from `speed.cloudflare.com` through the tunnel.
4. **Publishes** a living README report plus a full set of subscription files.

## The product (after the first run)

```
subs/
  all.txt                 ALL working proxies, ranked by speed
  all.base64.txt          same, base64 (classic subscription format)
  top150.txt              curated top 150
  top150.base64.txt       same, base64
  by-proto/<proto>.txt    per-protocol working lists (vless, vmess, trojan, ...)
  by-engine/allxray.txt   verified through the Xray core
  by-engine/allsingbox.txt  verified through the sing-box core
  by-engine/alldirect.txt   plain http/socks (curl-verified)
  by-country/<CC>.txt     per-exit-country lists (US.txt, DE.txt, ...)
  sing-box-client.json    ready-to-run sing-box client config (top 150)
  xray-client.json        ready-to-run xray client config (top 150)
```

Every plain list also has a `.base64.txt` sibling. The README shows which exit
countries currently work, with counts, speeds, and a link per country.

## How to use

- **v2rayN / v2rayNG / Nekobox / Hiddify / Shadowrocket:** subscribe to
  `https://raw.githubusercontent.com/<owner>/<repo>/main/subs/all.base64.txt`
- **One country only:** `.../subs/by-country/US.txt` (see README table)
- **One protocol only:** `.../subs/by-proto/vless.txt`
- **sing-box / Xray users:** grab the ready-made client JSON configs.

## Repository layout

```
sources/   url_subs.yml + telegram.yml (the scannable source lists)
scripts/   collect.py, test.py, report.py + lib/ (parsers, engines, state)
state/     source health, alive-recall pool, geo cache (committed)
data/      stats + history (committed), full results (artifact only)
subs/      THE PRODUCT: verified working proxies
badges/    shields.io endpoint badges
archive/   gz snapshots of every collection (30 kept)
```

## Disclaimers

- Free proxies are **public and untrusted** — never send credentials or do
  anything sensitive through them.
- All configs come from publicly posted sources; nothing is brute-forced.
  Removal requests: open an issue.
- The working list is re-verified every 6 hours; availability is transient.

License: MIT
