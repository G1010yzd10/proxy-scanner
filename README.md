# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-07 22:20:28 UTC** — 157516 unique proxies collected from 133/133 URL sources and 47/47 Telegram channels; **4509** endpoints really tested, **841** reachable, **819** verified working (egress IP confirmed changed) across **47 exit countries**.

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

All 819 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 324 ms | 74.8 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 323 ms | 65.3 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `vless` | `47.253.226.114:443` | United States | 291 ms | 61.5 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `147.182.212.232:56565` | United States | 419 ms | 60.9 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vmess` | `67.220.95.3:18000` | United States | 362 ms | 58.3 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 459 ms | 57.9 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.52:443` | United States | 619 ms | 51.2 Mbps | xray |
| 8 | #8 ❓ ?? → 🇺🇸 US | `ss` | `45.76.9.57:8393` | United States | 4143 ms | 51.0 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.74:443` | United States | 455 ms | 47.0 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 445 ms | 45.9 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `hysteria2` | `159.223.157.129:8443` | United States | 156 ms | 43.5 Mbps | singbox |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.233.41:8882` | United States | 301 ms | 41.3 Mbps | xray |
| 13 | #13 ❓ ?? → 🇺🇸 US | `vless` | `fs.koomeh.net:443` | United States | 328 ms | 40.9 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.16:443` | United States | 4624 ms | 40.8 Mbps | xray |
| 15 | #15 ❓ ?? → 🇺🇸 US | `vless` | `185.95.231.156:443` | United States | 370 ms | 39.0 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.163:443` | United States | 195 ms | 37.7 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.247.206:4444` | United States | 292 ms | 35.6 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.182:443` | United States | 197 ms | 32.6 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `195.211.98.43:443` | United States | 431 ms | 31.9 Mbps | xray |
| 20 | #20 ❓ ?? → 🇺🇸 US | `vless` | `ww9.levikogjgfdd.ir:36925` | United States | 268 ms | 30.3 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.235:443` | United States | 1494 ms | 30.3 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.95:443` | United States | 190 ms | 30.3 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.212:443` | United States | 389 ms | 29.7 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 247 ms | 29.6 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.225:443` | United States | 567 ms | 28.9 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 47 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇳🇱 Netherlands | 161 | 7.1 Mbps | 272 ms | 20% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇺🇸 United States | 146 | 18.3 Mbps | 43 ms | 18% | [`US.txt`](subs/by-country/US.txt) |
| 🇩🇪 Germany | 80 | 6.0 Mbps | 333 ms | 10% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 60 | 5.1 Mbps | 361 ms | 7% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 48 | 3.6 Mbps | 521 ms | 6% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇭🇰 Hong Kong | 31 | 3.2 Mbps | 622 ms | 4% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇸🇬 Singapore | 29 | 2.6 Mbps | 672 ms | 4% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇰🇷 South Korea | 28 | 2.8 Mbps | 640 ms | 3% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇬🇧 United Kingdom | 26 | 7.5 Mbps | 307 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇨🇦 Canada | 18 | 10.8 Mbps | 126 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇵🇱 Poland | 18 | 5.5 Mbps | 435 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 18 | 4.1 Mbps | 332 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇮🇳 India | 12 | 2.7 Mbps | 383 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇨🇱 Chile | 11 | 6.1 Mbps | 473 ms | 1% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇷🇸 Serbia | 10 | 5.2 Mbps | 633 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇧🇬 Bulgaria | 10 | 5.1 Mbps | 511 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇪🇪 Estonia | 9 | 5.7 Mbps | 507 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇹🇷 Turkey | 8 | 5.3 Mbps | 465 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇾 BY | 8 | 5.3 Mbps | 711 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇲🇩 Moldova | 8 | 3.6 Mbps | 759 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇪🇸 Spain | 7 | 6.2 Mbps | 408 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇮🇪 Ireland | 6 | 6.1 Mbps | 222 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇸🇪 Sweden | 6 | 6.3 Mbps | 417 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇮🇹 Italy | 6 | 7.0 Mbps | 324 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇰🇿 Kazakhstan | 6 | 2.5 Mbps | 1115 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇹🇼 Taiwan | 5 | 2.7 Mbps | 767 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇨🇭 Switzerland | 4 | 7.0 Mbps | 439 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇦🇹 Austria | 4 | 7.2 Mbps | 363 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇳🇴 Norway | 4 | 3.1 Mbps | 437 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇷🇴 Romania | 4 | 3.6 Mbps | 648 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇷🇺 Russia | 4 | 4.0 Mbps | 653 ms | 0% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇹🇭 Thailand | 4 | 2.8 Mbps | 895 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇿🇦 South Africa | 3 | 3.4 Mbps | 883 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇮🇩 Indonesia | 3 | 1.9 Mbps | 1021 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇦🇪 UAE | 2 | 4.1 Mbps | 847 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇲🇽 Mexico | 1 | 7.9 Mbps | 472 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇺🇦 Ukraine | 1 | 7.2 Mbps | 693 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇱🇻 Latvia | 1 | 6.6 Mbps | 501 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇦🇱 AL | 1 | 6.3 Mbps | 546 ms | 0% | [`AL.txt`](subs/by-country/AL.txt) |
| 🇬🇷 Greece | 1 | 5.8 Mbps | 559 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇨🇿 Czechia | 1 | 4.5 Mbps | 948 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.9 Mbps | 1048 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇺 Australia | 1 | 3.8 Mbps | 892 ms | 0% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇮🇱 Israel | 1 | - | 711 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |
| 🇨🇳 China | 1 | - | 930 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |
| 🇲🇾 Malaysia | 1 | - | 1862 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇱🇺 Luxembourg | 1 | - | 4783 ms | 0% | [`LU.txt`](subs/by-country/LU.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2868 | 436 | 420 | 15% |
| `ss` | 433 | 199 | 198 | 46% |
| `trojan` | 220 | 99 | 99 | 45% |
| `vmess` | 937 | 83 | 78 | 9% |
| `hysteria2` | 47 | 23 | 23 | 49% |
| `tuic` | 1 | 1 | 1 | 100% |
| `http` | 3 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 750 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 69 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 454 |
| 1 - 5 Mbps | 248 |
| 0.25 - 1 Mbps | 24 |
| < 0.25 Mbps | 0 |
| unmeasured | 93 |

Latency (phase-1 HTTPS round trip): median **589 ms**, p90 **2447 ms**. 22 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

180 active, 74 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 799 | 466 | 3750 |
| `SK` | url | 740 | 409 | 193 |
| `HP` | url | 396 | 366 | 214 |
| `Ni` | url | 378 | 291 | 165 |
| `F0` | url | 311 | 281 | 147 |
| `RD-VL` | url | 2455 | 262 | 4211 |
| `HC` | url | 1417 | 242 | 88 |
| `AG-PL` | url | 568 | 218 | 1411 |
| `EV` | url | 424 | 217 | 1500 |
| `ST-VL` | url | 2402 | 197 | 666 |
| `RD-SS` | url | 405 | 195 | 257 |
| `ET` | url | 263 | 190 | 2556 |
| `SB` | url | 2586 | 140 | 4 |
| `KA` | url | 1533 | 139 | 4970 |
| `EV-SS` | url | 154 | 129 | 52 |
| `AN` | url | 131 | 129 | 13 |
| `AQ` | url | 155 | 95 | 569 |
| `TK` | url | 129 | 82 | 0 |
| `SB-VL` | url | 2143 | 79 | 0 |
| `EB2` | url | 137 | 76 | 3 |

## History

working per run (last 26): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇▇▇▇▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-10-01 22:23 | 4500 | 904 | 878 | 7.5M | 90.2M |
| 2026-10-01 17:56 | 4500 | 861 | 794 | 7.3M | 58.6M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (819) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (750) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (69) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **81% unreachable** and **82% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

