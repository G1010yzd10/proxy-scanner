# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-10 11:27:53 UTC** — 159874 unique proxies collected from 115/115 URL sources and 13/13 Telegram channels; **4506** endpoints really tested, **967** reachable, **933** verified working (egress IP confirmed changed) across **47 exit countries**.

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

All 933 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 42 ms | 63.8 Mbps | singbox |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `hysteria2` | `155.248.209.237:33333` | United States | 117 ms | 46.1 Mbps | singbox |
| 3 | #3 ❓ ?? → 🇺🇸 US | `vless` | `104.17.98.5:443` | United States | 358 ms | 39.2 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.209:23576` | United States | 449 ms | 37.8 Mbps | xray |
| 5 | #5 ❓ ?? → 🇺🇸 US | `vless` | `3h-unitedstates3.09vpn.com:8443` | United States | 94 ms | 35.8 Mbps | singbox |
| 6 | #6 ❓ ?? → 🇺🇸 US | `vmess` | `xjp111-3.vatilon.cc:10001` | United States | 30 ms | 35.4 Mbps | singbox |
| 7 | #7 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.123266.xyz:33333` | United States | 121 ms | 34.2 Mbps | singbox |
| 8 | #8 ❓ ?? → 🇺🇸 US | `vmess` | `us16-4.998998.best:443` | United States | 323 ms | 33.2 Mbps | xray |
| 9 | #9 ❓ ?? → 🇺🇸 US | `vless` | `144.202.126.147:443` | United States | 118 ms | 30.7 Mbps | singbox |
| 10 | #10 ❓ ?? → 🇨🇳 CN | `hysteria2` | `cn42.vatilon.cc:10004` | China | 56 ms | 30.1 Mbps | singbox |
| 11 | #11 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.561891.xyz:44356` | United States | 151 ms | 28.5 Mbps | singbox |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 121 ms | 27.9 Mbps | singbox |
| 13 | #13 ❓ ?? → 🇺🇸 US | `vless` | `45.63.53.81:443` | United States | 78 ms | 27.8 Mbps | singbox |
| 14 | #14 🇨🇦 CA → 🇨🇦 CA | `ss` | `149.22.95.183:443` | Canada | 237 ms | 27.7 Mbps | xray |
| 15 | #15 ❓ ?? → 🇺🇸 US | `vless` | `154.29.145.196:443` | United States | 102 ms | 27.7 Mbps | singbox |
| 16 | #16 ❓ ?? → 🇺🇸 US | `vless` | `tk1.high-speed-test-56424.me:443` | United States | 166 ms | 25.9 Mbps | xray |
| 17 | #17 ❓ ?? → 🇺🇸 US | `vless` | `154.12.38.202:443` | United States | 117 ms | 25.7 Mbps | singbox |
| 18 | #18 🇺🇸 US → 🇦🇺 AU | `vmess` | `169.197.142.22:18000` | Australia | 58 ms | 24.8 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.219:23576` | United States | 148 ms | 24.1 Mbps | xray |
| 20 | #20 ❓ ?? → 🇺🇸 US | `vless` | `154.12.38.159:443` | United States | 84 ms | 23.5 Mbps | singbox |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.216:23576` | United States | 92 ms | 22.6 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `51.81.203.63:443` | United States | 158 ms | 22.1 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.214:23576` | United States | 90 ms | 21.8 Mbps | xray |
| 24 | #24 ❓ ?? → 🇺🇸 US | `vless` | `ww13.levikogjgfdd.ir:23576` | United States | 334 ms | 21.8 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.195:23576` | United States | 89 ms | 21.8 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 47 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇳🇱 Netherlands | 175 | 4.2 Mbps | 450 ms | 19% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇺🇸 United States | 150 | 12.0 Mbps | 30 ms | 16% | [`US.txt`](subs/by-country/US.txt) |
| 🇩🇪 Germany | 102 | 3.8 Mbps | 366 ms | 11% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇯🇵 Japan | 71 | 4.4 Mbps | 327 ms | 8% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇫🇷 France | 63 | 3.4 Mbps | 588 ms | 7% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇸🇬 Singapore | 41 | 2.9 Mbps | 527 ms | 4% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇰🇷 South Korea | 39 | 3.4 Mbps | 483 ms | 4% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇫🇮 Finland | 32 | 2.8 Mbps | 542 ms | 3% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇵🇱 Poland | 29 | 2.9 Mbps | 731 ms | 3% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇬🇧 United Kingdom | 26 | 4.0 Mbps | 428 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇭🇰 Hong Kong | 24 | 3.6 Mbps | 560 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇨🇦 Canada | 16 | 6.5 Mbps | 217 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇧🇬 Bulgaria | 12 | 3.3 Mbps | 747 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇦🇺 Australia | 11 | 11.1 Mbps | 58 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇷🇸 Serbia | 11 | 3.3 Mbps | 947 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇳 India | 11 | 2.0 Mbps | 913 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇪🇪 Estonia | 10 | 2.8 Mbps | 643 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇧🇾 BY | 9 | 2.8 Mbps | 1143 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇸🇪 Sweden | 9 | 2.4 Mbps | 891 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇹🇷 Turkey | 8 | 3.6 Mbps | 892 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇮🇪 Ireland | 8 | 3.0 Mbps | 527 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇮🇹 Italy | 7 | 4.5 Mbps | 502 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇺 Russia | 6 | 2.3 Mbps | 1329 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇹🇭 Thailand | 6 | 2.6 Mbps | 697 ms | 1% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇲🇩 Moldova | 6 | 1.9 Mbps | 1256 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇨🇭 Switzerland | 4 | 4.3 Mbps | 673 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇪🇸 Spain | 4 | 4.4 Mbps | 666 ms | 0% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇹🇼 Taiwan | 4 | 4.0 Mbps | 588 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇿🇦 South Africa | 4 | 1.9 Mbps | 980 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇰🇿 Kazakhstan | 4 | 1.6 Mbps | 1836 ms | 0% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇨🇿 Czechia | 3 | 3.6 Mbps | 623 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇳🇴 Norway | 3 | 2.0 Mbps | 570 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇮🇩 Indonesia | 3 | 2.8 Mbps | 788 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇦🇪 UAE | 3 | 2.7 Mbps | 1136 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇦🇲 Armenia | 3 | 1.5 Mbps | 2015 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇨🇳 China | 2 | 30.1 Mbps | 56 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇦🇹 Austria | 2 | 4.8 Mbps | 687 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇱🇻 Latvia | 2 | 2.8 Mbps | 1104 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇷🇴 Romania | 2 | 3.8 Mbps | 922 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇲🇽 Mexico | 1 | 5.2 Mbps | 615 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇩🇰 Denmark | 1 | 4.8 Mbps | 660 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |
| 🇬🇷 Greece | 1 | 3.9 Mbps | 871 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇸🇦 Saudi Arabia | 1 | 2.7 Mbps | 1304 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇱🇰 LK | 1 | 1.2 Mbps | 1147 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇨🇱 Chile | 1 | - | 1055 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇮🇱 Israel | 1 | - | 1314 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |
| 🇲🇾 Malaysia | 1 | - | 2766 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2814 | 499 | 478 | 18% |
| `ss` | 450 | 203 | 196 | 45% |
| `trojan` | 240 | 134 | 133 | 56% |
| `vmess` | 908 | 74 | 69 | 8% |
| `hysteria2` | 90 | 55 | 55 | 61% |
| `tuic` | 2 | 2 | 2 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 787 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 146 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 162 |
| 1 - 5 Mbps | 570 |
| 0.25 - 1 Mbps | 42 |
| < 0.25 Mbps | 0 |
| unmeasured | 159 |

Latency (phase-1 HTTPS round trip): median **846 ms**, p90 **3455 ms**. 34 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

128 active, 126 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `SK` | url | 1090 | 626 | 7055 |
| `NK` | url | 1059 | 592 | 63 |
| `HP` | url | 464 | 401 | 188 |
| `ET` | url | 421 | 344 | 2648 |
| `F0` | url | 385 | 305 | 252 |
| `RD-VL` | url | 2454 | 304 | 4012 |
| `Ni` | url | 404 | 303 | 121 |
| `HC` | url | 1544 | 301 | 111 |
| `ST-VL` | url | 2352 | 212 | 685 |
| `EV` | url | 399 | 204 | 23 |
| `RD-SS` | url | 427 | 196 | 305 |
| `AG-PL` | url | 438 | 192 | 1223 |
| `KA` | url | 1796 | 171 | 3377 |
| `SB-VL` | url | 2097 | 125 | 0 |
| `EV-SS` | url | 153 | 122 | 51 |
| `SB` | url | 2427 | 117 | 0 |
| `WD` | url | 114 | 103 | 156 |
| `TK` | url | 133 | 85 | 0 |
| `10i-SC-TR` | url | 127 | 83 | 219 |
| `YA-VL` | url | 503 | 76 | 1478 |

## History

working per run (last 30): ▇▇▆▆▇█▇▆▇▆▆▇█▇▆▇█▇▇▇▆▆▇▆▇█▇▇█▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
| 2026-10-10 11:49 | 4506 | 967 | 933 | 5.2M | 63.8M |
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

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (933) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (787) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (146) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **79% unreachable** and **79% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

