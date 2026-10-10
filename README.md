# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-10 02:57:29 UTC** — 160688 unique proxies collected from 115/115 URL sources and 13/13 Telegram channels; **4504** endpoints really tested, **1154** reachable, **1128** verified working (egress IP confirmed changed) across **48 exit countries**.

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

All 1128 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 ❓ ?? → 🇺🇸 US | `vless` | `104.17.98.5:443` | United States | 102 ms | 47.7 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 102 ms | 46.9 Mbps | singbox |
| 3 | #3 ❓ ?? → 🇺🇸 US | `vless` | `45.32.69.110:443` | United States | 60 ms | 43.2 Mbps | singbox |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.0.177:8388` | United States | 253 ms | 42.0 Mbps | xray |
| 5 | #5 ❓ ?? → 🇺🇸 US | `vmess` | `us16-4.998998.best:443` | United States | 327 ms | 41.6 Mbps | xray |
| 6 | #6 ❓ ?? → 🇺🇸 US | `ss` | `103.11.76.248:28679` | United States | 572 ms | 40.0 Mbps | xray |
| 7 | #7 ❓ ?? → 🇺🇸 US | `vless` | `144.202.126.147:443` | United States | 63 ms | 37.3 Mbps | singbox |
| 8 | #8 ❓ ?? → 🇺🇸 US | `vmess` | `nomino.11hi8itbaf.workers.dev:443` | United States | 317 ms | 36.4 Mbps | xray |
| 9 | #9 ❓ ?? → 🇺🇸 US | `vless` | `45.63.53.81:443` | United States | 73 ms | 34.8 Mbps | singbox |
| 10 | #10 ❓ ?? → 🇺🇸 US | `hysteria2` | `163.192.14.135:50160` | United States | 158 ms | 34.4 Mbps | singbox |
| 11 | #11 ❓ ?? → 🇺🇸 US | `vless` | `154.12.38.159:443` | United States | 394 ms | 34.1 Mbps | singbox |
| 12 | #12 ❓ ?? → 🇺🇸 US | `vless` | `104.19.1.100:2082` | United States | 96 ms | 33.8 Mbps | xray |
| 13 | #13 ❓ ?? → 🇺🇸 US | `vless` | `154.12.38.202:443` | United States | 102 ms | 33.3 Mbps | singbox |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 203 ms | 32.3 Mbps | xray |
| 15 | #15 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.561891.xyz:44356` | United States | 95 ms | 32.3 Mbps | singbox |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vmess` | `129.146.77.248:39495` | United States | 27 ms | 32.0 Mbps | xray |
| 17 | #17 🇸🇨 SC → 🇺🇸 US | `vless` | `45.130.125.126:443` | United States | 78 ms | 31.4 Mbps | xray |
| 18 | #18 ❓ ?? → 🇺🇸 US | `vless` | `154.29.145.196:443` | United States | 74 ms | 30.9 Mbps | singbox |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `195.123.240.65:443` | United States | 2602 ms | 29.0 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 117 ms | 28.7 Mbps | singbox |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `ss` | `216.105.168.18:443` | United States | 65 ms | 28.5 Mbps | xray |
| 22 | #22 🇨🇦 CA → 🇺🇸 US | `vless` | `104.17.147.22:443` | United States | 85 ms | 27.5 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.168:443` | United States | 86 ms | 26.4 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `hysteria2` | `155.248.209.237:33333` | United States | 103 ms | 26.3 Mbps | singbox |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `ss` | `5.78.51.123:1080` | United States | 119 ms | 25.5 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 48 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 300 | 13.5 Mbps | 22 ms | 27% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 178 | 4.9 Mbps | 402 ms | 16% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 111 | 4.4 Mbps | 396 ms | 10% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇯🇵 Japan | 71 | 4.1 Mbps | 334 ms | 6% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇫🇷 France | 65 | 4.9 Mbps | 524 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇸🇬 Singapore | 49 | 3.2 Mbps | 546 ms | 4% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇰🇷 South Korea | 41 | 4.5 Mbps | 506 ms | 4% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇵🇱 Poland | 34 | 4.0 Mbps | 633 ms | 3% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇭🇰 Hong Kong | 29 | 4.4 Mbps | 485 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇬🇧 United Kingdom | 28 | 4.5 Mbps | 401 ms | 2% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇫🇮 Finland | 28 | 3.6 Mbps | 496 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇨🇦 Canada | 22 | 6.6 Mbps | 170 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇧🇬 Bulgaria | 12 | 3.8 Mbps | 694 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇮🇳 India | 12 | 2.1 Mbps | 494 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇪🇪 Estonia | 11 | 4.0 Mbps | 607 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇷🇸 Serbia | 11 | 3.7 Mbps | 679 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇪 Ireland | 10 | 4.2 Mbps | 492 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇹🇷 Turkey | 10 | 3.3 Mbps | 630 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇾 BY | 9 | 4.2 Mbps | 912 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇸🇪 Sweden | 8 | 4.6 Mbps | 569 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇱🇻 Latvia | 7 | 4.0 Mbps | 685 ms | 1% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇮🇹 Italy | 7 | 4.4 Mbps | 467 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇪🇸 Spain | 6 | 4.3 Mbps | 572 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇷🇴 Romania | 6 | 3.3 Mbps | 575 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇹🇭 Thailand | 6 | 2.5 Mbps | 728 ms | 1% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇲🇩 Moldova | 6 | 3.1 Mbps | 1004 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇹🇼 Taiwan | 5 | 3.1 Mbps | 482 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇰🇿 Kazakhstan | 5 | 1.7 Mbps | 1539 ms | 0% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇨🇭 Switzerland | 4 | 5.5 Mbps | 478 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇷🇺 Russia | 4 | 3.6 Mbps | 793 ms | 0% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇮🇩 Indonesia | 4 | 2.1 Mbps | 891 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇦🇪 UAE | 4 | 2.9 Mbps | 1068 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇦🇹 Austria | 3 | 4.0 Mbps | 495 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇳🇴 Norway | 3 | 3.5 Mbps | 507 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇿🇦 South Africa | 3 | 2.9 Mbps | 945 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇨🇿 Czechia | 2 | 4.6 Mbps | 656 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇲🇾 Malaysia | 2 | 2.9 Mbps | 774 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇨🇳 China | 2 | - | 1086 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇲🇽 Mexico | 1 | 9.0 Mbps | 421 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇦🇺 Australia | 1 | 5.0 Mbps | 702 ms | 0% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇬🇷 Greece | 1 | 4.2 Mbps | 769 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇦🇱 AL | 1 | 4.2 Mbps | 930 ms | 0% | [`AL.txt`](subs/by-country/AL.txt) |
| 🇻🇳 Vietnam | 1 | 3.4 Mbps | 1035 ms | 0% | [`VN.txt`](subs/by-country/VN.txt) |
| 🇸🇦 Saudi Arabia | 1 | 2.8 Mbps | 1300 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.2 Mbps | 2060 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇱🇺 Luxembourg | 1 | 1.6 Mbps | 6151 ms | 0% | [`LU.txt`](subs/by-country/LU.txt) |
| 🇨🇱 Chile | 1 | - | 756 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇮🇱 Israel | 1 | - | 1192 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2888 | 655 | 637 | 23% |
| `ss` | 444 | 201 | 199 | 45% |
| `trojan` | 244 | 152 | 152 | 62% |
| `vmess` | 837 | 90 | 84 | 11% |
| `hysteria2` | 87 | 54 | 54 | 62% |
| `tuic` | 2 | 2 | 2 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 1029 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 99 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 390 |
| 1 - 5 Mbps | 485 |
| 0.25 - 1 Mbps | 21 |
| < 0.25 Mbps | 0 |
| unmeasured | 232 |

Latency (phase-1 HTTPS round trip): median **642 ms**, p90 **2051 ms**. 26 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

128 active, 126 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 1025 | 703 | 6218 |
| `SK` | url | 996 | 678 | 638 |
| `HP` | url | 465 | 418 | 105 |
| `RD-VL` | url | 2513 | 376 | 4400 |
| `HC` | url | 1487 | 367 | 340 |
| `ET` | url | 379 | 339 | 1177 |
| `ST-VL` | url | 2462 | 305 | 739 |
| `F0` | url | 307 | 283 | 82 |
| `Ni` | url | 369 | 281 | 6 |
| `AG-PL` | url | 557 | 280 | 1259 |
| `EV` | url | 398 | 241 | 1374 |
| `KA` | url | 1615 | 225 | 5565 |
| `RD-SS` | url | 421 | 197 | 286 |
| `SB-VL` | url | 2204 | 186 | 3 |
| `SB` | url | 2521 | 183 | 0 |
| `EV-SS` | url | 153 | 125 | 61 |
| `EP-ALL` | url | 2206 | 116 | 0 |
| `YA-VL` | url | 462 | 98 | 1508 |
| `TK` | url | 135 | 98 | 5 |
| `EV-VL` | url | 191 | 98 | 0 |

## History

working per run (last 30): ▆▇▇▆▆▇█▇▆▇▆▆▇█▇▆▇█▇▇▇▆▆▇▆▇█▇▇█

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
| 2026-10-10 03:18 | 4504 | 1154 | 1128 | 6.1M | 47.7M |
| 2026-10-09 22:15 | 4506 | 966 | 935 | 6.8M | 51.9M |
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

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (1128) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (1029) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (99) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **74% unreachable** and **75% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

