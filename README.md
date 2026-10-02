# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-02 16:54:15 UTC** — 252502 unique proxies collected from 136/136 URL sources and 47/47 Telegram channels; **4500** endpoints really tested, **847** reachable, **807** verified working (egress IP confirmed changed) across **52 exit countries**.

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

All 807 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:443` | United States | 83 ms | 88.1 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.104.144:8081` | United States | 55 ms | 61.8 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.96.21:8081` | United States | 48 ms | 58.5 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.95.3:18000` | Australia | 165 ms | 58.1 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 122 ms | 56.8 Mbps | xray |
| 6 | #6 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.39.218:2082` | United States | 42 ms | 54.7 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:22324` | United States | 52 ms | 50.9 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.96.18:8081` | United States | 48 ms | 50.8 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `162.159.39.218:2052` | United States | 39 ms | 48.3 Mbps | xray |
| 10 | #10 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.53:8880` | United States | 36 ms | 47.7 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 71 ms | 46.9 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `ss` | `198.98.53.130:443` | United States | 94 ms | 46.8 Mbps | singbox |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.75:443` | United States | 149 ms | 46.7 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `185.95.231.233:443` | United States | 89 ms | 46.6 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 95 ms | 45.5 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `79.141.172.154:10453` | United States | 50 ms | 45.0 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 131 ms | 44.3 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 185 ms | 43.5 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.246.132:7307` | United States | 4022 ms | 42.8 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `159.89.87.21:28190` | United States | 60 ms | 42.1 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vmess` | `167.88.63.59:22324` | United States | 58 ms | 39.7 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vmess` | `172.111.38.100:22324` | United States | 247 ms | 39.7 Mbps | xray |
| 23 | #23 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.43.187:8080` | United States | 65 ms | 39.0 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vless` | `47.253.226.114:443` | United States | 34 ms | 37.4 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.85.46:18000` | Australia | 4981 ms | 36.2 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 52 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 246 | 15.0 Mbps | 29 ms | 30% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 143 | 6.6 Mbps | 268 ms | 18% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 57 | 5.7 Mbps | 296 ms | 7% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 35 | 6.0 Mbps | 364 ms | 4% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇵🇱 Poland | 28 | 3.8 Mbps | 434 ms | 3% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇯🇵 Japan | 25 | 2.7 Mbps | 482 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇬🇧 United Kingdom | 23 | 5.6 Mbps | 267 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇨🇦 Canada | 22 | 14.1 Mbps | 91 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇭🇰 Hong Kong | 22 | 4.0 Mbps | 684 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇰🇷 South Korea | 17 | 2.9 Mbps | 649 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇫🇮 Finland | 15 | 4.4 Mbps | 432 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇸🇬 Singapore | 15 | 2.8 Mbps | 893 ms | 2% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇦🇺 Australia | 11 | 18.5 Mbps | 133 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇸🇪 Sweden | 11 | 2.7 Mbps | 497 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇷🇺 Russia | 11 | 4.0 Mbps | 578 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇷🇸 Serbia | 10 | 5.0 Mbps | 659 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇪🇸 Spain | 9 | 8.0 Mbps | 138 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇧🇬 Bulgaria | 8 | 5.1 Mbps | 624 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇲🇩 Moldova | 7 | 2.6 Mbps | 870 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇰🇿 Kazakhstan | 7 | 1.6 Mbps | 1771 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇮🇳 India | 7 | 0.8 Mbps | 801 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇮🇹 Italy | 6 | 5.8 Mbps | 362 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇴 Romania | 6 | 2.2 Mbps | 692 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇹🇷 Turkey | 6 | 2.9 Mbps | 622 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇪🇪 Estonia | 5 | 8.9 Mbps | 149 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇦🇹 Austria | 5 | 6.9 Mbps | 358 ms | 1% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇨🇭 Switzerland | 4 | 5.8 Mbps | 418 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇳🇴 Norway | 4 | 2.5 Mbps | 376 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇹🇼 Taiwan | 4 | 2.6 Mbps | 650 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇧🇾 BY | 4 | 1.0 Mbps | 949 ms | 0% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇨🇱 Chile | 3 | 3.8 Mbps | 537 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇿🇦 South Africa | 3 | 3.3 Mbps | 839 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇲🇾 Malaysia | 3 | 3.5 Mbps | 935 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇱🇰 LK | 3 | 1.7 Mbps | 1065 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇮🇪 Ireland | 2 | 6.4 Mbps | 333 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇬🇷 Greece | 2 | 5.1 Mbps | 579 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇱🇻 Latvia | 2 | 4.3 Mbps | 545 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇦🇪 UAE | 2 | 3.3 Mbps | 873 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇬🇹 GT | 1 | 9.2 Mbps | 391 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇨🇴 Colombia | 1 | 8.9 Mbps | 383 ms | 0% | [`CO.txt`](subs/by-country/CO.txt) |
| 🇧🇷 Brazil | 1 | 5.1 Mbps | 805 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.7 Mbps | 1131 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇱🇹 Lithuania | 1 | 3.5 Mbps | 2553 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇹🇭 Thailand | 1 | 3.3 Mbps | 866 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇨🇿 Czechia | 1 | 3.0 Mbps | 765 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇵🇭 Philippines | 1 | 3.0 Mbps | 1117 ms | 0% | [`PH.txt`](subs/by-country/PH.txt) |
| 🇶🇦 Qatar | 1 | 2.3 Mbps | 1135 ms | 0% | [`QA.txt`](subs/by-country/QA.txt) |
| 🇦🇲 Armenia | 1 | 2.2 Mbps | 1999 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇩🇰 Denmark | 1 | 2.1 Mbps | 995 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |
| 🇭🇺 Hungary | 1 | 2.1 Mbps | 420 ms | 0% | [`HU.txt`](subs/by-country/HU.txt) |
| 🇲🇽 Mexico | 1 | - | 239 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇮🇩 Indonesia | 1 | - | 6779 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3166 | 502 | 482 | 16% |
| `ss` | 594 | 199 | 196 | 34% |
| `vmess` | 579 | 107 | 96 | 18% |
| `trojan` | 136 | 26 | 20 | 19% |
| `hysteria2` | 21 | 13 | 13 | 62% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 734 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 73 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 420 |
| 1 - 5 Mbps | 238 |
| 0.25 - 1 Mbps | 46 |
| < 0.25 Mbps | 0 |
| unmeasured | 103 |

Latency (phase-1 HTTPS round trip): median **536 ms**, p90 **4519 ms**. 40 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

182 active, 72 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2934 | 399 | 239 |
| `HP` | url | 576 | 375 | 0 |
| `SK` | url | 968 | 356 | 23 |
| `NK` | url | 926 | 332 | 0 |
| `HC` | url | 1768 | 327 | 0 |
| `ST-VL` | url | 2841 | 295 | 42 |
| `F0` | url | 507 | 286 | 0 |
| `EV` | url | 431 | 274 | 0 |
| `Ni` | url | 421 | 231 | 0 |
| `SB-VL` | url | 2455 | 210 | 1 |
| `RD-SS` | url | 570 | 195 | 9 |
| `ET` | url | 407 | 187 | 0 |
| `SB` | url | 2709 | 185 | 1 |
| `KA` | url | 1907 | 155 | 0 |
| `EV-SS` | url | 157 | 132 | 0 |
| `EV-VL` | url | 217 | 122 | 0 |
| `AG-PL` | url | 366 | 121 | 55 |
| `WU` | url | 239 | 114 | 0 |
| `EP-ALL` | url | 1275 | 98 | 0 |
| `RD-VM` | url | 495 | 92 | 3 |

## History

working per run (last 15): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-09-29 13:39 | 0 | 0 | 0 | - | - |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (807) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (734) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (73) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **81% unreachable** and **82% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

