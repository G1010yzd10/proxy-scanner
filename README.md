# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-01 02:41:07 UTC** — 177244 unique proxies collected from 173/173 URL sources and 81/81 Telegram channels; **4500** endpoints really tested, **1112** reachable, **1075** verified working (egress IP confirmed changed) across **52 exit countries**.

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

All 1075 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `ss` | `66.23.204.219:10676` | United States | 176 ms | 45.4 Mbps | xray |
| 2 | #2 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.42.85:2095` | United States | 97 ms | 42.1 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.170:443` | United States | 249 ms | 41.3 Mbps | xray |
| 4 | #4 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.108:2086` | United States | 75 ms | 40.4 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vless` | `195.211.98.43:443` | United States | 379 ms | 36.8 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `ss` | `103.214.111.162:16469` | United States | 217 ms | 36.4 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `198.46.215.223:8443` | United States | 87 ms | 35.8 Mbps | xray |
| 8 | #8 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.103:2095` | United States | 90 ms | 34.3 Mbps | xray |
| 9 | #9 🇨🇦 CA → 🇨🇦 CA | `ss` | `185.156.47.97:9443` | Canada | 311 ms | 33.9 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `ss` | `66.23.201.174:10274` | United States | 60 ms | 30.9 Mbps | xray |
| 11 | #11 🇨🇦 CA → 🇺🇸 US | `trojan` | `188.114.96.8:443` | United States | 168 ms | 30.9 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.167:443` | United States | 148 ms | 30.1 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `198.251.78.29:2053` | United States | 178 ms | 28.4 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vmess` | `167.88.62.124:22324` | United States | 88 ms | 28.2 Mbps | xray |
| 15 | #15 🇨🇦 CA → 🇦🇺 AU | `vmess` | `23.162.200.198:18000` | Australia | 133 ms | 26.5 Mbps | xray |
| 16 | #16 ❓ ?? → 🇺🇸 US | `vless` | `uspanel.unixzone.us:30016` | United States | 181 ms | 26.5 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.169:443` | United States | 272 ms | 26.3 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.168:443` | United States | 83 ms | 26.2 Mbps | xray |
| 19 | #19 🇨🇦 CA → 🇨🇦 CA | `vmess` | `198.57.27.190:22324` | Canada | 101 ms | 25.8 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 117 ms | 25.1 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `ss` | `198.98.53.130:443` | United States | 311 ms | 25.1 Mbps | xray |
| 22 | #22 🇨🇦 CA → 🇨🇦 CA | `ss` | `64.74.161.148:17201` | Canada | 109 ms | 25.0 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vmess` | `66.163.115.23:443` | United States | 140 ms | 24.4 Mbps | singbox |
| 24 | #24 ❓ ?? → 🇨🇦 CA | `ss` | `yyz-ca-01.blncvpn4u.cc:9443` | Canada | 137 ms | 24.3 Mbps | xray |
| 25 | #25 🇨🇦 CA → 🇨🇦 CA | `vmess` | `134.195.198.214:22324` | Canada | 133 ms | 24.1 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 52 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 385 | 14.0 Mbps | 60 ms | 36% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 155 | 5.9 Mbps | 335 ms | 14% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 84 | 4.9 Mbps | 366 ms | 8% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 60 | 5.2 Mbps | 338 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇬🇧 United Kingdom | 35 | 5.7 Mbps | 232 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇸🇬 Singapore | 33 | 3.2 Mbps | 794 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇨🇦 Canada | 30 | 16.2 Mbps | 101 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇭🇰 Hong Kong | 29 | 3.3 Mbps | 584 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇯🇵 Japan | 24 | 3.4 Mbps | 416 ms | 2% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇰🇷 South Korea | 20 | 3.3 Mbps | 605 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇸🇪 Sweden | 18 | 3.9 Mbps | 513 ms | 2% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇫🇮 Finland | 17 | 3.9 Mbps | 423 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇵🇱 Poland | 17 | 4.3 Mbps | 538 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇮🇳 India | 15 | 2.7 Mbps | 553 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇪🇸 Spain | 13 | 6.2 Mbps | 173 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇦🇺 Australia | 10 | 14.1 Mbps | 112 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇮🇹 Italy | 10 | 5.4 Mbps | 403 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇸 Serbia | 10 | 4.2 Mbps | 743 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇹🇷 Turkey | 9 | 3.6 Mbps | 576 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇬 Bulgaria | 9 | 4.2 Mbps | 608 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇷🇺 Russia | 9 | 2.3 Mbps | 759 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇰🇿 Kazakhstan | 7 | 2.5 Mbps | 1172 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇲🇩 Moldova | 7 | 2.6 Mbps | 964 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇳🇴 Norway | 6 | 5.5 Mbps | 480 ms | 1% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇺🇦 Ukraine | 5 | 3.4 Mbps | 511 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇨🇭 Switzerland | 5 | 3.6 Mbps | 389 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇹🇼 Taiwan | 5 | 3.6 Mbps | 581 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇷🇴 Romania | 4 | 4.3 Mbps | 608 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇱🇰 LK | 4 | 3.5 Mbps | 1101 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇦🇹 Austria | 3 | 6.1 Mbps | 427 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇱🇻 Latvia | 3 | 5.2 Mbps | 496 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇪🇪 Estonia | 3 | 4.7 Mbps | 594 ms | 0% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇮🇪 Ireland | 3 | 5.2 Mbps | 318 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇿🇦 South Africa | 3 | 3.3 Mbps | 908 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇦🇩 AD | 2 | 5.9 Mbps | 499 ms | 0% | [`AD.txt`](subs/by-country/AD.txt) |
| 🇬🇷 Greece | 2 | 3.7 Mbps | 691 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇦🇪 UAE | 2 | 3.2 Mbps | 881 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇱🇹 Lithuania | 2 | 3.7 Mbps | 749 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇹🇭 Thailand | 2 | 3.4 Mbps | 783 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇲🇾 Malaysia | 2 | - | 649 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇸🇰 Slovakia | 2 | - | 836 ms | 0% | [`SK.txt`](subs/by-country/SK.txt) |
| 🇬🇹 GT | 1 | 10.7 Mbps | 353 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇭🇺 Hungary | 1 | 6.2 Mbps | 504 ms | 0% | [`HU.txt`](subs/by-country/HU.txt) |
| 🇵🇭 Philippines | 1 | 3.4 Mbps | 970 ms | 0% | [`PH.txt`](subs/by-country/PH.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.1 Mbps | 1076 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.3 Mbps | 2036 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇩🇰 Denmark | 1 | 1.7 Mbps | 2353 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |
| 🇧🇷 Brazil | 1 | - | 994 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇦🇷 Argentina | 1 | - | 1040 ms | 0% | [`AR.txt`](subs/by-country/AR.txt) |
| 🇮🇩 Indonesia | 1 | - | 1732 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇨🇳 China | 1 | - | 1929 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇸🇨 SC | 1 | - | 4488 ms | 0% | [`SC.txt`](subs/by-country/SC.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3031 | 742 | 708 | 24% |
| `ss` | 552 | 200 | 199 | 36% |
| `vmess` | 763 | 112 | 110 | 15% |
| `trojan` | 117 | 46 | 46 | 39% |
| `hysteria2` | 33 | 12 | 12 | 36% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 1025 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 50 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 568 |
| 1 - 5 Mbps | 283 |
| 0.25 - 1 Mbps | 17 |
| < 0.25 Mbps | 0 |
| unmeasured | 207 |

Latency (phase-1 HTTPS round trip): median **489 ms**, p90 **1513 ms**. 37 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

211 active, 43 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2819 | 605 | 60 |
| `HC` | url | 1713 | 489 | 7 |
| `ST-VL` | url | 2741 | 481 | 37 |
| `HP` | url | 546 | 440 | 3 |
| `SK` | url | 839 | 439 | 34 |
| `NK` | url | 802 | 403 | 0 |
| `SB-VL` | url | 2405 | 345 | 0 |
| `F0` | url | 468 | 339 | 0 |
| `SB` | url | 2637 | 334 | 0 |
| `EV` | url | 444 | 299 | 0 |
| `Ni` | url | 367 | 266 | 0 |
| `KA` | url | 2302 | 210 | 0 |
| `ET` | url | 348 | 202 | 519 |
| `RD-SS` | url | 527 | 198 | 4 |
| `EP-ALL` | url | 1356 | 151 | 0 |
| `EV-VL` | url | 223 | 149 | 0 |
| `WU` | url | 199 | 144 | 80 |
| `BR-VL` | url | 799 | 142 | 0 |
| `AG-PL` | url | 377 | 133 | 49 |
| `EV-SS` | url | 157 | 130 | 0 |

## History

working per run (last 10): ▁▁▆▆▇█▇▆▇█

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
| 2026-10-01 03:00 | 4500 | 1112 | 1075 | 8.1M | 45.4M |
| 2026-09-30 21:54 | 4500 | 899 | 866 | 9.3M | 69.4M |
| 2026-09-30 17:26 | 4500 | 838 | 795 | 7.3M | 57.9M |
| 2026-09-30 11:48 | 4500 | 860 | 810 | 7.9M | 64.4M |
| 2026-09-30 02:56 | 4500 | 1030 | 973 | 10.3M | 92.2M |
| 2026-09-29 21:53 | 4500 | 880 | 852 | 6.5M | 61.8M |
| 2026-09-29 15:48 | 4500 | 839 | 796 | 6.7M | 51.3M |
| 2026-09-29 14:48 | 4500 | 799 | 756 | 6.9M | 52.1M |
| 2026-09-29 14:12 | 4500 | 0 | 0 | - | - |
| 2026-09-29 13:39 | 0 | 0 | 0 | - | - |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (1075) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (1025) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (50) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (52 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **75% unreachable** and **76% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

