# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-02 21:29:46 UTC** — 253607 unique proxies collected from 135/135 URL sources and 47/47 Telegram channels; **4500** endpoints really tested, **890** reachable, **861** verified working (egress IP confirmed changed) across **53 exit countries**.

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

All 861 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:22324` | United States | 134 ms | 68.7 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `vmess` | `172.111.38.100:22324` | United States | 466 ms | 68.2 Mbps | xray |
| 3 | #3 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.46:2052` | United States | 57 ms | 63.8 Mbps | xray |
| 4 | #4 ❓ ?? → 🇺🇸 US | `vmess` | `vspeedfast.org:443` | United States | 486 ms | 50.6 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:443` | United States | 83 ms | 48.6 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 291 ms | 48.5 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.95.3:18000` | Australia | 819 ms | 48.2 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 152 ms | 47.6 Mbps | xray |
| 9 | #9 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.34.14:8080` | United States | 533 ms | 45.3 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.133:443` | United States | 137 ms | 41.9 Mbps | xray |
| 11 | #11 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.234:2082` | United States | 60 ms | 41.7 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.96.21:8081` | United States | 64 ms | 41.4 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.96.18:8081` | United States | 61 ms | 40.7 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 208 ms | 40.6 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.104.144:8081` | United States | 116 ms | 40.2 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.15:443` | United States | 199 ms | 39.9 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.95:443` | United States | 204 ms | 39.6 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.224:443` | United States | 133 ms | 39.2 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `185.95.231.233:443` | United States | 421 ms | 39.1 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `ss` | `198.98.53.130:443` | United States | 404 ms | 38.7 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.223:443` | United States | 482 ms | 38.4 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `147.182.212.232:56565` | United States | 82 ms | 37.3 Mbps | xray |
| 23 | #23 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.169:8880` | United States | 526 ms | 35.8 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vmess` | `167.88.63.59:22324` | United States | 413 ms | 35.0 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 211 ms | 33.6 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 53 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 247 | 16.2 Mbps | 36 ms | 29% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 147 | 6.6 Mbps | 297 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 68 | 5.7 Mbps | 302 ms | 8% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 59 | 4.6 Mbps | 364 ms | 7% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 28 | 4.1 Mbps | 470 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇨🇦 Canada | 24 | 15.3 Mbps | 115 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇬🇧 United Kingdom | 24 | 6.0 Mbps | 313 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇭🇰 Hong Kong | 23 | 3.1 Mbps | 615 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇵🇱 Poland | 22 | 4.5 Mbps | 476 ms | 3% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇰🇷 South Korea | 20 | 3.5 Mbps | 605 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇸🇬 Singapore | 16 | 3.0 Mbps | 894 ms | 2% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇪🇸 Spain | 14 | 6.7 Mbps | 171 ms | 2% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇦🇺 Australia | 11 | 15.4 Mbps | 56 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇸🇪 Sweden | 11 | 4.6 Mbps | 548 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇫🇮 Finland | 10 | 3.5 Mbps | 491 ms | 1% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇷🇺 Russia | 10 | 2.4 Mbps | 553 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇷🇸 Serbia | 10 | 4.8 Mbps | 661 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇳 India | 9 | 1.4 Mbps | 1867 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇮🇹 Italy | 8 | 5.5 Mbps | 355 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇧🇬 Bulgaria | 8 | 5.0 Mbps | 520 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇪🇪 Estonia | 7 | 8.1 Mbps | 124 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇧🇾 BY | 7 | 3.6 Mbps | 990 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇷🇴 Romania | 6 | 4.1 Mbps | 514 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇲🇩 Moldova | 6 | 3.0 Mbps | 956 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇰🇿 Kazakhstan | 6 | 3.0 Mbps | 1237 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇦🇹 Austria | 5 | 7.3 Mbps | 444 ms | 1% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇹🇷 Turkey | 5 | 1.7 Mbps | 765 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇨🇭 Switzerland | 4 | 4.7 Mbps | 469 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇹🇼 Taiwan | 4 | 2.8 Mbps | 666 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇨🇱 Chile | 3 | 5.3 Mbps | 546 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇨🇿 Czechia | 3 | 2.5 Mbps | 612 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇱🇰 LK | 3 | 3.5 Mbps | 1064 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇲🇾 Malaysia | 3 | 3.3 Mbps | 731 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇳🇴 Norway | 3 | 3.0 Mbps | 557 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇿🇦 South Africa | 3 | 3.4 Mbps | 824 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇲🇽 Mexico | 2 | 12.5 Mbps | 236 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇮🇪 Ireland | 2 | 6.7 Mbps | 404 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇬🇷 Greece | 2 | 3.2 Mbps | 759 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇱🇻 Latvia | 2 | 4.8 Mbps | 839 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇦🇪 UAE | 2 | 3.8 Mbps | 849 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇹🇭 Thailand | 2 | 3.0 Mbps | 842 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇬🇹 GT | 1 | 10.2 Mbps | 369 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇨🇴 Colombia | 1 | 9.9 Mbps | 324 ms | 0% | [`CO.txt`](subs/by-country/CO.txt) |
| 🇭🇺 Hungary | 1 | 5.3 Mbps | 578 ms | 0% | [`HU.txt`](subs/by-country/HU.txt) |
| 🇧🇷 Brazil | 1 | 4.8 Mbps | 635 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇱🇹 Lithuania | 1 | 4.7 Mbps | 1263 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.9 Mbps | 1177 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇶🇦 Qatar | 1 | 3.7 Mbps | 1378 ms | 0% | [`QA.txt`](subs/by-country/QA.txt) |
| 🇵🇭 Philippines | 1 | 3.0 Mbps | 1128 ms | 0% | [`PH.txt`](subs/by-country/PH.txt) |
| 🇩🇰 Denmark | 1 | 2.4 Mbps | 1268 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |
| 🇬🇪 Georgia | 1 | 0.9 Mbps | 7727 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇦🇲 Armenia | 1 | 0.6 Mbps | 2054 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇮🇩 Indonesia | 1 | - | 1790 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3192 | 522 | 505 | 16% |
| `ss` | 601 | 202 | 196 | 34% |
| `vmess` | 546 | 110 | 104 | 20% |
| `trojan` | 136 | 43 | 43 | 32% |
| `hysteria2` | 21 | 13 | 13 | 62% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 794 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 67 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 497 |
| 1 - 5 Mbps | 250 |
| 0.25 - 1 Mbps | 34 |
| < 0.25 Mbps | 0 |
| unmeasured | 80 |

Latency (phase-1 HTTPS round trip): median **556 ms**, p90 **2528 ms**. 29 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

181 active, 73 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2959 | 425 | 101 |
| `HP` | url | 573 | 390 | 3 |
| `SK` | url | 984 | 384 | 0 |
| `NK` | url | 942 | 358 | 33 |
| `HC` | url | 1756 | 340 | 10 |
| `ST-VL` | url | 2870 | 313 | 42 |
| `F0` | url | 514 | 298 | 0 |
| `EV` | url | 428 | 274 | 0 |
| `Ni` | url | 424 | 243 | 0 |
| `SB-VL` | url | 2488 | 225 | 1 |
| `SB` | url | 2739 | 214 | 0 |
| `RD-SS` | url | 577 | 195 | 1 |
| `ET` | url | 409 | 194 | 0 |
| `KA` | url | 1835 | 165 | 0 |
| `EV-SS` | url | 157 | 131 | 0 |
| `AG-PL` | url | 363 | 127 | 0 |
| `WU` | url | 244 | 122 | 10 |
| `EV-VL` | url | 214 | 122 | 0 |
| `EP-ALL` | url | 1286 | 109 | 0 |
| `RD-VM` | url | 478 | 100 | 10 |

## History

working per run (last 16): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-09-29 15:48 | 4500 | 839 | 796 | 6.7M | 51.3M |
| 2026-09-29 14:48 | 4500 | 799 | 756 | 6.9M | 52.1M |
| 2026-09-29 14:12 | 4500 | 0 | 0 | - | - |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (861) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (794) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (67) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (53 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

