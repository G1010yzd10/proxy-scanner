# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-01 22:03:41 UTC** — 248511 unique proxies collected from 137/137 URL sources and 48/48 Telegram channels; **4500** endpoints really tested, **904** reachable, **878** verified working (egress IP confirmed changed) across **48 exit countries**.

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

All 878 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 ❓ ?? → 🇺🇸 US | `vless` | `3h-unitedstates3.09vpn.com:8443` | United States | 2653 ms | 90.2 Mbps | singbox |
| 2 | #2 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.48.32:8080` | United States | 429 ms | 67.7 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `74.201.177.54:14680` | United States | 457 ms | 53.3 Mbps | xray |
| 4 | #4 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.123266.xyz:33333` | United States | 80 ms | 52.1 Mbps | singbox |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.38.85:42942` | United States | 443 ms | 51.8 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇦🇺 AU | `vmess` | `169.197.142.22:18000` | Australia | 75 ms | 51.4 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `hysteria2` | `155.248.209.237:33333` | United States | 67 ms | 51.1 Mbps | singbox |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `ss` | `104.192.225.106:15438` | United States | 466 ms | 50.8 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vmess` | `167.17.68.89:22324` | United States | 68 ms | 47.4 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `trojan` | `43.173.90.202:443` | United States | 51 ms | 44.8 Mbps | singbox |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vless` | `167.17.68.205:443` | United States | 59 ms | 44.0 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `vmess` | `216.152.152.187:22324` | United States | 72 ms | 43.1 Mbps | xray |
| 13 | #13 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.169:2082` | United States | 112 ms | 41.7 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `108.162.198.178:2086` | United States | 51 ms | 41.7 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.0.177:8388` | United States | 352 ms | 40.7 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `172.233.139.46:53734` | United States | 59 ms | 40.6 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `ss` | `5.78.51.123:1080` | United States | 67 ms | 39.7 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `23.95.222.127:8443` | United States | 113 ms | 39.3 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.43.210:53957` | United States | 55 ms | 38.6 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 49 ms | 38.5 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.206:23576` | United States | 447 ms | 38.0 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 313 ms | 37.8 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.214:23576` | United States | 99 ms | 37.8 Mbps | xray |
| 24 | #24 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.53:2095` | United States | 68 ms | 37.7 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 85 ms | 37.4 Mbps | singbox |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 48 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 262 | 15.3 Mbps | 42 ms | 30% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 146 | 4.2 Mbps | 447 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 61 | 3.8 Mbps | 480 ms | 7% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 54 | 3.8 Mbps | 597 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇸🇬 Singapore | 37 | 3.2 Mbps | 676 ms | 4% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇭🇰 Hong Kong | 29 | 4.4 Mbps | 478 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇬🇧 United Kingdom | 28 | 4.3 Mbps | 431 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇨🇦 Canada | 24 | 7.8 Mbps | 95 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇯🇵 Japan | 24 | 5.8 Mbps | 321 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇰🇷 South Korea | 22 | 4.5 Mbps | 520 ms | 3% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇵🇱 Poland | 21 | 3.3 Mbps | 642 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 16 | 3.0 Mbps | 534 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇸🇪 Sweden | 14 | 3.3 Mbps | 652 ms | 2% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇮🇳 India | 12 | 1.8 Mbps | 928 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇦🇺 Australia | 11 | 13.1 Mbps | 75 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇪🇸 Spain | 11 | 3.9 Mbps | 335 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇷🇸 Serbia | 10 | 3.4 Mbps | 945 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇹 Italy | 8 | 2.9 Mbps | 530 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇺 Russia | 8 | 1.8 Mbps | 798 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇧🇬 Bulgaria | 8 | 3.5 Mbps | 877 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇲🇩 Moldova | 7 | 2.2 Mbps | 1076 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇹🇼 Taiwan | 5 | 3.9 Mbps | 496 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇪🇪 Estonia | 5 | 3.9 Mbps | 659 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇹🇷 Turkey | 5 | 2.2 Mbps | 1034 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇳🇴 Norway | 5 | 2.9 Mbps | 723 ms | 1% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇰🇿 Kazakhstan | 5 | 1.7 Mbps | 1483 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇦🇹 Austria | 4 | 4.5 Mbps | 536 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇨🇭 Switzerland | 4 | 3.9 Mbps | 544 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇱🇰 LK | 4 | 3.4 Mbps | 1245 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇲🇾 Malaysia | 3 | 4.4 Mbps | 550 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇮🇪 Ireland | 3 | 4.1 Mbps | 397 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇿🇦 South Africa | 3 | 2.6 Mbps | 1000 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇷🇴 Romania | 2 | 4.0 Mbps | 914 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇬🇷 Greece | 2 | 3.6 Mbps | 829 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇦🇪 UAE | 2 | 2.8 Mbps | 1125 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇬🇹 GT | 1 | 10.7 Mbps | 448 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇨🇴 Colombia | 1 | 7.2 Mbps | 572 ms | 0% | [`CO.txt`](subs/by-country/CO.txt) |
| 🇨🇱 Chile | 1 | 4.9 Mbps | 672 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇵🇹 Portugal | 1 | 4.4 Mbps | 566 ms | 0% | [`PT.txt`](subs/by-country/PT.txt) |
| 🇱🇻 Latvia | 1 | 4.1 Mbps | 1056 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇵🇭 Philippines | 1 | 3.9 Mbps | 1071 ms | 0% | [`PH.txt`](subs/by-country/PH.txt) |
| 🇹🇭 Thailand | 1 | 3.8 Mbps | 706 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇧🇷 Brazil | 1 | 3.3 Mbps | 888 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇸🇦 Saudi Arabia | 1 | 2.8 Mbps | 1316 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇧🇾 BY | 1 | 2.7 Mbps | 1550 ms | 0% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇱🇹 Lithuania | 1 | 2.5 Mbps | 1627 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇦🇲 Armenia | 1 | 2.4 Mbps | 2156 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇮🇩 Indonesia | 1 | - | 4000 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3100 | 540 | 518 | 17% |
| `ss` | 570 | 201 | 197 | 35% |
| `vmess` | 683 | 108 | 108 | 16% |
| `trojan` | 120 | 42 | 42 | 35% |
| `hysteria2` | 23 | 13 | 13 | 57% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 811 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 67 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 272 |
| 1 - 5 Mbps | 459 |
| 0.25 - 1 Mbps | 42 |
| < 0.25 Mbps | 0 |
| unmeasured | 105 |

Latency (phase-1 HTTPS round trip): median **683 ms**, p90 **2837 ms**. 26 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

184 active, 70 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2870 | 440 | 46 |
| `HP` | url | 572 | 426 | 0 |
| `SK` | url | 922 | 379 | 0 |
| `HC` | url | 1767 | 372 | 1 |
| `NK` | url | 874 | 347 | 0 |
| `ST-VL` | url | 2781 | 304 | 123 |
| `F0` | url | 470 | 295 | 0 |
| `EV` | url | 432 | 278 | 0 |
| `Ni` | url | 403 | 264 | 0 |
| `SB-VL` | url | 2398 | 205 | 0 |
| `ET` | url | 385 | 198 | 0 |
| `RD-SS` | url | 545 | 196 | 0 |
| `SB` | url | 2627 | 193 | 1 |
| `KA` | url | 2095 | 172 | 0 |
| `AG-PL` | url | 369 | 137 | 47 |
| `EV-SS` | url | 157 | 131 | 0 |
| `EV-VL` | url | 218 | 125 | 0 |
| `WU` | url | 219 | 121 | 11 |
| `RD-VM` | url | 547 | 104 | 2 |
| `EP-ALL` | url | 1289 | 93 | 2 |

## History

working per run (last 13): ▁▁▆▆▇█▇▆▇█▇▆▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (878) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (811) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (67) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **80% unreachable** and **80% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

