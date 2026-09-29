# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-09-29 21:34:22 UTC** — 164268 unique proxies collected from 173/173 URL sources and 81/81 Telegram channels; **4500** endpoints really tested, **880** reachable, **852** verified working (egress IP confirmed changed) across **50 exit countries**.

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

All 852 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇨🇦 CA → 🇨🇦 CA | `ss` | `149.22.95.183:443` | Canada | 152 ms | 61.8 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `5.78.51.123:1080` | United States | 207 ms | 58.0 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.219:23576` | United States | 317 ms | 57.2 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.197:23576` | United States | 124 ms | 55.4 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇦🇺 AU | `vmess` | `84.17.41.2:18000` | Australia | 50 ms | 28.2 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.206:23576` | United States | 59 ms | 26.8 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.209:23576` | United States | 70 ms | 25.9 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 184 ms | 25.0 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.216:23576` | United States | 74 ms | 24.8 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 156 ms | 24.2 Mbps | singbox |
| 11 | #11 🇨🇦 CA → 🇺🇸 US | `vless` | `188.114.97.6:2086` | United States | 125 ms | 24.1 Mbps | xray |
| 12 | #12 🇨🇦 CA → 🇨🇦 CA | `vmess` | `158.51.123.42:22324` | Canada | 111 ms | 23.5 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.198:23576` | United States | 57 ms | 23.3 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.195:23576` | United States | 63 ms | 23.3 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vmess` | `216.106.185.141:22324` | United States | 156 ms | 23.3 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `108.162.198.178:2086` | United States | 124 ms | 22.8 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `15.204.97.214:23576` | United States | 89 ms | 22.3 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `51.81.203.63:443` | United States | 103 ms | 22.1 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `192.3.247.109:43578` | United States | 147 ms | 21.8 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.38.85:42942` | United States | 142 ms | 21.7 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `ss` | `192.3.247.109:43579` | United States | 148 ms | 21.5 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `108.162.198.178:80` | United States | 437 ms | 21.4 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `192.3.247.109:32132` | United States | 153 ms | 21.4 Mbps | xray |
| 24 | #24 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.234:8080` | United States | 121 ms | 20.9 Mbps | xray |
| 25 | #25 ❓ ?? → 🇺🇸 US | `vless` | `ww13.levikogjgfdd.ir:23576` | United States | 289 ms | 20.8 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 50 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 226 | 12.2 Mbps | 37 ms | 27% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 141 | 4.5 Mbps | 424 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇫🇷 France | 69 | 3.2 Mbps | 585 ms | 8% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇩🇪 Germany | 60 | 4.1 Mbps | 459 ms | 7% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇭🇰 Hong Kong | 32 | 3.4 Mbps | 455 ms | 4% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇬🇧 United Kingdom | 31 | 4.2 Mbps | 412 ms | 4% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇸🇬 Singapore | 28 | 3.5 Mbps | 664 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇨🇦 Canada | 25 | 10.0 Mbps | 111 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇯🇵 Japan | 24 | 4.8 Mbps | 308 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇰🇷 South Korea | 20 | 4.5 Mbps | 459 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇵🇱 Poland | 17 | 3.0 Mbps | 704 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 16 | 3.1 Mbps | 668 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇸🇪 Sweden | 15 | 2.8 Mbps | 619 ms | 2% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇮🇳 India | 13 | 2.5 Mbps | 715 ms | 2% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇦🇺 Australia | 12 | 11.2 Mbps | 50 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇪🇸 Spain | 10 | 4.7 Mbps | 366 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇮🇹 Italy | 10 | 3.2 Mbps | 493 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇸 Serbia | 9 | 3.4 Mbps | 933 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇧🇬 Bulgaria | 8 | 3.3 Mbps | 918 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇷🇺 Russia | 7 | 1.8 Mbps | 1050 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇲🇩 Moldova | 7 | 2.5 Mbps | 1077 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇰🇿 Kazakhstan | 7 | 1.9 Mbps | 1797 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇦🇹 Austria | 5 | 4.7 Mbps | 562 ms | 1% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇹🇼 Taiwan | 5 | 2.3 Mbps | 527 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇪🇪 Estonia | 5 | 3.6 Mbps | 641 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇹🇷 Turkey | 5 | 2.7 Mbps | 730 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇳🇴 Norway | 4 | 4.2 Mbps | 655 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇺🇦 Ukraine | 4 | 3.6 Mbps | 643 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇷🇴 Romania | 4 | 2.9 Mbps | 853 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇱🇰 LK | 3 | 3.4 Mbps | 1232 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇱🇹 Lithuania | 3 | 3.3 Mbps | 984 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇿🇦 South Africa | 3 | 2.4 Mbps | 1019 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇮🇪 Ireland | 2 | 4.4 Mbps | 746 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇨🇭 Switzerland | 2 | 2.8 Mbps | 649 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇹🇭 Thailand | 2 | 3.3 Mbps | 682 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇦🇪 UAE | 2 | 2.5 Mbps | 1100 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇦🇩 AD | 2 | 2.3 Mbps | 3326 ms | 0% | [`AD.txt`](subs/by-country/AD.txt) |
| 🇸🇰 Slovakia | 2 | - | 887 ms | 0% | [`SK.txt`](subs/by-country/SK.txt) |
| 🇬🇹 GT | 1 | 5.8 Mbps | 530 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇱🇻 Latvia | 1 | 4.2 Mbps | 880 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇬🇪 Georgia | 1 | 2.9 Mbps | 4269 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇸🇦 Saudi Arabia | 1 | 2.7 Mbps | 1216 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.4 Mbps | 2021 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇩🇰 Denmark | 1 | 1.0 Mbps | 1485 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |
| 🇮🇩 Indonesia | 1 | 0.9 Mbps | 1206 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇨🇳 China | 1 | - | 642 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇧🇷 Brazil | 1 | - | 1092 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇦🇷 Argentina | 1 | - | 1147 ms | 0% | [`AR.txt`](subs/by-country/AR.txt) |
| 🇲🇾 Malaysia | 1 | - | 1593 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇨🇱 Chile | 1 | - | 1692 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2818 | 512 | 489 | 18% |
| `ss` | 489 | 195 | 194 | 40% |
| `vmess` | 1057 | 106 | 102 | 10% |
| `trojan` | 95 | 54 | 54 | 57% |
| `hysteria2` | 37 | 13 | 13 | 35% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 802 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 50 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 288 |
| 1 - 5 Mbps | 393 |
| 0.25 - 1 Mbps | 33 |
| < 0.25 Mbps | 0 |
| unmeasured | 138 |

Latency (phase-1 HTTPS round trip): median **720 ms**, p90 **2994 ms**. 28 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

254 active, 0 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `HP` | url | 502 | 429 | 0 |
| `RD-VL` | url | 2632 | 407 | 115 |
| `HC` | url | 1650 | 373 | 5 |
| `SK` | url | 665 | 368 | 0 |
| `NK` | url | 643 | 346 | 41 |
| `F0` | url | 406 | 330 | 0 |
| `EV` | url | 428 | 304 | 0 |
| `ST-VL` | url | 2571 | 296 | 23 |
| `Ni` | url | 300 | 236 | 0 |
| `RD-SS` | url | 447 | 192 | 0 |
| `SB-VL` | url | 2270 | 186 | 0 |
| `ET` | url | 269 | 177 | 0 |
| `SB` | url | 2454 | 160 | 295 |
| `KA` | url | 2746 | 150 | 0 |
| `EV-SS` | url | 156 | 131 | 0 |
| `EV-VL` | url | 209 | 130 | 0 |
| `AG-PL` | url | 331 | 119 | 82 |
| `WU` | url | 152 | 116 | 9 |
| `RD-VM` | url | 653 | 99 | 0 |
| `YA-VL` | url | 533 | 79 | 117 |

## History

working per run (last 5): ▁▁███

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
| 2026-09-29 21:53 | 4500 | 880 | 852 | 6.5M | 61.8M |
| 2026-09-29 15:48 | 4500 | 839 | 796 | 6.7M | 51.3M |
| 2026-09-29 14:48 | 4500 | 799 | 756 | 6.9M | 52.1M |
| 2026-09-29 14:12 | 4500 | 0 | 0 | - | - |
| 2026-09-29 13:39 | 0 | 0 | 0 | - | - |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (852) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (802) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (50) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (50 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

