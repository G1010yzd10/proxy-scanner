# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-08 12:19:58 UTC** — 158653 unique proxies collected from 133/133 URL sources and 47/47 Telegram channels; **4504** endpoints really tested, **827** reachable, **775** verified working (egress IP confirmed changed) across **47 exit countries**.

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

All 775 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 248 ms | 67.7 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.95.3:18000` | Australia | 2572 ms | 60.1 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 174 ms | 59.9 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 177 ms | 58.8 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 163 ms | 58.6 Mbps | xray |
| 6 | #6 ❓ ?? → 🇺🇸 US | `ss` | `216.52.183.174:17036` | United States | 293 ms | 56.1 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `137.184.218.169:36925` | United States | 447 ms | 49.2 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.163:443` | United States | 3648 ms | 47.9 Mbps | xray |
| 9 | #9 ❓ ?? → 🇺🇸 US | `vless` | `fs.koomeh.net:443` | United States | 397 ms | 46.3 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.95:443` | United States | 409 ms | 45.6 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.225:443` | United States | 572 ms | 40.5 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.224:443` | United States | 1211 ms | 38.3 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `2.24.124.64:443` | United States | 409 ms | 36.9 Mbps | xray |
| 14 | #14 🇨🇦 CA → 🇨🇦 CA | `vless` | `66.70.179.198:2053` | Canada | 431 ms | 36.1 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.202:443` | United States | 142 ms | 32.2 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `147.182.212.232:56565` | United States | 50 ms | 29.5 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `167.17.69.171:443` | United States | 126 ms | 28.2 Mbps | xray |
| 18 | #18 ❓ ?? → 🇺🇸 US | `vless` | `185.95.231.156:443` | United States | 91 ms | 26.8 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.168:443` | United States | 74 ms | 26.5 Mbps | xray |
| 20 | #20 ❓ ?? → 🇺🇸 US | `vless` | `ww9.levikogjgfdd.ir:36925` | United States | 58 ms | 24.7 Mbps | xray |
| 21 | #21 🇨🇦 CA → 🇨🇦 CA | `vless` | `209.200.246.148:443` | Canada | 189 ms | 23.8 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.15:443` | United States | 262 ms | 23.5 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.75:443` | United States | 116 ms | 23.1 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 50 ms | 22.7 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.247.206:4444` | United States | 100 ms | 21.9 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 47 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇳🇱 Netherlands | 158 | 6.6 Mbps | 273 ms | 20% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇺🇸 United States | 145 | 13.3 Mbps | 40 ms | 19% | [`US.txt`](subs/by-country/US.txt) |
| 🇩🇪 Germany | 86 | 5.0 Mbps | 282 ms | 11% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇯🇵 Japan | 53 | 3.0 Mbps | 489 ms | 7% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇸🇬 Singapore | 31 | 2.0 Mbps | 891 ms | 4% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇰🇷 South Korea | 30 | 2.9 Mbps | 661 ms | 4% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇫🇷 France | 27 | 5.1 Mbps | 367 ms | 3% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇭🇰 Hong Kong | 26 | 2.9 Mbps | 619 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇵🇱 Poland | 23 | 4.7 Mbps | 439 ms | 3% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇬🇧 United Kingdom | 21 | 6.0 Mbps | 278 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇫🇮 Finland | 21 | 4.4 Mbps | 409 ms | 3% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇨🇦 Canada | 16 | 9.4 Mbps | 80 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇦🇺 Australia | 12 | 15.6 Mbps | 228 ms | 2% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇷🇸 Serbia | 10 | 5.0 Mbps | 644 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇮🇳 India | 10 | 2.7 Mbps | 375 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇸🇪 Sweden | 9 | 6.1 Mbps | 417 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇧🇬 Bulgaria | 9 | 4.7 Mbps | 641 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇮🇪 Ireland | 7 | 6.5 Mbps | 228 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇰🇿 Kazakhstan | 6 | 2.4 Mbps | 1709 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇧🇾 BY | 6 | 1.7 Mbps | 2948 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇮🇹 Italy | 5 | 6.9 Mbps | 327 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇪🇪 Estonia | 5 | 5.4 Mbps | 410 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇹🇷 Turkey | 5 | 3.3 Mbps | 681 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇹🇼 Taiwan | 5 | 2.6 Mbps | 684 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇷🇺 Russia | 4 | 4.4 Mbps | 357 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇨🇭 Switzerland | 4 | 6.8 Mbps | 483 ms | 1% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇪🇸 Spain | 4 | 6.3 Mbps | 489 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇳🇴 Norway | 4 | 3.0 Mbps | 421 ms | 1% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇲🇩 Moldova | 4 | 2.9 Mbps | 789 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇿🇦 South Africa | 4 | 2.9 Mbps | 865 ms | 1% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇮🇩 Indonesia | 3 | 1.0 Mbps | 1283 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇲🇽 Mexico | 2 | 5.5 Mbps | 408 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇦🇹 Austria | 2 | 6.8 Mbps | 374 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇷🇴 Romania | 2 | 5.9 Mbps | 678 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇱🇻 Latvia | 2 | 5.9 Mbps | 572 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇹🇭 Thailand | 2 | 1.2 Mbps | 1015 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇦🇪 UAE | 2 | 0.7 Mbps | 1116 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇦🇱 AL | 1 | 6.6 Mbps | 553 ms | 0% | [`AL.txt`](subs/by-country/AL.txt) |
| 🇺🇦 Ukraine | 1 | 6.5 Mbps | 721 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇬🇷 Greece | 1 | 5.6 Mbps | 593 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇸🇦 Saudi Arabia | 1 | 4.6 Mbps | 1195 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇨🇿 Czechia | 1 | 4.5 Mbps | 993 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇻🇳 Vietnam | 1 | 2.6 Mbps | 1858 ms | 0% | [`VN.txt`](subs/by-country/VN.txt) |
| 🇦🇲 Armenia | 1 | 2.3 Mbps | 2044 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇨🇱 Chile | 1 | - | 656 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇲🇾 Malaysia | 1 | - | 956 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇮🇱 Israel | 1 | - | 1036 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2835 | 441 | 407 | 16% |
| `ss` | 487 | 200 | 193 | 41% |
| `trojan` | 219 | 84 | 79 | 38% |
| `vmess` | 902 | 71 | 65 | 8% |
| `hysteria2` | 57 | 30 | 30 | 53% |
| `tuic` | 1 | 1 | 1 | 100% |
| `http` | 3 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 696 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 79 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 358 |
| 1 - 5 Mbps | 253 |
| 0.25 - 1 Mbps | 37 |
| < 0.25 Mbps | 0 |
| unmeasured | 127 |

Latency (phase-1 HTTPS round trip): median **684 ms**, p90 **3816 ms**. 52 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

179 active, 75 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 875 | 461 | 4764 |
| `SK` | url | 818 | 409 | 218 |
| `Ni` | url | 433 | 310 | 176 |
| `HP` | url | 378 | 299 | 91 |
| `ET` | url | 359 | 274 | 2536 |
| `F0` | url | 370 | 265 | 101 |
| `RD-VL` | url | 2466 | 260 | 4430 |
| `HC` | url | 1436 | 217 | 111 |
| `EV` | url | 424 | 204 | 15 |
| `ST-VL` | url | 2425 | 198 | 691 |
| `RD-SS` | url | 447 | 192 | 310 |
| `KA` | url | 1544 | 126 | 5198 |
| `EV-SS` | url | 155 | 123 | 54 |
| `AG-PL` | url | 428 | 120 | 1117 |
| `SB-VL` | url | 2139 | 120 | 0 |
| `AN` | url | 113 | 110 | 0 |
| `WD` | url | 98 | 92 | 140 |
| `SB` | url | 2395 | 84 | 2 |
| `RO` | url | 86 | 75 | 1 |
| `TK` | url | 130 | 73 | 0 |

## History

working per run (last 28): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇▇▇▇▇█▆

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-10-03 02:52 | 4500 | 1062 | 1030 | 8.0M | 75.5M |
| 2026-10-02 21:49 | 4500 | 890 | 861 | 8.9M | 68.7M |
| 2026-10-02 17:14 | 4500 | 847 | 807 | 8.6M | 88.1M |
| 2026-10-02 11:49 | 4500 | 861 | 798 | 7.9M | 85.3M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (775) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (696) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (79) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **82% unreachable** and **83% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

