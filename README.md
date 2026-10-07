# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-07 02:54:21 UTC** — 156823 unique proxies collected from 133/133 URL sources and 47/47 Telegram channels; **4516** endpoints really tested, **957** reachable, **922** verified working (egress IP confirmed changed) across **47 exit countries**.

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

All 922 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 ❓ ?? → 🇺🇸 US | `ss` | `66.23.204.210:16995` | United States | 414 ms | 49.7 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.167:443` | United States | 394 ms | 40.8 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `vmess` | `167.88.62.124:22324` | United States | 394 ms | 39.5 Mbps | xray |
| 4 | #4 ❓ ?? → 🇺🇸 US | `vless` | `3h-unitedstates1.09vpn.com:80` | United States | 351 ms | 38.8 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `vless` | `195.211.98.43:443` | United States | 2298 ms | 38.1 Mbps | xray |
| 6 | #6 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.169:443` | United States | 405 ms | 28.7 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `198.251.78.29:2053` | United States | 177 ms | 28.0 Mbps | xray |
| 8 | #8 ❓ ?? → 🇺🇸 US | `vless` | `uspanel.unixzone.us:30016` | United States | 187 ms | 27.4 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `ss` | `156.146.38.168:443` | United States | 313 ms | 27.1 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.160:443` | United States | 192 ms | 25.7 Mbps | xray |
| 11 | #11 🇨🇦 CA → 🇨🇦 CA | `vmess` | `134.195.196.211:18000` | Canada | 271 ms | 24.7 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.246.132:7307` | United States | 279 ms | 23.8 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.244:443` | United States | 355 ms | 23.5 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.236:443` | United States | 401 ms | 22.7 Mbps | xray |
| 15 | #15 🇨🇦 CA → 🇺🇸 US | `vless` | `188.114.96.9:443` | United States | 254 ms | 22.3 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:22324` | United States | 189 ms | 21.4 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.163:443` | United States | 267 ms | 21.0 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.133:443` | United States | 271 ms | 21.0 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.184:443` | United States | 275 ms | 20.9 Mbps | xray |
| 20 | #20 ❓ ?? → 🇺🇸 US | `vless` | `fs.koomeh.net:443` | United States | 283 ms | 20.8 Mbps | xray |
| 21 | #21 ❓ ?? → 🇺🇸 US | `vless` | `185.95.231.156:443` | United States | 151 ms | 20.3 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `ss` | `15.204.233.41:8882` | United States | 305 ms | 20.1 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `ss` | `140.82.63.79:8388` | United States | 320 ms | 19.9 Mbps | xray |
| 24 | #24 🇺🇸 US → 🇺🇸 US | `vmess` | `172.111.38.100:22324` | United States | 343 ms | 19.8 Mbps | xray |
| 25 | #25 🇨🇦 CA → 🇨🇦 CA | `vmess` | `23.162.200.227:443` | Canada | 186 ms | 19.7 Mbps | singbox |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 47 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 230 | 13.3 Mbps | 77 ms | 25% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 161 | 5.8 Mbps | 361 ms | 17% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 90 | 4.8 Mbps | 376 ms | 10% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 58 | 5.9 Mbps | 453 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 40 | 3.8 Mbps | 426 ms | 4% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇨🇦 Canada | 36 | 11.0 Mbps | 86 ms | 4% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇰🇷 South Korea | 29 | 4.0 Mbps | 591 ms | 3% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇭🇰 Hong Kong | 27 | 3.1 Mbps | 722 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇸🇬 Singapore | 22 | 2.7 Mbps | 639 ms | 2% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇬🇧 United Kingdom | 20 | 4.9 Mbps | 342 ms | 2% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇵🇱 Poland | 20 | 3.9 Mbps | 543 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 20 | 3.5 Mbps | 419 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇮🇳 India | 12 | 2.2 Mbps | 847 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇸🇪 Sweden | 11 | 4.7 Mbps | 485 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇨🇱 Chile | 11 | 5.3 Mbps | 533 ms | 1% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇪🇪 Estonia | 10 | 4.7 Mbps | 550 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇷🇸 Serbia | 10 | 4.2 Mbps | 750 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇲🇩 Moldova | 9 | 3.5 Mbps | 936 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇷🇺 Russia | 8 | 5.7 Mbps | 473 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇧🇬 Bulgaria | 8 | 4.2 Mbps | 571 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇮🇹 Italy | 7 | 4.6 Mbps | 500 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇪🇸 Spain | 7 | 4.9 Mbps | 449 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇰🇿 Kazakhstan | 7 | 2.5 Mbps | 753 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇹🇷 Turkey | 7 | 3.5 Mbps | 743 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇾 BY | 7 | 1.7 Mbps | 766 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇮🇪 Ireland | 6 | 4.7 Mbps | 419 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇷🇴 Romania | 6 | 4.0 Mbps | 562 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇳🇴 Norway | 5 | 4.3 Mbps | 504 ms | 1% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇹🇼 Taiwan | 5 | 3.0 Mbps | 628 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇦🇹 Austria | 4 | 5.9 Mbps | 428 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇨🇭 Switzerland | 3 | 5.6 Mbps | 561 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇮🇩 Indonesia | 3 | 2.6 Mbps | 914 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇹🇭 Thailand | 3 | 2.7 Mbps | 787 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇿🇦 South Africa | 3 | 2.8 Mbps | 926 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇱🇻 Latvia | 2 | 4.1 Mbps | 960 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇮🇱 Israel | 2 | 3.1 Mbps | 802 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |
| 🇦🇪 UAE | 2 | 2.8 Mbps | 1232 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇲🇾 Malaysia | 2 | - | 697 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇦🇱 AL | 1 | 5.5 Mbps | 527 ms | 0% | [`AL.txt`](subs/by-country/AL.txt) |
| 🇺🇦 Ukraine | 1 | 5.0 Mbps | 857 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇬🇷 Greece | 1 | 4.8 Mbps | 700 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇧🇷 Brazil | 1 | 4.0 Mbps | 882 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇦🇺 Australia | 1 | 3.8 Mbps | 1205 ms | 0% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇨🇿 Czechia | 1 | 3.4 Mbps | 1088 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.4 Mbps | 1158 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇦🇲 Armenia | 1 | 2.4 Mbps | 1748 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇨🇳 China | 1 | - | 783 ms | 0% | [`CN.txt`](subs/by-country/CN.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2819 | 546 | 523 | 19% |
| `ss` | 424 | 198 | 193 | 47% |
| `vmess` | 1085 | 101 | 95 | 9% |
| `trojan` | 147 | 95 | 94 | 65% |
| `hysteria2` | 38 | 16 | 16 | 42% |
| `tuic` | 1 | 1 | 1 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 854 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 68 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 432 |
| 1 - 5 Mbps | 299 |
| 0.25 - 1 Mbps | 22 |
| < 0.25 Mbps | 0 |
| unmeasured | 169 |

Latency (phase-1 HTTPS round trip): median **565 ms**, p90 **1686 ms**. 35 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

180 active, 74 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 744 | 437 | 4484 |
| `SK` | url | 645 | 342 | 0 |
| `HP` | url | 480 | 341 | 76 |
| `F0` | url | 359 | 321 | 211 |
| `RD-VL` | url | 2443 | 316 | 3831 |
| `Ni` | url | 352 | 279 | 208 |
| `HC` | url | 1464 | 279 | 201 |
| `ET` | url | 303 | 269 | 2110 |
| `AG-PL` | url | 433 | 244 | 1303 |
| `ST-VL` | url | 2295 | 240 | 686 |
| `EV` | url | 442 | 237 | 0 |
| `SB` | url | 2467 | 211 | 114 |
| `RD-SS` | url | 406 | 189 | 277 |
| `KA` | url | 1522 | 138 | 13086 |
| `EV-SS` | url | 155 | 129 | 55 |
| `SB-VL` | url | 2035 | 120 | 0 |
| `EB2` | url | 153 | 100 | 6 |
| `LK2` | url | 718 | 96 | 11337 |
| `RD-VM` | url | 802 | 92 | 2111 |
| `10i-3` | url | 313 | 91 | 489 |

## History

working per run (last 24): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇▇▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-10-01 12:16 | 4500 | 931 | 883 | 7.3M | 34.4M |
| 2026-10-01 03:00 | 4500 | 1112 | 1075 | 8.1M | 45.4M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (922) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (854) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (68) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **79% unreachable** and **80% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

