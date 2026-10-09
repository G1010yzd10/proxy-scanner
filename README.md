# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-09 12:10:24 UTC** — 160116 unique proxies collected from 132/132 URL sources and 47/47 Telegram channels; **4508** endpoints really tested, **904** reachable, **853** verified working (egress IP confirmed changed) across **45 exit countries**.

## How the testing works (the *really* part)

```mermaid
flowchart LR
  S1[URL subs<br/>+ Telegram] --> F[fetch &<br/>parse]
  F --> C[clean &<br/>dedupe]
  C --> T1[phase 1<br/>connectivity<br/>gstatic 204]
  T1 -->|reachable| T2[phase 2<br/>exit IP check<br/>ip-api]
  T1 -->|dead| X[drop]
  T2 -->|egress changed| T3[1 MB speed<br/>test]
  T2 -->|same IP| X2[mark leak]
  T3 --> R[README + subs<br/>+ badges]
```

1. **Phase 1 — connectivity.** Each proxy is loaded as an outbound into a real Xray or sing-box instance (or used directly via `curl -x` for plain http/socks). An HTTPS request to `gstatic.com/generate_204` goes through the tunnel with **DNS resolved on the proxy side**. Only an HTTP 204 counts as reachable.
2. **Phase 2 — egress verification.** An ip-api request through the same tunnel must return an exit IP **different from the runner's own IP**, plus its country and AS. Proxies that pass phase 1 but keep your IP are marked as leaks and excluded from the working list. Server country vs exit country mismatches are flagged in the tables.
3. **Throughput.** Working proxies download 1 MB from `speed.cloudflare.com` through the tunnel; the measured rate is the speed you see in the tables.
4. **Engine fallback.** If a proxy fails on Xray, it is retried on sing-box (and vice versa) before being declared dead — some configs only work on one core.

## Top working proxies

All 853 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.169:443` | United States | 319 ms | 37.6 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.167:443` | United States | 458 ms | 33.9 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.170:443` | United States | 195 ms | 32.9 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `ss` | `5.78.51.123:1080` | United States | 473 ms | 23.6 Mbps | xray |
| 5 | #5 ❓ ?? → 🇺🇸 US | `vless` | `144.202.126.147:443` | United States | 134 ms | 23.1 Mbps | singbox |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `hysteria2` | `155.248.209.237:33333` | United States | 125 ms | 22.7 Mbps | singbox |
| 7 | #7 ❓ ?? → 🇺🇸 US | `vless` | `45.32.69.110:443` | United States | 196 ms | 22.7 Mbps | singbox |
| 8 | #8 ❓ ?? → 🇺🇸 US | `vless` | `45.63.53.81:443` | United States | 140 ms | 22.6 Mbps | singbox |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.168:443` | United States | 64 ms | 22.4 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.219:23576` | United States | 210 ms | 22.2 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 487 ms | 21.2 Mbps | singbox |
| 12 | #12 ❓ ?? → 🇺🇸 US | `vless` | `38.107.232.36:80` | United States | 136 ms | 20.8 Mbps | xray |
| 13 | #13 ❓ ?? → 🇺🇸 US | `vless` | `3h-unitedstates1.09vpn.com:80` | United States | 155 ms | 20.4 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.209:23576` | United States | 299 ms | 19.2 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `195.123.240.65:443` | United States | 378 ms | 19.1 Mbps | xray |
| 16 | #16 ❓ ?? → 🇺🇸 US | `hysteria2` | `163.192.14.135:50160` | United States | 133 ms | 19.0 Mbps | singbox |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `69.48.201.136:30016` | United States | 190 ms | 18.7 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `195.211.98.43:443` | United States | 412 ms | 18.6 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 138 ms | 18.2 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.206:23576` | United States | 159 ms | 17.5 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.214:23576` | United States | 154 ms | 17.5 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.216:23576` | United States | 153 ms | 17.4 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 299 ms | 17.2 Mbps | xray |
| 24 | #24 ❓ ?? → 🇺🇸 US | `vless` | `172.245.253.16:443` | United States | 161 ms | 17.2 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.0.177:8388` | United States | 363 ms | 17.1 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 45 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇳🇱 Netherlands | 159 | 4.7 Mbps | 402 ms | 19% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇺🇸 United States | 147 | 11.5 Mbps | 64 ms | 17% | [`US.txt`](subs/by-country/US.txt) |
| 🇩🇪 Germany | 92 | 4.0 Mbps | 383 ms | 11% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇯🇵 Japan | 60 | 3.3 Mbps | 374 ms | 7% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇫🇷 France | 54 | 5.4 Mbps | 508 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇸🇬 Singapore | 35 | 2.4 Mbps | 572 ms | 4% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇰🇷 South Korea | 32 | 3.9 Mbps | 536 ms | 4% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇵🇱 Poland | 25 | 2.9 Mbps | 600 ms | 3% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇬🇧 United Kingdom | 23 | 4.2 Mbps | 377 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇭🇰 Hong Kong | 23 | 2.5 Mbps | 686 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇨🇦 Canada | 20 | 5.9 Mbps | 167 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇫🇮 Finland | 19 | 3.3 Mbps | 458 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇦🇺 Australia | 12 | 8.9 Mbps | 177 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇪🇪 Estonia | 12 | 3.5 Mbps | 597 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇮🇳 India | 12 | 3.0 Mbps | 489 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇧🇬 Bulgaria | 12 | 3.6 Mbps | 704 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇷🇸 Serbia | 10 | 3.6 Mbps | 884 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇪 Ireland | 8 | 2.6 Mbps | 320 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇧🇾 BY | 8 | 1.4 Mbps | 2708 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇸🇪 Sweden | 7 | 3.2 Mbps | 690 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇨🇭 Switzerland | 6 | 5.0 Mbps | 555 ms | 1% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇷🇴 Romania | 6 | 3.8 Mbps | 624 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇹🇷 Turkey | 6 | 2.5 Mbps | 804 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇰🇿 Kazakhstan | 6 | 1.8 Mbps | 1473 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇷🇺 Russia | 5 | 2.5 Mbps | 505 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇱🇻 Latvia | 5 | 3.7 Mbps | 753 ms | 1% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇮🇹 Italy | 5 | 3.8 Mbps | 462 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇹🇼 Taiwan | 5 | 3.2 Mbps | 553 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇹🇭 Thailand | 5 | 1.1 Mbps | 901 ms | 1% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇪🇸 Spain | 4 | 4.8 Mbps | 727 ms | 0% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇲🇩 Moldova | 4 | 2.7 Mbps | 985 ms | 0% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇲🇾 Malaysia | 4 | 3.3 Mbps | 601 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇳🇴 Norway | 3 | 2.0 Mbps | 1736 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇮🇩 Indonesia | 3 | 0.6 Mbps | 1217 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇦🇹 Austria | 2 | 5.4 Mbps | 468 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇦🇪 UAE | 2 | 2.9 Mbps | 982 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇨🇿 Czechia | 2 | 2.0 Mbps | 946 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇿🇦 South Africa | 2 | 2.5 Mbps | 1012 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇻🇳 Vietnam | 2 | 2.5 Mbps | 2326 ms | 0% | [`VN.txt`](subs/by-country/VN.txt) |
| 🇬🇷 Greece | 1 | 4.3 Mbps | 765 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.1 Mbps | 1288 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.2 Mbps | 6986 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇨🇳 China | 1 | - | 737 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇨🇱 Chile | 1 | - | 769 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇮🇱 Israel | 1 | - | 1018 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2840 | 463 | 431 | 16% |
| `ss` | 470 | 199 | 190 | 42% |
| `trojan` | 231 | 132 | 126 | 57% |
| `vmess` | 890 | 72 | 68 | 8% |
| `hysteria2` | 73 | 36 | 36 | 49% |
| `tuic` | 2 | 2 | 2 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 751 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 102 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 294 |
| 1 - 5 Mbps | 347 |
| 0.25 - 1 Mbps | 55 |
| < 0.25 Mbps | 0 |
| unmeasured | 157 |

Latency (phase-1 HTTPS round trip): median **781 ms**, p90 **3607 ms**. 51 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

179 active, 75 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `SK` | url | 995 | 556 | 5846 |
| `NK` | url | 934 | 499 | 0 |
| `HP` | url | 413 | 347 | 45 |
| `Ni` | url | 400 | 308 | 267 |
| `ET` | url | 382 | 303 | 2403 |
| `F0` | url | 352 | 268 | 188 |
| `RD-VL` | url | 2450 | 265 | 4064 |
| `HC` | url | 1458 | 234 | 75 |
| `EV` | url | 403 | 207 | 0 |
| `AG-PL` | url | 422 | 202 | 1412 |
| `RD-SS` | url | 425 | 187 | 300 |
| `ST-VL` | url | 2388 | 184 | 743 |
| `KA` | url | 1709 | 147 | 7349 |
| `EV-SS` | url | 154 | 122 | 62 |
| `SB` | url | 2441 | 118 | 3 |
| `TK` | url | 137 | 89 | 0 |
| `SB-VL` | url | 2080 | 88 | 0 |
| `WD` | url | 78 | 75 | 121 |
| `RO` | url | 89 | 75 | 17 |
| `EB2` | url | 143 | 74 | 7 |

## History

working per run (last 30): ▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇▇▇▇▇█▆▇█▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
| 2026-10-09 12:32 | 4508 | 904 | 853 | 5.2M | 37.6M |
| 2026-10-09 03:37 | 4504 | 1042 | 1006 | 8.3M | 72.4M |
| 2026-10-08 22:53 | 4507 | 873 | 851 | 5.5M | 55.0M |
| 2026-10-08 12:40 | 4504 | 827 | 775 | 6.8M | 67.7M |
| 2026-10-08 03:32 | 4506 | 1004 | 982 | 5.9M | 36.7M |
| 2026-10-07 22:39 | 4509 | 841 | 819 | 7.8M | 74.8M |
| 2026-10-07 12:30 | 4516 | 858 | 815 | 5.7M | 36.0M |
| 2026-10-07 03:14 | 4516 | 957 | 922 | 6.7M | 49.7M |
| 2026-10-06 22:16 | 4513 | 946 | 913 | 7.8M | 46.8M |
| 2026-10-06 12:39 | 4515 | 918 | 867 | 6.7M | 38.2M |
| 2026-10-06 03:49 | 4521 | 1046 | 1018 | 10.0M | 87.7M |
| 2026-10-05 23:43 | 4527 | 929 | 912 | 7.6M | 50.6M |
| 2026-10-05 19:47 | 4547 | 861 | 822 | 8.6M | 77.6M |
| 2026-10-03 11:04 | 4500 | 899 | 860 | 8.7M | 82.3M |
| 2026-10-03 02:52 | 4500 | 1062 | 1030 | 8.0M | 75.5M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (853) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (751) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (102) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (45 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
| [`sing-box-client.json`](subs/sing-box-client.json) | top 150 as a ready-to-run sing-box client config | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/sing-box-client.json` |
| [`xray-client.json`](subs/xray-client.json) | top 150 as a ready-to-run xray client config | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/xray-client.json` |
| [`archive/`](archive/) | gz snapshot of every collection (30 kept) | — |

## Use the proxies

- **v2rayN / v2rayNG / Nekobox / Hiddify / Shadowrocket**: add subscription `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` (everything working) or `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` (curated top 150).
- **Want a specific country?** Grab `subs/by-country/<CC>.txt` (see the Exit locations table above) — e.g. `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-country/US.txt`, `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-country/DE.txt`.
- **Only one protocol?** `subs/by-proto/<proto>.txt` — e.g. `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-proto/vless.txt`, `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-proto/hysteria2.txt`.
- **sing-box**: download [`subs/sing-box-client.json`](subs/sing-box-client.json) and run `sing-box run -c sing-box-client.json` — it listens on `127.0.0.1:2080` (mixed) with a selector + auto urltest group.
- **Xray**: download [`subs/xray-client.json`](subs/xray-client.json), socks inbound on `127.0.0.1:2080`.
- Raw snapshots of every collection: [`archive/`](archive/) (30 kept).

## Repository layout

```
sources/            url_subs.yml + telegram.yml (scannable source lists)
scripts/            collect.py, test.py, report.py + lib/
state/              source health, alive-recall pool, geo cache (committed)
data/               stats, history, compact last-run results
subs/               THE PRODUCT: verified working proxies, split by
                    proto / engine / exit country + all + top150 lists
badges/             shields.io endpoint badges
archive/            gz snapshots of every collection
```

## Why most "free proxy lists" lie

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **80% unreachable** and **81% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

