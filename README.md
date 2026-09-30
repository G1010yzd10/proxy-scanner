# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-09-30 02:37:29 UTC** — 168057 unique proxies collected from 173/173 URL sources and 81/81 Telegram channels; **4500** endpoints really tested, **1030** reachable, **973** verified working (egress IP confirmed changed) across **48 exit countries**.

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

All 973 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:22324` | United States | 55 ms | 92.2 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇦🇺 AU | `vmess` | `67.220.95.3:18000` | Australia | 188 ms | 78.3 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `37.19.198.243:443` | United States | 304 ms | 64.2 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.89:443` | United States | 68 ms | 59.2 Mbps | xray |
| 5 | #5 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.234:2082` | United States | 33 ms | 59.1 Mbps | xray |
| 6 | #6 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.24.131:8880` | United States | 36 ms | 59.0 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vless` | `159.89.87.21:28190` | United States | 56 ms | 57.9 Mbps | xray |
| 8 | #8 🇺🇸 US → 🇺🇸 US | `vmess` | `216.106.183.35:22324` | United States | 71 ms | 55.7 Mbps | xray |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.104:443` | United States | 237 ms | 55.1 Mbps | xray |
| 10 | #10 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.149.54:443` | United States | 46 ms | 55.0 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.225:443` | United States | 193 ms | 54.5 Mbps | xray |
| 12 | #12 🇺🇸 US → 🇺🇸 US | `vless` | `47.90.153.88:443` | United States | 32 ms | 54.2 Mbps | xray |
| 13 | #13 🇺🇸 US → 🇺🇸 US | `vless` | `185.95.231.233:443` | United States | 72 ms | 53.8 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.96.39:8081` | United States | 49 ms | 53.8 Mbps | xray |
| 15 | #15 🇺🇸 US → 🇺🇸 US | `vless` | `79.141.172.154:10453` | United States | 39 ms | 53.1 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.179:443` | United States | 134 ms | 52.1 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vless` | `137.184.218.169:36925` | United States | 67 ms | 51.8 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `162.35.96.21:8081` | United States | 46 ms | 51.7 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `195.123.235.177:443` | United States | 71 ms | 50.6 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vmess` | `38.107.226.227:443` | United States | 38 ms | 50.2 Mbps | xray |
| 21 | #21 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.235:443` | United States | 132 ms | 48.5 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `169.40.42.35:443` | United States | 136 ms | 48.2 Mbps | xray |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vmess` | `216.106.183.35:443` | United States | 102 ms | 47.4 Mbps | xray |
| 24 | #24 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.158.146:8880` | United States | 33 ms | 46.7 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `vless` | `167.17.69.171:443` | United States | 79 ms | 45.9 Mbps | xray |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 48 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 348 | 18.0 Mbps | 24 ms | 36% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 139 | 7.1 Mbps | 293 ms | 14% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 76 | 6.3 Mbps | 285 ms | 8% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 49 | 6.9 Mbps | 273 ms | 5% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇬🇧 United Kingdom | 33 | 7.3 Mbps | 244 ms | 3% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇸🇬 Singapore | 29 | 3.0 Mbps | 802 ms | 3% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇨🇦 Canada | 28 | 21.1 Mbps | 80 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇭🇰 Hong Kong | 28 | 2.0 Mbps | 782 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇯🇵 Japan | 23 | 2.9 Mbps | 483 ms | 2% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇵🇱 Poland | 21 | 4.1 Mbps | 392 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇰🇷 South Korea | 18 | 3.7 Mbps | 663 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇸🇪 Sweden | 17 | 5.0 Mbps | 405 ms | 2% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇫🇮 Finland | 15 | 4.1 Mbps | 412 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇮🇳 India | 14 | 2.7 Mbps | 497 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇦🇺 Australia | 11 | 17.6 Mbps | 113 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇪🇸 Spain | 11 | 7.4 Mbps | 121 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇮🇹 Italy | 10 | 6.6 Mbps | 333 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇸 Serbia | 9 | 5.2 Mbps | 638 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇧🇬 Bulgaria | 8 | 5.0 Mbps | 520 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇷🇺 Russia | 8 | 4.4 Mbps | 404 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇲🇩 Moldova | 7 | 3.9 Mbps | 859 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇰🇿 Kazakhstan | 6 | 3.1 Mbps | 1069 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇦🇹 Austria | 5 | 7.5 Mbps | 430 ms | 1% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇹🇷 Turkey | 5 | 4.5 Mbps | 412 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇪🇪 Estonia | 5 | 6.1 Mbps | 464 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇹🇼 Taiwan | 5 | 3.0 Mbps | 665 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇳🇴 Norway | 4 | 5.6 Mbps | 377 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇺🇦 Ukraine | 4 | 4.6 Mbps | 448 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇷🇴 Romania | 4 | 5.3 Mbps | 521 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇱🇰 LK | 4 | 3.9 Mbps | 1007 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇮🇪 Ireland | 3 | 6.2 Mbps | 208 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇿🇦 South Africa | 3 | 3.4 Mbps | 821 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇨🇭 Switzerland | 2 | 6.8 Mbps | 410 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇦🇩 AD | 2 | 4.3 Mbps | 444 ms | 0% | [`AD.txt`](subs/by-country/AD.txt) |
| 🇦🇪 UAE | 2 | 3.3 Mbps | 840 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇹🇭 Thailand | 2 | 2.9 Mbps | 838 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇱🇹 Lithuania | 2 | 1.0 Mbps | 644 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇸🇰 Slovakia | 2 | - | 619 ms | 0% | [`SK.txt`](subs/by-country/SK.txt) |
| 🇲🇾 Malaysia | 2 | - | 748 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇲🇽 Mexico | 1 | 13.1 Mbps | 294 ms | 0% | [`MX.txt`](subs/by-country/MX.txt) |
| 🇬🇹 GT | 1 | 8.1 Mbps | 462 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇱🇻 Latvia | 1 | 6.6 Mbps | 576 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.7 Mbps | 1041 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇬🇪 Georgia | 1 | 3.5 Mbps | 1435 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇦🇲 Armenia | 1 | 2.3 Mbps | 2136 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇮🇩 Indonesia | 1 | 1.5 Mbps | 1260 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇧🇷 Brazil | 1 | - | 954 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇦🇷 Argentina | 1 | - | 979 ms | 0% | [`AR.txt`](subs/by-country/AR.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2850 | 645 | 622 | 23% |
| `ss` | 505 | 205 | 204 | 41% |
| `vmess` | 996 | 103 | 100 | 10% |
| `trojan` | 111 | 64 | 34 | 58% |
| `hysteria2` | 34 | 13 | 13 | 38% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 928 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 45 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 550 |
| 1 - 5 Mbps | 197 |
| 0.25 - 1 Mbps | 32 |
| < 0.25 Mbps | 0 |
| unmeasured | 194 |

Latency (phase-1 HTTPS round trip): median **401 ms**, p90 **1532 ms**. 57 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

254 active, 0 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `RD-VL` | url | 2659 | 532 | 5 |
| `HC` | url | 1651 | 462 | 2 |
| `HP` | url | 522 | 448 | 0 |
| `ST-VL` | url | 2585 | 412 | 59 |
| `SK` | url | 714 | 404 | 0 |
| `NK` | url | 693 | 383 | 54 |
| `F0` | url | 411 | 329 | 0 |
| `EV` | url | 432 | 297 | 0 |
| `SB-VL` | url | 2292 | 280 | 0 |
| `Ni` | url | 326 | 257 | 0 |
| `SB` | url | 2502 | 257 | 0 |
| `KA` | url | 2643 | 207 | 0 |
| `RD-SS` | url | 470 | 201 | 0 |
| `ET` | url | 293 | 187 | 440 |
| `EV-VL` | url | 213 | 145 | 0 |
| `EV-SS` | url | 156 | 131 | 0 |
| `WU` | url | 158 | 122 | 7 |
| `AG-PL` | url | 335 | 121 | 455 |
| `EP-ALL` | url | 1413 | 110 | 0 |
| `YA-VL` | url | 556 | 102 | 48 |

## History

working per run (last 6): ▁▁▇▇██

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (973) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (928) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (45) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
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

The typical aggregator relists whatever it scraped, so 80-95% of entries are dead within hours — this run found **77% unreachable** and **78% unusable** overall. Only tunnels that completed a real HTTPS handshake, returned a verifiable foreign exit IP, and pushed a 1 MB download are counted as working here.

## Disclaimers

- Free proxies are **public and untrusted**. Anything you send through them can be observed or modified by their operators. Never use them for authentication, payments, or anything sensitive.
- All configs are collected from publicly posted sources (GitHub subscriptions and public Telegram channels); no credentials are guessed or brute-forced. Removal requests: open an issue.
- Availability is transient: the working list is re-verified every 6 hours, and past performance never guarantees future availability.

