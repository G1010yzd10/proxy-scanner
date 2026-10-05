# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-05 19:27:01 UTC** — 155208 unique proxies collected from 134/134 URL sources and 47/47 Telegram channels; **4547** endpoints really tested, **861** reachable, **822** verified working (egress IP confirmed changed) across **47 exit countries**.

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

All 822 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `vmess` | `172.111.38.100:22324` | United States | 1078 ms | 77.6 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 375 ms | 64.7 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:22324` | United States | 369 ms | 62.2 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 260 ms | 58.6 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vmess` | `67.220.95.3:18000` | United States | 1377 ms | 55.9 Mbps | xray |
| 6 | #6 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.34.14:2082` | United States | 51 ms | 55.0 Mbps | xray |
| 7 | #7 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.158.146:2095` | United States | 72 ms | 54.1 Mbps | xray |
| 8 | #8 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.24.131:8880` | United States | 49 ms | 53.1 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `147.182.212.232:56565` | United States | 547 ms | 51.7 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `162.159.38.127:2095` | United States | 42 ms | 49.2 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.202:443` | United States | 124 ms | 47.7 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 131 ms | 47.0 Mbps | singbox |
| 13 | #13 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.48.32:8080` | United States | 45 ms | 46.1 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `137.184.218.169:36925` | United States | 201 ms | 45.1 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 61 ms | 44.8 Mbps | xray |
| 16 | #16 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.46:2086` | United States | 47 ms | 44.0 Mbps | xray |
| 17 | #17 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.169:2086` | United States | 358 ms | 43.6 Mbps | xray |
| 18 | #18 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.154.8:8080` | United States | 46 ms | 43.3 Mbps | xray |
| 19 | #19 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.46:8080` | United States | 499 ms | 42.8 Mbps | xray |
| 20 | #20 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.46:2052` | United States | 46 ms | 42.2 Mbps | xray |
| 21 | #21 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.43.187:8880` | United States | 40 ms | 40.9 Mbps | xray |
| 22 | #22 ❓ ?? → 🇺🇸 US | `vless` | `cdn8.alihapp.com:443` | United States | 609 ms | 40.7 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.247.206:4444` | United States | 72 ms | 38.1 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vless` | `2.24.124.64:443` | United States | 106 ms | 36.4 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.182:443` | United States | 76 ms | 36.2 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 47 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 245 | 16.3 Mbps | 28 ms | 30% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 147 | 6.7 Mbps | 296 ms | 18% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 71 | 5.1 Mbps | 283 ms | 9% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 42 | 4.3 Mbps | 368 ms | 5% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 40 | 3.6 Mbps | 476 ms | 5% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇰🇷 South Korea | 25 | 3.3 Mbps | 646 ms | 3% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇨🇦 Canada | 22 | 12.8 Mbps | 77 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇸🇬 Singapore | 22 | 2.9 Mbps | 665 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇭🇰 Hong Kong | 19 | 2.9 Mbps | 659 ms | 2% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇬🇧 United Kingdom | 18 | 6.9 Mbps | 257 ms | 2% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇵🇱 Poland | 15 | 4.3 Mbps | 446 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 15 | 3.6 Mbps | 356 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇨🇱 Chile | 10 | 5.3 Mbps | 477 ms | 1% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇷🇸 Serbia | 10 | 4.7 Mbps | 667 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇪🇪 Estonia | 9 | 5.7 Mbps | 411 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇧🇬 Bulgaria | 9 | 4.8 Mbps | 627 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇮🇳 India | 9 | 2.5 Mbps | 785 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇮🇹 Italy | 8 | 3.6 Mbps | 339 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇸🇪 Sweden | 8 | 3.8 Mbps | 423 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇷🇴 Romania | 8 | 4.7 Mbps | 599 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇪🇸 Spain | 6 | 6.0 Mbps | 373 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇲🇩 Moldova | 6 | 2.9 Mbps | 785 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇹🇷 Turkey | 5 | 2.9 Mbps | 659 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇰🇿 Kazakhstan | 5 | 2.3 Mbps | 1022 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇮🇪 Ireland | 4 | 6.4 Mbps | 359 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇷🇺 Russia | 4 | 4.6 Mbps | 392 ms | 0% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇳🇴 Norway | 4 | 6.3 Mbps | 415 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇿🇦 South Africa | 4 | 3.4 Mbps | 885 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇹🇼 Taiwan | 4 | 2.4 Mbps | 698 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇨🇭 Switzerland | 3 | 4.8 Mbps | 484 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇱🇹 Lithuania | 3 | 6.2 Mbps | 587 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇧🇾 BY | 3 | 2.1 Mbps | 5287 ms | 0% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇦🇹 Austria | 2 | 7.2 Mbps | 359 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇱🇻 Latvia | 2 | 5.6 Mbps | 480 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇦🇪 UAE | 2 | 3.8 Mbps | 839 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇱🇰 LK | 2 | 2.9 Mbps | 1127 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇦🇱 AL | 1 | 7.8 Mbps | 564 ms | 0% | [`AL.txt`](subs/by-country/AL.txt) |
| 🇸🇦 Saudi Arabia | 1 | 4.7 Mbps | 885 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇨🇿 Czechia | 1 | 4.3 Mbps | 956 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇧🇷 Brazil | 1 | 3.7 Mbps | 652 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇲🇾 Malaysia | 1 | 3.7 Mbps | 998 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇹🇭 Thailand | 1 | 3.0 Mbps | 941 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇬🇷 Greece | 1 | 2.5 Mbps | 1557 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇬🇪 Georgia | 1 | 1.4 Mbps | 4353 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇦🇲 Armenia | 1 | 1.2 Mbps | 1974 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇨🇾 Cyprus | 1 | - | 3173 ms | 0% | [`CY.txt`](subs/by-country/CY.txt) |
| 🇮🇩 Indonesia | 1 | - | 3422 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3019 | 482 | 459 | 16% |
| `ss` | 424 | 198 | 188 | 47% |
| `vmess` | 924 | 90 | 86 | 10% |
| `trojan` | 141 | 77 | 75 | 55% |
| `hysteria2` | 37 | 14 | 14 | 38% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 751 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 71 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 442 |
| 1 - 5 Mbps | 236 |
| 0.25 - 1 Mbps | 39 |
| < 0.25 Mbps | 0 |
| unmeasured | 105 |

Latency (phase-1 HTTPS round trip): median **627 ms**, p90 **4114 ms**. 39 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

180 active, 74 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 853 | 495 | 4528 |
| `SK` | url | 800 | 444 | 0 |
| `HP` | url | 491 | 389 | 219 |
| `RD-VL` | url | 2557 | 332 | 4465 |
| `Ni` | url | 367 | 290 | 255 |
| `F0` | url | 345 | 288 | 196 |
| `EV` | url | 454 | 266 | 1501 |
| `HC` | url | 1394 | 206 | 231 |
| `ET` | url | 420 | 190 | 0 |
| `ST-VL` | url | 2408 | 187 | 930 |
| `RD-SS` | url | 387 | 183 | 306 |
| `SB` | url | 2565 | 172 | 40 |
| `EV-SS` | url | 156 | 128 | 49 |
| `KA` | url | 1443 | 125 | 10716 |
| `EV-VL` | url | 249 | 121 | 0 |
| `AG-PL` | url | 415 | 117 | 1321 |
| `AN` | url | 116 | 112 | 14 |
| `SB-VL` | url | 2182 | 107 | 0 |
| `TK` | url | 131 | 97 | 0 |
| `AQ` | url | 173 | 96 | 572 |

## History

working per run (last 19): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-09-30 11:48 | 4500 | 860 | 810 | 7.9M | 64.4M |
| 2026-09-30 02:56 | 4500 | 1030 | 973 | 10.3M | 92.2M |
| 2026-09-29 21:53 | 4500 | 880 | 852 | 6.5M | 61.8M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (822) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (751) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (71) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (47 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **81% unreachable** and **82% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

