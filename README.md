# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-09 03:17:41 UTC** — 158654 unique proxies collected from 132/132 URL sources and 47/47 Telegram channels; **4504** endpoints really tested, **1042** reachable, **1006** verified working (egress IP confirmed changed) across **46 exit countries**.

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

All 1006 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 247 ms | 72.4 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 235 ms | 69.0 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 243 ms | 66.5 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `159.89.87.21:28190` | United States | 90 ms | 64.8 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 243 ms | 60.4 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.95.3:18000` | Australia | 200 ms | 59.0 Mbps | xray |
| 7 | #7 ❓ ?? → 🇺🇸 US | `vless` | `185.95.231.156:443` | United States | 215 ms | 56.5 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.182:443` | United States | 188 ms | 55.6 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.224:443` | United States | 183 ms | 54.9 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `vless` | `195.123.235.177:443` | United States | 55 ms | 54.1 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.75:443` | United States | 195 ms | 53.0 Mbps | xray |
| 12 | #12 ❓ ?? → 🇺🇸 US | `vless` | `ww9.levikogjgfdd.ir:36925` | United States | 253 ms | 52.5 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.90:443` | United States | 183 ms | 51.4 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.74:443` | United States | 4974 ms | 50.9 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `137.184.218.169:36925` | United States | 111 ms | 49.3 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.179:443` | United States | 73 ms | 46.8 Mbps | xray |
| 17 | #17 ❓ ?? → 🇺🇸 US | `ss` | `45.76.9.57:8393` | United States | 4162 ms | 43.8 Mbps | xray |
| 18 | #18 ❓ ?? → 🇺🇸 US | `vless` | `104.243.33.154:45299` | United States | 191 ms | 41.1 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.35:443` | United States | 71 ms | 40.9 Mbps | xray |
| 20 | #20 ❓ ?? → 🇺🇸 US | `vless` | `92.118.112.249:443` | United States | 67 ms | 40.1 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.202:443` | United States | 4081 ms | 39.4 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.168:443` | United States | 185 ms | 39.2 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.212:443` | United States | 252 ms | 38.7 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.104:443` | United States | 122 ms | 38.6 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.89:443` | United States | 143 ms | 38.6 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 46 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 259 | 18.4 Mbps | 39 ms | 26% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 169 | 6.7 Mbps | 272 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 105 | 5.9 Mbps | 306 ms | 10% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 61 | 7.9 Mbps | 347 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 59 | 3.0 Mbps | 500 ms | 6% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇸🇬 Singapore | 35 | 2.6 Mbps | 681 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇬🇧 United Kingdom | 30 | 7.3 Mbps | 262 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇵🇱 Poland | 28 | 5.4 Mbps | 430 ms | 3% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇭🇰 Hong Kong | 27 | 3.0 Mbps | 840 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇫🇮 Finland | 23 | 5.0 Mbps | 351 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇰🇷 South Korea | 22 | 3.0 Mbps | 649 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇨🇦 Canada | 20 | 14.9 Mbps | 84 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇮🇳 India | 13 | 3.3 Mbps | 687 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇪🇪 Estonia | 11 | 5.5 Mbps | 407 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇧🇬 Bulgaria | 11 | 5.0 Mbps | 530 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇷🇸 Serbia | 10 | 5.2 Mbps | 636 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇸🇪 Sweden | 9 | 5.7 Mbps | 389 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇹🇷 Turkey | 9 | 3.3 Mbps | 409 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇾 BY | 8 | 1.0 Mbps | 802 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇦🇺 Australia | 7 | 17.4 Mbps | 155 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇨🇭 Switzerland | 7 | 5.4 Mbps | 418 ms | 1% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇮🇪 Ireland | 7 | 4.9 Mbps | 320 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇷🇺 Russia | 6 | 5.5 Mbps | 362 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇮🇹 Italy | 6 | 6.8 Mbps | 335 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇲🇩 Moldova | 6 | 3.9 Mbps | 776 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇰🇿 Kazakhstan | 6 | 2.5 Mbps | 1321 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇱🇻 Latvia | 5 | 5.3 Mbps | 486 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇷🇴 Romania | 5 | 3.8 Mbps | 473 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇹🇼 Taiwan | 5 | 2.5 Mbps | 665 ms | 0% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇪🇸 Spain | 4 | 6.7 Mbps | 399 ms | 0% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇲🇾 Malaysia | 4 | 3.2 Mbps | 731 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇹🇭 Thailand | 4 | 2.3 Mbps | 876 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇦🇹 Austria | 3 | 7.3 Mbps | 346 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇳🇴 Norway | 3 | 7.1 Mbps | 390 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇮🇩 Indonesia | 3 | 2.4 Mbps | 1044 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇻🇳 Vietnam | 3 | 2.9 Mbps | 1814 ms | 0% | [`VN.txt`](subs/by-country/VN.txt) |
| 🇨🇿 Czechia | 2 | 3.9 Mbps | 850 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇦🇪 UAE | 2 | 4.1 Mbps | 843 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇿🇦 South Africa | 2 | 3.6 Mbps | 857 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇬🇷 Greece | 1 | 5.6 Mbps | 578 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇸🇦 Saudi Arabia | 1 | 4.2 Mbps | 984 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.2 Mbps | 2053 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇱🇺 Luxembourg | 1 | 2.1 Mbps | 1752 ms | 0% | [`LU.txt`](subs/by-country/LU.txt) |
| 🇨🇳 China | 1 | 0.7 Mbps | 1074 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇨🇱 Chile | 1 | - | 658 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇮🇱 Israel | 1 | - | 912 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2830 | 601 | 578 | 21% |
| `ss` | 476 | 202 | 190 | 42% |
| `trojan` | 227 | 122 | 122 | 54% |
| `vmess` | 900 | 81 | 80 | 9% |
| `hysteria2` | 68 | 35 | 35 | 51% |
| `tuic` | 1 | 1 | 1 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 929 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 77 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 527 |
| 1 - 5 Mbps | 270 |
| 0.25 - 1 Mbps | 23 |
| < 0.25 Mbps | 0 |
| unmeasured | 186 |

Latency (phase-1 HTTPS round trip): median **472 ms**, p90 **1894 ms**. 36 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

179 active, 75 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 1007 | 677 | 5579 |
| `SK` | url | 916 | 588 | 0 |
| `HP` | url | 416 | 385 | 39 |
| `RD-VL` | url | 2435 | 341 | 4355 |
| `Ni` | url | 402 | 304 | 91 |
| `F0` | url | 324 | 294 | 100 |
| `HC` | url | 1382 | 293 | 223 |
| `ET` | url | 340 | 280 | 1044 |
| `ST-VL` | url | 2391 | 280 | 762 |
| `EV` | url | 404 | 238 | 23 |
| `KA` | url | 1459 | 190 | 5373 |
| `RD-SS` | url | 436 | 187 | 295 |
| `SB` | url | 2505 | 182 | 8 |
| `AG-PL` | url | 390 | 170 | 1249 |
| `EV-SS` | url | 154 | 126 | 45 |
| `SB-VL` | url | 2082 | 123 | 0 |
| `WU` | url | 129 | 107 | 334 |
| `EV-VL` | url | 200 | 95 | 1480 |
| `LK2` | url | 465 | 90 | 11881 |
| `WD` | url | 91 | 84 | 171 |

## History

working per run (last 30): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇▇▇▇▇█▆▇█

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-10-03 02:52 | 4500 | 1062 | 1030 | 8.0M | 75.5M |
| 2026-10-02 21:49 | 4500 | 890 | 861 | 8.9M | 68.7M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (1006) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (929) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (77) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (46 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **77% unreachable** and **78% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

