# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-03 02:31:29 UTC** — 255228 unique proxies collected from 134/134 URL sources and 47/47 Telegram channels; **4500** endpoints really tested, **1062** reachable, **1030** verified working (egress IP confirmed changed) across **53 exit countries**.

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

All 1030 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 51 ms | 75.5 Mbps | xray |
| 2 | #2 ❓ ?? → 🇺🇸 US | `vless` | `q2-phbest7v2a8iuowpr.g0xigfh41wwnv39y-b3rzmht.workers.dev:443` | United States | 187 ms | 57.7 Mbps | xray |
| 3 | #3 🇨🇦 CA → 🇺🇸 US | `vless` | `104.24.65.202:2086` | United States | 59 ms | 56.1 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `167.17.68.205:443` | United States | 60 ms | 55.8 Mbps | xray |
| 5 | #5 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.81.177:80` | United States | 58 ms | 55.4 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇦🇺 AU | `vmess` | `169.197.142.22:18000` | Australia | 68 ms | 54.6 Mbps | xray |
| 7 | #7 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.154.8:2052` | United States | 354 ms | 54.4 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `trojan` | `43.173.90.202:443` | United States | 38 ms | 52.5 Mbps | singbox |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vmess` | `216.152.152.187:22324` | United States | 55 ms | 52.1 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `2.27.160.4:443` | United States | 55 ms | 51.6 Mbps | xray |
| 11 | #11 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.154.8:2082` | United States | 444 ms | 50.6 Mbps | xray |
| 12 | #12 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.123266.xyz:33333` | United States | 79 ms | 49.4 Mbps | singbox |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `172.233.139.46:53734` | United States | 69 ms | 48.5 Mbps | xray |
| 14 | #14 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.229.2:80` | United States | 407 ms | 46.0 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `hysteria2` | `155.248.209.237:33333` | United States | 60 ms | 45.9 Mbps | singbox |
| 16 | #16 🇨🇦 CA → 🇺🇸 US | `vless` | `104.25.122.72:80` | United States | 59 ms | 44.7 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vmess` | `167.17.68.89:443` | United States | 407 ms | 44.3 Mbps | xray |
| 18 | #18 ❓ ?? → 🇺🇸 US | `vless` | `154.12.38.202:443` | United States | 897 ms | 43.9 Mbps | singbox |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 69 ms | 43.4 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vmess` | `216.106.185.141:22324` | United States | 141 ms | 42.8 Mbps | xray |
| 21 | #21 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.561891.xyz:44356` | United States | 98 ms | 42.3 Mbps | singbox |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `ss` | `5.78.51.123:1080` | United States | 104 ms | 41.2 Mbps | xray |
| 23 | #23 ❓ ?? → 🇺🇸 US | `vless` | `3h-unitedstates3.09vpn.com:8443` | United States | 49 ms | 40.7 Mbps | singbox |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.214:23576` | United States | 489 ms | 40.5 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.43.210:53957` | United States | 64 ms | 40.1 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 53 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 395 | 15.5 Mbps | 33 ms | 38% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 147 | 4.6 Mbps | 457 ms | 14% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 79 | 3.9 Mbps | 453 ms | 8% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 33 | 4.0 Mbps | 577 ms | 3% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇭🇰 Hong Kong | 29 | 3.4 Mbps | 475 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇬🇧 United Kingdom | 28 | 4.3 Mbps | 431 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇯🇵 Japan | 26 | 4.3 Mbps | 354 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇨🇦 Canada | 25 | 8.8 Mbps | 112 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇵🇱 Poland | 24 | 3.6 Mbps | 690 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇰🇷 South Korea | 20 | 4.8 Mbps | 495 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇸🇬 Singapore | 17 | 3.2 Mbps | 514 ms | 2% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇪🇸 Spain | 13 | 4.3 Mbps | 344 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇸🇪 Sweden | 13 | 3.6 Mbps | 685 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇷🇸 Serbia | 12 | 3.4 Mbps | 946 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇦🇺 Australia | 11 | 15.5 Mbps | 68 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇫🇮 Finland | 11 | 3.0 Mbps | 538 ms | 1% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇷🇺 Russia | 11 | 1.6 Mbps | 780 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇮🇳 India | 10 | 2.3 Mbps | 797 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇮🇹 Italy | 9 | 4.3 Mbps | 506 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇪🇪 Estonia | 8 | 4.6 Mbps | 221 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇹🇷 Turkey | 8 | 2.7 Mbps | 668 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇬 Bulgaria | 8 | 3.4 Mbps | 753 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇲🇩 Moldova | 8 | 2.7 Mbps | 1108 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇨🇭 Switzerland | 7 | 4.2 Mbps | 497 ms | 1% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇧🇾 BY | 7 | 4.2 Mbps | 918 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇷🇴 Romania | 7 | 3.6 Mbps | 672 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇰🇿 Kazakhstan | 7 | 1.9 Mbps | 1236 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇳🇴 Norway | 5 | 4.4 Mbps | 677 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇦🇹 Austria | 5 | 4.4 Mbps | 580 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇹🇼 Taiwan | 4 | 4.5 Mbps | 567 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇧🇷 Brazil | 4 | 2.2 Mbps | 725 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇿🇦 South Africa | 4 | 2.7 Mbps | 998 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇨🇿 Czechia | 3 | 3.8 Mbps | 992 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇮🇪 Ireland | 3 | 4.4 Mbps | 410 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇨🇱 Chile | 3 | 4.1 Mbps | 716 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇱🇰 LK | 3 | 3.4 Mbps | 992 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇲🇽 Mexico | 2 | 12.0 Mbps | 240 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇲🇾 Malaysia | 2 | 4.8 Mbps | 736 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇹🇭 Thailand | 2 | 4.2 Mbps | 664 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇬🇷 Greece | 2 | 3.9 Mbps | 825 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇱🇻 Latvia | 2 | 3.6 Mbps | 1049 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇦🇪 UAE | 2 | 2.9 Mbps | 1080 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇬🇹 GT | 1 | 7.6 Mbps | 297 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇨🇴 Colombia | 1 | 7.2 Mbps | 606 ms | 0% | [`CO.txt`](subs/by-country/CO.txt) |
| 🇭🇺 Hungary | 1 | 4.9 Mbps | 604 ms | 0% | [`HU.txt`](subs/by-country/HU.txt) |
| 🇵🇭 Philippines | 1 | 3.8 Mbps | 937 ms | 0% | [`PH.txt`](subs/by-country/PH.txt) |
| 🇱🇹 Lithuania | 1 | 3.4 Mbps | 1029 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇩🇰 Denmark | 1 | 3.0 Mbps | 1127 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |
| 🇸🇦 Saudi Arabia | 1 | 2.7 Mbps | 1169 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.3 Mbps | 1986 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇶🇦 Qatar | 1 | 1.5 Mbps | 1443 ms | 0% | [`QA.txt`](subs/by-country/QA.txt) |
| 🇬🇪 Georgia | 1 | 0.7 Mbps | 5898 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇮🇩 Indonesia | 1 | - | 1090 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3210 | 708 | 691 | 22% |
| `ss` | 605 | 199 | 194 | 33% |
| `vmess` | 522 | 118 | 108 | 23% |
| `trojan` | 137 | 23 | 23 | 17% |
| `hysteria2` | 22 | 14 | 14 | 64% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 970 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 60 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 321 |
| 1 - 5 Mbps | 483 |
| 0.25 - 1 Mbps | 26 |
| < 0.25 Mbps | 0 |
| unmeasured | 200 |

Latency (phase-1 HTTPS round trip): median **584 ms**, p90 **1393 ms**. 32 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

181 active, 73 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2975 | 582 | 73 |
| `ST-VL` | url | 2890 | 479 | 70 |
| `HC` | url | 1743 | 451 | 5 |
| `SK` | url | 987 | 421 | 29 |
| `HP` | url | 574 | 398 | 1 |
| `NK` | url | 945 | 393 | 14 |
| `SB-VL` | url | 2514 | 359 | 1 |
| `SB` | url | 2770 | 338 | 0 |
| `F0` | url | 528 | 311 | 0 |
| `EV` | url | 427 | 298 | 0 |
| `Ni` | url | 427 | 243 | 0 |
| `KA` | url | 1783 | 215 | 0 |
| `ET` | url | 414 | 208 | 336 |
| `RD-SS` | url | 580 | 194 | 0 |
| `EP-ALL` | url | 1313 | 182 | 0 |
| `WU` | url | 247 | 146 | 7 |
| `EV-VL` | url | 213 | 146 | 0 |
| `AG-PL` | url | 363 | 134 | 98 |
| `BR-VL` | url | 837 | 133 | 0 |
| `EV-SS` | url | 157 | 131 | 0 |

## History

working per run (last 17): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-09-29 15:48 | 4500 | 839 | 796 | 6.7M | 51.3M |
| 2026-09-29 14:48 | 4500 | 799 | 756 | 6.9M | 52.1M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (1030) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (970) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (60) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **76% unreachable** and **77% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

