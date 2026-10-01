# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-01 17:35:23 UTC** — 181117 unique proxies collected from 137/137 URL sources and 49/49 Telegram channels; **4500** endpoints really tested, **861** reachable, **794** verified working (egress IP confirmed changed) across **49 exit countries**.

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

All 794 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `hysteria2` | `155.248.209.237:33333` | United States | 78 ms | 58.6 Mbps | singbox |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.38.85:42942` | United States | 353 ms | 55.2 Mbps | xray |
| 3 | #3 ❓ ?? → 🇺🇸 US | `vless` | `3h-unitedstates3.09vpn.com:8443` | United States | 231 ms | 53.5 Mbps | singbox |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.43.210:53957` | United States | 62 ms | 52.0 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `trojan` | `43.173.90.202:443` | United States | 46 ms | 49.6 Mbps | singbox |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `vless` | `172.233.139.46:53734` | United States | 61 ms | 48.3 Mbps | xray |
| 7 | #7 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.24.131:8080` | United States | 87 ms | 47.8 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `vless` | `167.17.68.205:443` | United States | 65 ms | 44.8 Mbps | xray |
| 9 | #9 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.123266.xyz:33333` | United States | 109 ms | 42.4 Mbps | singbox |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 93 ms | 39.8 Mbps | singbox |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `ss` | `5.78.51.123:1080` | United States | 69 ms | 37.5 Mbps | xray |
| 12 | #12 🇨🇦 CA → 🇺🇸 US | `vless` | `188.114.97.6:2095` | United States | 107 ms | 37.5 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 352 ms | 37.2 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.198:23576` | United States | 86 ms | 36.5 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.209:23576` | United States | 94 ms | 36.3 Mbps | xray |
| 16 | #16 🇨🇦 CA → 🇺🇸 US | `vless` | `188.114.97.6:2082` | United States | 118 ms | 36.3 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.197:23576` | United States | 89 ms | 35.0 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.195:23576` | United States | 88 ms | 34.8 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.214:23576` | United States | 98 ms | 34.6 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.206:23576` | United States | 414 ms | 34.5 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.0.177:8388` | United States | 330 ms | 34.5 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.219:23576` | United States | 100 ms | 34.3 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `51.81.203.63:443` | United States | 408 ms | 33.7 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.216:23576` | United States | 98 ms | 33.7 Mbps | xray |
| 25 | #25 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.47.113:2095` | United States | 87 ms | 31.6 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 49 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 250 | 14.9 Mbps | 40 ms | 31% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 131 | 3.8 Mbps | 471 ms | 16% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 57 | 3.4 Mbps | 466 ms | 7% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇸🇬 Singapore | 39 | 3.6 Mbps | 514 ms | 5% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇭🇰 Hong Kong | 28 | 3.4 Mbps | 477 ms | 4% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇨🇦 Canada | 24 | 8.0 Mbps | 89 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇯🇵 Japan | 24 | 4.4 Mbps | 325 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇫🇷 France | 24 | 3.6 Mbps | 605 ms | 3% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇬🇧 United Kingdom | 23 | 4.2 Mbps | 440 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇵🇱 Poland | 18 | 3.0 Mbps | 689 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇰🇷 South Korea | 17 | 4.5 Mbps | 507 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇫🇮 Finland | 15 | 2.7 Mbps | 538 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇸🇪 Sweden | 13 | 3.0 Mbps | 697 ms | 2% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇪🇸 Spain | 12 | 4.5 Mbps | 350 ms | 2% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇦🇺 Australia | 11 | 12.0 Mbps | 80 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇷🇸 Serbia | 10 | 3.4 Mbps | 961 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇳 India | 10 | 1.0 Mbps | 971 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇷🇺 Russia | 8 | 2.3 Mbps | 1335 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇧🇬 Bulgaria | 8 | 3.4 Mbps | 828 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇰🇿 Kazakhstan | 7 | 1.4 Mbps | 1228 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇮🇹 Italy | 6 | 2.7 Mbps | 617 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇹🇷 Turkey | 5 | 1.7 Mbps | 1035 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇦🇹 Austria | 4 | 4.6 Mbps | 527 ms | 1% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇹🇼 Taiwan | 4 | 3.7 Mbps | 522 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇪🇪 Estonia | 4 | 3.7 Mbps | 662 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇱🇰 LK | 4 | 2.0 Mbps | 1364 ms | 1% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇳🇴 Norway | 4 | 1.8 Mbps | 1714 ms | 1% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇮🇪 Ireland | 3 | 4.7 Mbps | 391 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇨🇭 Switzerland | 3 | 4.2 Mbps | 558 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇿🇦 South Africa | 3 | 2.8 Mbps | 981 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇲🇩 Moldova | 3 | 1.7 Mbps | 1117 ms | 0% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇲🇾 Malaysia | 2 | 4.6 Mbps | 717 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇷🇴 Romania | 2 | 3.9 Mbps | 1020 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇬🇷 Greece | 2 | 3.8 Mbps | 889 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇦🇪 UAE | 2 | 1.6 Mbps | 1114 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇬🇹 GT | 1 | 7.8 Mbps | 594 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇨🇴 Colombia | 1 | 6.9 Mbps | 545 ms | 0% | [`CO.txt`](subs/by-country/CO.txt) |
| 🇭🇺 Hungary | 1 | 4.8 Mbps | 613 ms | 0% | [`HU.txt`](subs/by-country/HU.txt) |
| 🇵🇹 Portugal | 1 | 4.4 Mbps | 561 ms | 0% | [`PT.txt`](subs/by-country/PT.txt) |
| 🇵🇭 Philippines | 1 | 3.8 Mbps | 877 ms | 0% | [`PH.txt`](subs/by-country/PH.txt) |
| 🇹🇭 Thailand | 1 | 3.8 Mbps | 693 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇱🇻 Latvia | 1 | 3.6 Mbps | 782 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.2 Mbps | 1341 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.2 Mbps | 2171 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇧🇾 BY | 1 | 0.7 Mbps | 1925 ms | 0% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇨🇳 China | 1 | - | 1947 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇨🇾 Cyprus | 1 | - | 2120 ms | 0% | [`CY.txt`](subs/by-country/CY.txt) |
| 🇮🇩 Indonesia | 1 | - | 2263 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇩🇰 Denmark | 1 | - | 5943 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3100 | 532 | 488 | 17% |
| `ss` | 563 | 197 | 185 | 35% |
| `vmess` | 692 | 103 | 98 | 15% |
| `hysteria2` | 25 | 13 | 13 | 52% |
| `trojan` | 116 | 16 | 10 | 14% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 716 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 78 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 228 |
| 1 - 5 Mbps | 382 |
| 0.25 - 1 Mbps | 38 |
| < 0.25 Mbps | 0 |
| unmeasured | 146 |

Latency (phase-1 HTTPS round trip): median **714 ms**, p90 **4381 ms**. 67 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

185 active, 69 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2876 | 414 | 14 |
| `HP` | url | 569 | 396 | 0 |
| `SK` | url | 918 | 354 | 24 |
| `HC` | url | 1780 | 350 | 0 |
| `NK` | url | 872 | 327 | 0 |
| `F0` | url | 466 | 273 | 0 |
| `ST-VL` | url | 2778 | 271 | 287 |
| `EV` | url | 433 | 269 | 0 |
| `Ni` | url | 402 | 252 | 0 |
| `ET` | url | 380 | 185 | 0 |
| `RD-SS` | url | 539 | 184 | 1 |
| `SB-VL` | url | 2394 | 180 | 0 |
| `KA` | url | 2128 | 160 | 0 |
| `SB` | url | 2621 | 153 | 1 |
| `AG-PL` | url | 372 | 126 | 31 |
| `EV-SS` | url | 157 | 126 | 0 |
| `EV-VL` | url | 218 | 123 | 0 |
| `WU` | url | 214 | 108 | 0 |
| `RD` | url | 126 | 94 | 0 |
| `RD-VM` | url | 542 | 94 | 0 |

## History

working per run (last 12): ▁▁▆▆▇█▇▆▇█▇▆

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (794) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (716) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (78) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (49 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

