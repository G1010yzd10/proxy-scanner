# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-05 23:24:21 UTC** — 155076 unique proxies collected from 133/133 URL sources and 47/47 Telegram channels; **4527** endpoints really tested, **929** reachable, **912** verified working (egress IP confirmed changed) across **48 exit countries**.

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

All 912 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.47.113:2095` | United States | 131 ms | 50.6 Mbps | xray |
| 2 | #2 ❓ ?? → 🇺🇸 US | `vless` | `45.63.53.81:443` | United States | 60 ms | 46.2 Mbps | singbox |
| 3 | #3 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.108:8080` | United States | 107 ms | 45.7 Mbps | xray |
| 4 | #4 ❓ ?? → 🇺🇸 US | `vless` | `45.32.69.110:443` | United States | 415 ms | 44.5 Mbps | singbox |
| 5 | #5 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.561891.xyz:44356` | United States | 127 ms | 43.3 Mbps | singbox |
| 6 | #6 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.42.85:8880` | United States | 101 ms | 42.9 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `ss` | `173.244.56.9:443` | United States | 139 ms | 41.5 Mbps | xray |
| 8 | #8 ❓ ?? → 🇺🇸 US | `vless` | `154.29.145.196:443` | United States | 73 ms | 40.8 Mbps | singbox |
| 9 | #9 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.169:2086` | United States | 100 ms | 40.2 Mbps | xray |
| 10 | #10 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.234:80` | United States | 315 ms | 39.2 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `ss` | `173.244.56.6:443` | United States | 90 ms | 38.6 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 137 ms | 38.2 Mbps | xray |
| 13 | #13 ❓ ?? → 🇺🇸 US | `vless` | `144.202.126.147:443` | United States | 65 ms | 38.0 Mbps | singbox |
| 14 | #14 ❓ ?? → 🇺🇸 US | `vmess` | `guanwang.awsno.com:443` | United States | 299 ms | 37.0 Mbps | xray |
| 15 | #15 ❓ ?? → 🇺🇸 US | `vless` | `154.12.38.159:443` | United States | 78 ms | 36.8 Mbps | singbox |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 106 ms | 34.9 Mbps | xray |
| 17 | #17 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.53:80` | United States | 81 ms | 34.4 Mbps | xray |
| 18 | #18 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.43.187:8080` | United States | 172 ms | 34.1 Mbps | xray |
| 19 | #19 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.103:2082` | United States | 110 ms | 33.8 Mbps | xray |
| 20 | #20 ❓ ?? → 🇺🇸 US | `vmess` | `www.shopify.com:443` | United States | 140 ms | 33.8 Mbps | xray |
| 21 | #21 ❓ ?? → 🇺🇸 US | `vmess` | `vspeedfast.org:443` | United States | 566 ms | 33.5 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.0.177:8388` | United States | 59 ms | 32.6 Mbps | xray |
| 23 | #23 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.229.2:80` | United States | 98 ms | 32.4 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vmess` | `129.146.77.248:39495` | United States | 66 ms | 32.3 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vmess` | `167.17.68.89:443` | United States | 75 ms | 31.8 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 48 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 252 | 15.9 Mbps | 35 ms | 28% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 159 | 5.0 Mbps | 425 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 87 | 4.2 Mbps | 417 ms | 10% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 56 | 4.4 Mbps | 514 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 42 | 5.2 Mbps | 339 ms | 5% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇰🇷 South Korea | 31 | 4.2 Mbps | 489 ms | 3% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇨🇦 Canada | 25 | 8.3 Mbps | 165 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇸🇬 Singapore | 24 | 2.8 Mbps | 540 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇬🇧 United Kingdom | 22 | 4.5 Mbps | 396 ms | 2% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇵🇱 Poland | 17 | 3.5 Mbps | 625 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 16 | 3.6 Mbps | 496 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇭🇰 Hong Kong | 13 | 3.9 Mbps | 480 ms | 1% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇮🇳 India | 12 | 2.9 Mbps | 494 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇨🇱 Chile | 11 | 5.1 Mbps | 552 ms | 1% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇪🇪 Estonia | 10 | 4.3 Mbps | 625 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇷🇸 Serbia | 10 | 3.4 Mbps | 921 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇲🇩 Moldova | 10 | 3.2 Mbps | 1004 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇸🇪 Sweden | 9 | 4.2 Mbps | 539 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇹🇷 Turkey | 9 | 3.4 Mbps | 573 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇬 Bulgaria | 9 | 3.5 Mbps | 766 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇮🇹 Italy | 8 | 3.3 Mbps | 488 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇴 Romania | 8 | 3.4 Mbps | 753 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇧🇾 BY | 8 | 4.2 Mbps | 911 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇪🇸 Spain | 7 | 4.3 Mbps | 484 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇰🇿 Kazakhstan | 6 | 2.1 Mbps | 1232 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇮🇪 Ireland | 5 | 4.8 Mbps | 376 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇹🇼 Taiwan | 5 | 3.4 Mbps | 515 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇷🇺 Russia | 4 | 3.6 Mbps | 548 ms | 0% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇳🇴 Norway | 4 | 3.2 Mbps | 607 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇦🇹 Austria | 3 | 5.1 Mbps | 490 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇨🇭 Switzerland | 3 | 4.4 Mbps | 631 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇹🇭 Thailand | 3 | 3.5 Mbps | 737 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇿🇦 South Africa | 3 | 2.9 Mbps | 966 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇱🇻 Latvia | 2 | 4.2 Mbps | 664 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇱🇹 Lithuania | 2 | 4.3 Mbps | 738 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇲🇾 Malaysia | 2 | 4.0 Mbps | 600 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇮🇩 Indonesia | 2 | 3.7 Mbps | 819 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇦🇪 UAE | 2 | 3.0 Mbps | 1053 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇱🇰 LK | 2 | 2.8 Mbps | 1309 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇲🇽 Mexico | 1 | 7.2 Mbps | 622 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇦🇱 AL | 1 | 4.8 Mbps | 859 ms | 0% | [`AL.txt`](subs/by-country/AL.txt) |
| 🇬🇷 Greece | 1 | 4.2 Mbps | 812 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇧🇷 Brazil | 1 | 3.8 Mbps | 948 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇨🇿 Czechia | 1 | 3.4 Mbps | 1208 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇬🇪 Georgia | 1 | 3.3 Mbps | 1433 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇸🇦 Saudi Arabia | 1 | 2.8 Mbps | 1328 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.3 Mbps | 2064 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇨🇳 China | 1 | - | 960 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3010 | 533 | 521 | 18% |
| `ss` | 419 | 199 | 196 | 47% |
| `trojan` | 159 | 94 | 94 | 59% |
| `vmess` | 898 | 88 | 86 | 10% |
| `hysteria2` | 38 | 14 | 14 | 37% |
| `tuic` | 1 | 1 | 1 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 857 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 55 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 451 |
| 1 - 5 Mbps | 391 |
| 0.25 - 1 Mbps | 12 |
| < 0.25 Mbps | 0 |
| unmeasured | 58 |

Latency (phase-1 HTTPS round trip): median **597 ms**, p90 **1342 ms**. 17 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

180 active, 74 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 875 | 578 | 4609 |
| `HP` | url | 487 | 455 | 102 |
| `SK` | url | 676 | 381 | 0 |
| `RD-VL` | url | 2623 | 369 | 4577 |
| `HC` | url | 1619 | 352 | 359 |
| `Ni` | url | 382 | 325 | 135 |
| `F0` | url | 342 | 303 | 53 |
| `EV` | url | 449 | 272 | 15 |
| `ST-VL` | url | 2489 | 227 | 785 |
| `RD-SS` | url | 394 | 191 | 255 |
| `ET` | url | 420 | 190 | 0 |
| `AG-PL` | url | 401 | 160 | 1313 |
| `KA` | url | 1251 | 141 | 1844 |
| `EV-SS` | url | 156 | 130 | 67 |
| `SB-VL` | url | 2271 | 130 | 1 |
| `EV-VL` | url | 244 | 125 | 1498 |
| `AN` | url | 121 | 120 | 2 |
| `SB` | url | 2508 | 120 | 0 |
| `TK` | url | 117 | 94 | 0 |
| `YA-VL` | url | 495 | 89 | 1509 |

## History

working per run (last 20): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-09-30 11:48 | 4500 | 860 | 810 | 7.9M | 64.4M |
| 2026-09-30 02:56 | 4500 | 1030 | 973 | 10.3M | 92.2M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (912) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (857) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (55) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (48 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **79% unreachable** and **80% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

