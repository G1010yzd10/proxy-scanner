# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-06 12:18:10 UTC** — 155078 unique proxies collected from 133/133 URL sources and 47/47 Telegram channels; **4515** endpoints really tested, **918** reachable, **867** verified working (egress IP confirmed changed) across **44 exit countries**.

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

All 867 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.167:443` | United States | 497 ms | 38.2 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.168:443` | United States | 251 ms | 34.9 Mbps | xray |
| 3 | #3 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.53:2095` | United States | 106 ms | 34.2 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.169:443` | United States | 490 ms | 29.0 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vmess` | `167.88.62.124:22324` | United States | 275 ms | 27.7 Mbps | xray |
| 6 | #6 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.103:2095` | United States | 475 ms | 26.8 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `66.42.97.171:443` | United States | 117 ms | 26.0 Mbps | xray |
| 8 | #8 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.108:2082` | United States | 103 ms | 25.6 Mbps | xray |
| 9 | #9 ❓ ?? → 🇺🇸 US | `vless` | `45.32.69.110:443` | United States | 134 ms | 25.1 Mbps | singbox |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 138 ms | 25.0 Mbps | xray |
| 11 | #11 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.47.113:2052` | United States | 103 ms | 24.0 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `vless` | `162.159.38.127:2095` | United States | 164 ms | 24.0 Mbps | xray |
| 13 | #13 ❓ ?? → 🇺🇸 US | `vless` | `144.202.126.147:443` | United States | 134 ms | 23.6 Mbps | singbox |
| 14 | #14 ❓ ?? → 🇺🇸 US | `vless` | `84.32.71.124:443` | United States | 155 ms | 23.1 Mbps | xray |
| 15 | #15 ❓ ?? → 🇺🇸 US | `vless` | `45.63.53.81:443` | United States | 141 ms | 22.6 Mbps | singbox |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `ss` | `5.78.51.123:1080` | United States | 134 ms | 22.5 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.214:23576` | United States | 150 ms | 22.4 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.209:23576` | United States | 142 ms | 22.1 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.216:23576` | United States | 160 ms | 21.9 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.197:23576` | United States | 175 ms | 21.8 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.219:23576` | United States | 351 ms | 21.6 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.206:23576` | United States | 142 ms | 21.6 Mbps | xray |
| 23 | #23 ❓ ?? → 🇺🇸 US | `ss` | `66.23.204.210:16995` | United States | 258 ms | 21.6 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.170:443` | United States | 393 ms | 21.5 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 169 ms | 21.2 Mbps | singbox |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 44 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 263 | 12.3 Mbps | 85 ms | 30% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 145 | 5.1 Mbps | 408 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 82 | 4.1 Mbps | 421 ms | 9% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 51 | 4.3 Mbps | 546 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 39 | 4.2 Mbps | 385 ms | 4% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇭🇰 Hong Kong | 25 | 3.2 Mbps | 585 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇸🇬 Singapore | 24 | 2.5 Mbps | 590 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇨🇦 Canada | 23 | 9.2 Mbps | 147 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇬🇧 United Kingdom | 21 | 4.3 Mbps | 378 ms | 2% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇰🇷 South Korea | 18 | 4.2 Mbps | 533 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇵🇱 Poland | 17 | 2.3 Mbps | 619 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 14 | 2.9 Mbps | 635 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇪🇪 Estonia | 12 | 4.0 Mbps | 571 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇨🇱 Chile | 11 | 4.3 Mbps | 553 ms | 1% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇷🇸 Serbia | 10 | 3.7 Mbps | 882 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇳 India | 9 | 1.5 Mbps | 1174 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇷🇴 Romania | 8 | 3.4 Mbps | 772 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇧🇬 Bulgaria | 8 | 3.5 Mbps | 842 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇲🇩 Moldova | 8 | 2.5 Mbps | 1006 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇮🇹 Italy | 7 | 3.9 Mbps | 458 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇪🇸 Spain | 7 | 3.5 Mbps | 597 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇸🇪 Sweden | 7 | 2.6 Mbps | 724 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇹🇷 Turkey | 7 | 2.4 Mbps | 750 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇮🇪 Ireland | 6 | 3.1 Mbps | 424 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇰🇿 Kazakhstan | 6 | 2.7 Mbps | 1204 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇳🇴 Norway | 4 | 3.9 Mbps | 795 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇹🇼 Taiwan | 4 | 3.1 Mbps | 533 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇦🇹 Austria | 3 | 5.2 Mbps | 471 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇨🇭 Switzerland | 3 | 3.4 Mbps | 556 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇷🇺 Russia | 3 | 1.9 Mbps | 537 ms | 0% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇿🇦 South Africa | 3 | 2.9 Mbps | 995 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇧🇾 BY | 3 | 1.5 Mbps | 3159 ms | 0% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇱🇻 Latvia | 2 | 4.8 Mbps | 789 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇧🇷 Brazil | 2 | 3.2 Mbps | 840 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇮🇩 Indonesia | 2 | 3.5 Mbps | 1090 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇦🇪 UAE | 2 | 1.9 Mbps | 2412 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇱🇹 Lithuania | 1 | 4.3 Mbps | 738 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.8 Mbps | 1127 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇹🇭 Thailand | 1 | 3.5 Mbps | 720 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇨🇿 Czechia | 1 | 3.5 Mbps | 1152 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇦🇲 Armenia | 1 | 2.4 Mbps | 2043 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇬🇷 Greece | 1 | 2.2 Mbps | 778 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇬🇪 Georgia | 1 | 1.0 Mbps | 7471 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇲🇾 Malaysia | 1 | - | 2403 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2857 | 520 | 494 | 18% |
| `ss` | 431 | 187 | 177 | 43% |
| `vmess` | 1044 | 105 | 91 | 10% |
| `trojan` | 144 | 91 | 90 | 63% |
| `hysteria2` | 36 | 14 | 14 | 39% |
| `tuic` | 1 | 1 | 1 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 779 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 88 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 410 |
| 1 - 5 Mbps | 310 |
| 0.25 - 1 Mbps | 38 |
| < 0.25 Mbps | 0 |
| unmeasured | 109 |

Latency (phase-1 HTTPS round trip): median **631 ms**, p90 **3668 ms**. 51 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

180 active, 74 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `SK` | url | 809 | 509 | 4571 |
| `NK` | url | 779 | 482 | 0 |
| `HP` | url | 503 | 423 | 155 |
| `RD-VL` | url | 2480 | 344 | 4004 |
| `HC` | url | 1511 | 338 | 244 |
| `F0` | url | 365 | 284 | 171 |
| `Ni` | url | 353 | 266 | 115 |
| `EV` | url | 446 | 263 | 23 |
| `ET` | url | 226 | 199 | 0 |
| `ST-VL` | url | 2346 | 198 | 769 |
| `RD-SS` | url | 407 | 175 | 303 |
| `KA` | url | 1442 | 153 | 10429 |
| `SB` | url | 2431 | 149 | 12 |
| `AG-PL` | url | 438 | 132 | 1181 |
| `EV-SS` | url | 156 | 125 | 61 |
| `EV-VL` | url | 239 | 120 | 1476 |
| `AN` | url | 114 | 111 | 6 |
| `TK` | url | 135 | 88 | 0 |
| `RD-VM` | url | 761 | 87 | 2071 |
| `YA-VL` | url | 464 | 84 | 1540 |

## History

working per run (last 22): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
| 2026-10-06 12:39 | 4515 | 918 | 867 | 6.7M | 38.2M |
| 2026-10-06 03:49 | 4521 | 1046 | 1018 | 10.0M | 87.7M |
| 2026-10-05 23:43 | 4527 | 929 | 912 | 7.6M | 50.6M |
| 2026-10-05 19:47 | 4547 | 861 | 822 | 8.6M | 77.6M |
| 2026-10-03 11:04 | 4500 | 899 | 860 | 8.7M | 82.3M |
| 2026-10-03 02:52 | 4500 | 1062 | 1030 | 8.0M | 75.5M |
| 2026-10-02 21:49 | 4500 | 890 | 861 | 8.9M | 68.7M |
| 2026-10-02 17:14 | 4500 | 847 | 807 | 8.6M | 88.1M |
| 2026-10-02 11:49 | 4500 | 861 | 798 | 7.9M | 85.3M |
| 2026-10-01 22:23 | 4500 | 904 | 878 | 7.5M | 90.2M |
| 2026-10-01 17:56 | 4500 | 861 | 794 | 7.3M | 58.6M |
| 2026-10-01 12:16 | 4500 | 931 | 883 | 7.3M | 34.4M |
| 2026-10-01 03:00 | 4500 | 1112 | 1075 | 8.1M | 45.4M |
| 2026-09-30 21:54 | 4500 | 899 | 866 | 9.3M | 69.4M |
| 2026-09-30 17:26 | 4500 | 838 | 795 | 7.3M | 57.9M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (867) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (779) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (88) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (44 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

