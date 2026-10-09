# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-09 21:55:30 UTC** — 161739 unique proxies collected from 115/115 URL sources and 13/13 Telegram channels; **4506** endpoints really tested, **966** reachable, **935** verified working (egress IP confirmed changed) across **45 exit countries**.

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

All 935 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 300 ms | 51.9 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 314 ms | 49.8 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 301 ms | 46.1 Mbps | xray |
| 4 | #4 ❓ ?? → 🇺🇸 US | `ss` | `45.76.9.57:8393` | United States | 3143 ms | 43.3 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 165 ms | 43.1 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.212:443` | United States | 2802 ms | 41.3 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.231:443` | United States | 927 ms | 40.7 Mbps | xray |
| 8 | #8 ❓ ?? → 🇺🇸 US | `vless` | `185.95.231.156:443` | United States | 274 ms | 40.1 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.74:443` | United States | 3684 ms | 39.6 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.15:443` | United States | 196 ms | 37.5 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.233.41:8882` | United States | 290 ms | 37.2 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.95.3:18000` | Australia | 392 ms | 37.0 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.89:443` | United States | 4740 ms | 36.4 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 174 ms | 32.8 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `137.184.218.169:36925` | United States | 173 ms | 31.9 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.168:443` | United States | 159 ms | 31.0 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.235:443` | United States | 233 ms | 30.2 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.90:443` | United States | 177 ms | 29.2 Mbps | xray |
| 19 | #19 ❓ ?? → 🇺🇸 US | `vless` | `1579e6d9-6b57-4fb1-b080-9c9a6da46ae5.fly.dev:443` | United States | 835 ms | 27.7 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.225:443` | United States | 137 ms | 26.5 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.133:443` | United States | 159 ms | 26.4 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.223:443` | United States | 3060 ms | 26.3 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.52:443` | United States | 99 ms | 25.5 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.163:443` | United States | 358 ms | 25.0 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.95:443` | United States | 200 ms | 24.7 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 45 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇳🇱 Netherlands | 169 | 7.0 Mbps | 305 ms | 18% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇺🇸 United States | 152 | 14.7 Mbps | 49 ms | 16% | [`US.txt`](subs/by-country/US.txt) |
| 🇩🇪 Germany | 108 | 5.7 Mbps | 276 ms | 12% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇯🇵 Japan | 67 | 3.8 Mbps | 494 ms | 7% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇫🇷 France | 59 | 4.5 Mbps | 339 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇸🇬 Singapore | 44 | 2.7 Mbps | 726 ms | 5% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇰🇷 South Korea | 41 | 3.2 Mbps | 631 ms | 4% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇵🇱 Poland | 33 | 4.8 Mbps | 472 ms | 4% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 25 | 4.6 Mbps | 374 ms | 3% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇬🇧 United Kingdom | 24 | 6.3 Mbps | 293 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇭🇰 Hong Kong | 23 | 2.7 Mbps | 629 ms | 2% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇨🇦 Canada | 20 | 10.0 Mbps | 92 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇧🇬 Bulgaria | 12 | 4.8 Mbps | 580 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇦🇺 Australia | 11 | 13.6 Mbps | 149 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇪🇪 Estonia | 11 | 4.9 Mbps | 434 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇮🇳 India | 11 | 1.9 Mbps | 782 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇮🇪 Ireland | 10 | 5.8 Mbps | 244 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇹🇷 Turkey | 10 | 3.8 Mbps | 534 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇷🇸 Serbia | 10 | 4.9 Mbps | 658 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇧🇾 BY | 9 | 3.2 Mbps | 842 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇸🇪 Sweden | 7 | 6.4 Mbps | 367 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇪🇸 Spain | 6 | 7.0 Mbps | 390 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇮🇹 Italy | 6 | 6.5 Mbps | 350 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇱🇻 Latvia | 6 | 4.9 Mbps | 529 ms | 1% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇷🇴 Romania | 6 | 4.2 Mbps | 514 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇲🇩 Moldova | 6 | 3.5 Mbps | 825 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇰🇿 Kazakhstan | 5 | 2.3 Mbps | 1483 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇹🇼 Taiwan | 5 | 3.2 Mbps | 667 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇹🇭 Thailand | 5 | 2.6 Mbps | 860 ms | 1% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇨🇭 Switzerland | 4 | 6.0 Mbps | 462 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇦🇹 Austria | 4 | 6.2 Mbps | 382 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇿🇦 South Africa | 4 | 3.3 Mbps | 807 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇮🇩 Indonesia | 4 | 1.5 Mbps | 979 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇷🇺 Russia | 3 | 4.4 Mbps | 663 ms | 0% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇳🇴 Norway | 2 | 4.7 Mbps | 1736 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇨🇿 Czechia | 2 | 3.7 Mbps | 588 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇲🇾 Malaysia | 2 | 3.3 Mbps | 747 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇦🇪 UAE | 2 | 2.9 Mbps | 871 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇬🇷 Greece | 1 | 5.5 Mbps | 594 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.6 Mbps | 1050 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇱🇺 Luxembourg | 1 | 3.2 Mbps | 4097 ms | 0% | [`LU.txt`](subs/by-country/LU.txt) |
| 🇦🇲 Armenia | 1 | 2.1 Mbps | 2107 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇻🇳 Vietnam | 1 | 2.1 Mbps | 1269 ms | 0% | [`VN.txt`](subs/by-country/VN.txt) |
| 🇮🇱 Israel | 1 | - | 836 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |
| 🇨🇱 Chile | 1 | - | 891 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2676 | 490 | 464 | 18% |
| `ss` | 460 | 201 | 201 | 44% |
| `trojan` | 262 | 144 | 144 | 55% |
| `vmess` | 1020 | 80 | 75 | 8% |
| `hysteria2` | 84 | 49 | 49 | 58% |
| `tuic` | 2 | 2 | 2 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 825 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 110 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 466 |
| 1 - 5 Mbps | 335 |
| 0.25 - 1 Mbps | 34 |
| < 0.25 Mbps | 0 |
| unmeasured | 100 |

Latency (phase-1 HTTPS round trip): median **682 ms**, p90 **2623 ms**. 31 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

128 active, 126 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 1022 | 603 | 6334 |
| `SK` | url | 947 | 534 | 0 |
| `HP` | url | 475 | 424 | 123 |
| `Ni` | url | 400 | 318 | 191 |
| `RD-VL` | url | 2294 | 284 | 4101 |
| `F0` | url | 302 | 278 | 100 |
| `ET` | url | 340 | 264 | 2755 |
| `AG-PL` | url | 557 | 251 | 1439 |
| `HC` | url | 1325 | 238 | 180 |
| `EV` | url | 404 | 206 | 0 |
| `RD-SS` | url | 428 | 200 | 281 |
| `ST-VL` | url | 2188 | 190 | 683 |
| `KA` | url | 1783 | 157 | 5734 |
| `SB-VL` | url | 1979 | 131 | 171 |
| `EV-SS` | url | 153 | 124 | 63 |
| `SB` | url | 2296 | 117 | 2 |
| `AQ` | url | 163 | 91 | 566 |
| `TK` | url | 129 | 89 | 0 |
| `RO` | url | 93 | 85 | 1 |
| `EB2` | url | 157 | 82 | 0 |

## History

working per run (last 30): ▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇▇▇▇▇█▆▇█▇▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-10-03 11:04 | 4500 | 899 | 860 | 8.7M | 82.3M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (935) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (825) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (110) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (45 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

