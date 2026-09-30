# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-09-30 21:34:58 UTC** — 173808 unique proxies collected from 173/173 URL sources and 81/81 Telegram channels; **4500** endpoints really tested, **899** reachable, **866** verified working (egress IP confirmed changed) across **51 exit countries**.

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

All 866 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.95.3:18000` | Australia | 358 ms | 69.4 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 145 ms | 68.5 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 46 ms | 67.1 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vmess` | `172.111.38.100:22324` | United States | 53 ms | 65.1 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:22324` | United States | 449 ms | 64.8 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.96.21:8081` | United States | 444 ms | 60.2 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `185.95.231.233:443` | United States | 84 ms | 57.5 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 373 ms | 57.0 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.133:443` | United States | 365 ms | 55.2 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `195.123.235.177:443` | United States | 55 ms | 55.1 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.104.144:8081` | United States | 465 ms | 54.1 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.231:443` | United States | 1037 ms | 44.6 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `hysteria2` | `159.223.157.129:8443` | United States | 107 ms | 43.9 Mbps | singbox |
| 14 | #14 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.43.187:2095` | United States | 39 ms | 43.7 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.74:443` | United States | 7292 ms | 42.0 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.247.206:4444` | United States | 70 ms | 39.3 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 317 ms | 39.2 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vmess` | `167.88.63.59:22324` | United States | 56 ms | 38.8 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.173:443` | United States | 430 ms | 36.2 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.163:443` | United States | 150 ms | 36.1 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.232:443` | United States | 124 ms | 35.5 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.95:443` | United States | 76 ms | 34.7 Mbps | xray |
| 23 | #23 🇨🇦 CA → 🇨🇦 CA | `vless` | `66.70.179.198:2053` | Canada | 123 ms | 34.3 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vmess` | `216.106.183.35:22324` | United States | 72 ms | 32.2 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.184:443` | United States | 196 ms | 31.9 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 51 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 256 | 15.8 Mbps | 27 ms | 30% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 146 | 7.2 Mbps | 272 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 59 | 6.7 Mbps | 296 ms | 7% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 53 | 4.8 Mbps | 360 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇨🇦 Canada | 30 | 15.9 Mbps | 80 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇸🇬 Singapore | 30 | 3.0 Mbps | 777 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇭🇰 Hong Kong | 29 | 2.7 Mbps | 190 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇬🇧 United Kingdom | 28 | 5.8 Mbps | 270 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇯🇵 Japan | 23 | 3.6 Mbps | 482 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇰🇷 South Korea | 18 | 4.0 Mbps | 630 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇵🇱 Poland | 17 | 4.9 Mbps | 412 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇮🇳 India | 15 | 2.3 Mbps | 572 ms | 2% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇦🇺 Australia | 12 | 17.3 Mbps | 132 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇪🇸 Spain | 12 | 7.0 Mbps | 125 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇫🇮 Finland | 12 | 4.5 Mbps | 409 ms | 1% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇮🇹 Italy | 11 | 5.5 Mbps | 318 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇸🇪 Sweden | 10 | 5.4 Mbps | 445 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇷🇸 Serbia | 10 | 5.1 Mbps | 649 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇧🇬 Bulgaria | 8 | 5.0 Mbps | 501 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇷🇺 Russia | 8 | 1.3 Mbps | 576 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇲🇩 Moldova | 7 | 2.4 Mbps | 771 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇳🇴 Norway | 6 | 5.3 Mbps | 599 ms | 1% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇹🇷 Turkey | 6 | 4.3 Mbps | 424 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇹🇼 Taiwan | 5 | 3.1 Mbps | 639 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇦🇹 Austria | 4 | 7.5 Mbps | 360 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇺🇦 Ukraine | 4 | 3.4 Mbps | 524 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇪🇪 Estonia | 4 | 6.2 Mbps | 421 ms | 0% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇱🇰 LK | 4 | 4.1 Mbps | 997 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇰🇿 Kazakhstan | 4 | 2.9 Mbps | 1294 ms | 0% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇨🇭 Switzerland | 3 | 6.5 Mbps | 396 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇮🇪 Ireland | 3 | 6.7 Mbps | 213 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇷🇴 Romania | 3 | 5.4 Mbps | 605 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇿🇦 South Africa | 3 | 3.4 Mbps | 819 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇦🇩 AD | 2 | 6.1 Mbps | 434 ms | 0% | [`AD.txt`](subs/by-country/AD.txt) |
| 🇹🇭 Thailand | 2 | 2.7 Mbps | 861 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇦🇪 UAE | 2 | 2.3 Mbps | 897 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇸🇰 Slovakia | 2 | - | 629 ms | 0% | [`SK.txt`](subs/by-country/SK.txt) |
| 🇲🇾 Malaysia | 2 | - | 981 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇬🇹 GT | 1 | 9.0 Mbps | 340 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇬🇷 Greece | 1 | 5.6 Mbps | 589 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇱🇻 Latvia | 1 | 5.0 Mbps | 833 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇬🇪 Georgia | 1 | 4.2 Mbps | 1045 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.5 Mbps | 1068 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇵🇭 Philippines | 1 | 3.1 Mbps | 1092 ms | 0% | [`PH.txt`](subs/by-country/PH.txt) |
| 🇦🇲 Armenia | 1 | 2.0 Mbps | 2047 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇮🇩 Indonesia | 1 | 0.6 Mbps | 8379 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇨🇱 Chile | 1 | - | 466 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇱🇹 Lithuania | 1 | - | 642 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇧🇷 Brazil | 1 | - | 839 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇦🇷 Argentina | 1 | - | 973 ms | 0% | [`AR.txt`](subs/by-country/AR.txt) |
| 🇨🇳 China | 1 | - | 5146 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2988 | 540 | 516 | 18% |
| `ss` | 540 | 198 | 193 | 37% |
| `vmess` | 815 | 108 | 104 | 13% |
| `trojan` | 120 | 41 | 41 | 34% |
| `hysteria2` | 33 | 12 | 12 | 36% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 811 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 55 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 499 |
| 1 - 5 Mbps | 220 |
| 0.25 - 1 Mbps | 29 |
| < 0.25 Mbps | 0 |
| unmeasured | 118 |

Latency (phase-1 HTTPS round trip): median **530 ms**, p90 **2431 ms**. 33 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

254 active, 0 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2782 | 438 | 246 |
| `HP` | url | 543 | 424 | 1 |
| `SK` | url | 784 | 377 | 30 |
| `HC` | url | 1720 | 368 | 1 |
| `NK` | url | 763 | 355 | 0 |
| `F0` | url | 438 | 313 | 0 |
| `ST-VL` | url | 2700 | 312 | 68 |
| `EV` | url | 439 | 277 | 0 |
| `Ni` | url | 347 | 250 | 5 |
| `SB-VL` | url | 2359 | 207 | 0 |
| `SB` | url | 2591 | 199 | 2 |
| `RD-SS` | url | 514 | 192 | 2 |
| `ET` | url | 329 | 176 | 0 |
| `KA` | url | 2387 | 160 | 0 |
| `EV-SS` | url | 157 | 131 | 0 |
| `AG-PL` | url | 369 | 128 | 38 |
| `EV-VL` | url | 216 | 124 | 0 |
| `WU` | url | 180 | 110 | 13 |
| `RD-VM` | url | 597 | 102 | 5 |
| `EP-ALL` | url | 1403 | 96 | 0 |

## History

working per run (last 9): ▁▁▇▇██▇▇█

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (866) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (811) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (55) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (51 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

