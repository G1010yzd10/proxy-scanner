# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-10-06 21:56:22 UTC** — 157536 unique proxies collected from 133/133 URL sources and 47/47 Telegram channels; **4513** endpoints really tested, **946** reachable, **913** verified working (egress IP confirmed changed) across **44 exit countries**.

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

All 913 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.48.32:2086` | United States | 107 ms | 46.8 Mbps | xray |
| 2 | #2 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.108:8080` | United States | 487 ms | 46.8 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 366 ms | 44.7 Mbps | xray |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 132 ms | 44.5 Mbps | singbox |
| 5 | #5 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.47.113:2095` | United States | 444 ms | 44.0 Mbps | xray |
| 6 | #6 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.46:80` | United States | 110 ms | 42.9 Mbps | xray |
| 7 | #7 🇺🇸 US → 🇺🇸 US | `vmess` | `167.17.68.89:22324` | United States | 77 ms | 41.2 Mbps | xray |
| 8 | #8 ❓ ?? → 🇺🇸 US | `vless` | `45.32.69.110:443` | United States | 73 ms | 40.8 Mbps | singbox |
| 9 | #9 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.154.8:8880` | United States | 110 ms | 40.8 Mbps | xray |
| 10 | #10 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.46.46:8080` | United States | 75 ms | 40.4 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vmess` | `216.152.152.187:22324` | United States | 176 ms | 40.2 Mbps | xray |
| 12 | #12 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.43.187:8080` | United States | 96 ms | 39.5 Mbps | xray |
| 13 | #13 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.169:2086` | United States | 87 ms | 39.4 Mbps | xray |
| 14 | #14 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.229.2:8880` | United States | 154 ms | 38.9 Mbps | xray |
| 15 | #15 ❓ ?? → 🇺🇸 US | `vmess` | `vspeedfast.org:443` | United States | 339 ms | 38.9 Mbps | xray |
| 16 | #16 ❓ ?? → 🇺🇸 US | `vmess` | `guanwang.awsno.com:443` | United States | 200 ms | 38.5 Mbps | xray |
| 17 | #17 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.48.32:8080` | United States | 173 ms | 38.2 Mbps | xray |
| 18 | #18 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.229.170:8880` | United States | 78 ms | 36.7 Mbps | xray |
| 19 | #19 🇺🇸 US → 🇺🇸 US | `vless` | `195.123.240.65:443` | United States | 89 ms | 36.5 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.0.177:8388` | United States | 375 ms | 36.5 Mbps | xray |
| 21 | #21 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.32.103:8880` | United States | 128 ms | 35.6 Mbps | xray |
| 22 | #22 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.53:8880` | United States | 429 ms | 35.6 Mbps | xray |
| 23 | #23 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.39.218:2086` | United States | 81 ms | 34.4 Mbps | xray |
| 24 | #24 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.34.14:2052` | United States | 84 ms | 34.2 Mbps | xray |
| 25 | #25 ❓ ?? → 🇺🇸 US | `vless` | `154.29.145.196:443` | United States | 80 ms | 33.8 Mbps | singbox |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 44 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 259 | 16.7 Mbps | 41 ms | 28% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 162 | 4.8 Mbps | 402 ms | 18% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 83 | 4.2 Mbps | 417 ms | 9% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 54 | 3.3 Mbps | 538 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇯🇵 Japan | 42 | 4.7 Mbps | 343 ms | 5% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇭🇰 Hong Kong | 26 | 4.2 Mbps | 498 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇬🇧 United Kingdom | 22 | 4.7 Mbps | 385 ms | 2% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇰🇷 South Korea | 22 | 3.9 Mbps | 497 ms | 2% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇸🇬 Singapore | 22 | 3.4 Mbps | 548 ms | 2% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇨🇦 Canada | 21 | 7.2 Mbps | 164 ms | 2% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇵🇱 Poland | 19 | 3.5 Mbps | 645 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇫🇮 Finland | 18 | 3.0 Mbps | 505 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇮🇳 India | 12 | 1.6 Mbps | 933 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇨🇱 Chile | 11 | 5.0 Mbps | 546 ms | 1% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇸🇪 Sweden | 10 | 4.2 Mbps | 579 ms | 1% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇪🇪 Estonia | 10 | 3.8 Mbps | 628 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇷🇸 Serbia | 10 | 3.5 Mbps | 911 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇲🇩 Moldova | 10 | 2.7 Mbps | 1020 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇪🇸 Spain | 8 | 3.8 Mbps | 563 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇮🇹 Italy | 8 | 4.4 Mbps | 528 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇴 Romania | 8 | 3.2 Mbps | 789 ms | 1% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇧🇬 Bulgaria | 8 | 3.6 Mbps | 696 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇹🇷 Turkey | 8 | 2.8 Mbps | 817 ms | 1% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇧🇾 BY | 8 | 1.6 Mbps | 938 ms | 1% | [`BY.txt`](subs/by-country/BY.txt) |
| 🇮🇪 Ireland | 6 | 4.3 Mbps | 493 ms | 1% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇰🇿 Kazakhstan | 6 | 2.1 Mbps | 1234 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇷🇺 Russia | 5 | 4.6 Mbps | 330 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇹🇼 Taiwan | 5 | 3.6 Mbps | 518 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇨🇭 Switzerland | 4 | 3.9 Mbps | 654 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇦🇹 Austria | 3 | 5.0 Mbps | 494 ms | 0% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇳🇴 Norway | 3 | 4.5 Mbps | 752 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇮🇩 Indonesia | 3 | 3.3 Mbps | 896 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |
| 🇿🇦 South Africa | 3 | 2.9 Mbps | 982 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇧🇷 Brazil | 2 | 4.0 Mbps | 905 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇲🇾 Malaysia | 2 | 4.2 Mbps | 604 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇦🇪 UAE | 2 | 3.1 Mbps | 1060 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇱🇻 Latvia | 1 | 4.3 Mbps | 1074 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇬🇷 Greece | 1 | 4.2 Mbps | 852 ms | 0% | [`GR.txt`](subs/by-country/GR.txt) |
| 🇺🇦 Ukraine | 1 | 4.0 Mbps | 936 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇹🇭 Thailand | 1 | 3.8 Mbps | 730 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇦🇺 Australia | 1 | 3.4 Mbps | 1141 ms | 0% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇸🇦 Saudi Arabia | 1 | 3.0 Mbps | 1036 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇨🇿 Czechia | 1 | 2.5 Mbps | 1198 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇦🇲 Armenia | 1 | 2.3 Mbps | 2025 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 2899 | 550 | 530 | 19% |
| `ss` | 429 | 191 | 184 | 45% |
| `vmess` | 990 | 97 | 93 | 10% |
| `trojan` | 155 | 93 | 91 | 60% |
| `hysteria2` | 37 | 14 | 14 | 38% |
| `tuic` | 1 | 1 | 1 | 100% |
| `http` | 2 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 840 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 73 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 413 |
| 1 - 5 Mbps | 378 |
| 0.25 - 1 Mbps | 27 |
| < 0.25 Mbps | 0 |
| unmeasured | 95 |

Latency (phase-1 HTTPS round trip): median **633 ms**, p90 **2596 ms**. 33 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

180 active, 74 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `NK` | url | 838 | 559 | 4645 |
| `SK` | url | 746 | 468 | 0 |
| `HP` | url | 486 | 428 | 149 |
| `RD-VL` | url | 2497 | 361 | 3964 |
| `HC` | url | 1423 | 324 | 238 |
| `F0` | url | 323 | 273 | 148 |
| `EV` | url | 448 | 272 | 0 |
| `Ni` | url | 320 | 250 | 91 |
| `ST-VL` | url | 2372 | 220 | 709 |
| `RD-SS` | url | 407 | 180 | 284 |
| `AG-PL` | url | 357 | 175 | 1361 |
| `ET` | url | 226 | 153 | 2741 |
| `KA` | url | 1478 | 150 | 13024 |
| `SB` | url | 2457 | 139 | 3 |
| `EV-SS` | url | 156 | 129 | 57 |
| `EV-VL` | url | 242 | 125 | 1469 |
| `SB-VL` | url | 2152 | 125 | 0 |
| `TK` | url | 137 | 101 | 62 |
| `RD-VM` | url | 708 | 90 | 2085 |
| `YA-VL` | url | 495 | 88 | 1497 |

## History

working per run (last 23): ▁▁▆▆▇█▇▆▇█▇▆▇▆▇▇█▇▇▇█▇▇

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
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
| 2026-09-30 21:54 | 4500 | 899 | 866 | 9.3M | 69.4M |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (913) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (6 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (840) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (73) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (44 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

