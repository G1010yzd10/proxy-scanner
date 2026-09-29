# Free Proxy Scanner

> **Really tested** free proxy aggregator. Every proxy below was fetched from public sources, tunneled through with Xray/sing-box, and verified to actually change your egress IP. No CSV-validation theater, no blind relisting.

![working](badges/working.json) ![alive](badges/alive.json) ![speed](badges/speed.json) ![max-speed](badges/max-speed.json) ![countries](badges/countries.json) ![sources](badges/sources.json) ![updated](badges/updated.json)

## What this is

A GitHub Actions pipeline (runs every 6 hours) that fetches free proxy configs from **173 URL subscriptions** and **81 Telegram channels**, parses 9 protocols (vless / vmess / trojan / ss / hysteria2 / hysteria / tuic / socks / http), deduplicates them, and **actually connects through every single one** to separate working proxies from dead ones.

Latest run: **2026-09-29 15:28:09 UTC** — 163148 unique proxies collected from 173/173 URL sources and 81/81 Telegram channels; **4500** endpoints really tested, **839** reachable, **796** verified working (egress IP confirmed changed) across **52 exit countries**.

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

All 796 working proxies are published in [`subs/all.txt`](subs/all.txt); this table shows the top 25.

| # | proxy | proto | server | exit | latency | speed | engine |
|---|-------|-------|--------|------|---------|-------|--------|
| 1 | #1 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.154.8:8880` | United States | 78 ms | 51.3 Mbps | xray |
| 2 | #2 🇺🇸 US → 🇺🇸 US | `ss` | `192.3.247.109:43579` | United States | 359 ms | 50.4 Mbps | xray |
| 3 | #3 🇺🇸 US → 🇺🇸 US | `hysteria2` | `142.249.37.90:44356` | United States | 107 ms | 48.5 Mbps | singbox |
| 4 | #4 🇺🇸 US → 🇺🇸 US | `vless` | `167.17.68.205:443` | United States | 73 ms | 41.8 Mbps | xray |
| 5 | #5 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.118.10:8388` | United States | 92 ms | 41.8 Mbps | xray |
| 6 | #6 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.43.187:8880` | United States | 326 ms | 40.1 Mbps | xray |
| 7 | #7 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.154.8:2052` | United States | 77 ms | 40.0 Mbps | xray |
| 8 | #8 ❓ ?? → 🇺🇸 US | `hysteria2` | `hy2.561891.xyz:44356` | United States | 102 ms | 39.6 Mbps | singbox |
| 9 | #9 🇺🇸 US → 🇺🇸 US | `ss` | `173.244.56.9:443` | United States | 97 ms | 38.1 Mbps | xray |
| 10 | #10 🇺🇸 US → 🇺🇸 US | `ss` | `108.181.0.177:8388` | United States | 348 ms | 35.3 Mbps | xray |
| 11 | #11 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.43.210:53957` | United States | 52 ms | 34.4 Mbps | xray |
| 12 | #12 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.0.169:80` | United States | 122 ms | 33.7 Mbps | xray |
| 13 | #13 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.43.187:2095` | United States | 241 ms | 33.2 Mbps | xray |
| 14 | #14 🇺🇸 US → 🇺🇸 US | `vless` | `192.3.247.109:32132` | United States | 51 ms | 33.0 Mbps | xray |
| 15 | #15 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.48.32:2095` | United States | 70 ms | 32.9 Mbps | xray |
| 16 | #16 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.25.74:443` | United States | 116 ms | 30.9 Mbps | xray |
| 17 | #17 🇺🇸 US → 🇺🇸 US | `vmess` | `129.146.77.248:39495` | United States | 29 ms | 29.9 Mbps | xray |
| 18 | #18 🇺🇸 US → 🇺🇸 US | `vless` | `172.235.38.85:42942` | United States | 59 ms | 29.7 Mbps | xray |
| 19 | #19 🇨🇦 CA → 🇺🇸 US | `vless` | `104.18.47.113:8880` | United States | 68 ms | 29.7 Mbps | xray |
| 20 | #20 🇺🇸 US → 🇺🇸 US | `vless` | `192.3.247.109:43580` | United States | 52 ms | 29.2 Mbps | xray |
| 21 | #21 🇨🇦 CA → 🇺🇸 US | `vless` | `162.159.24.131:80` | United States | 70 ms | 28.7 Mbps | xray |
| 22 | #22 🇺🇸 US → 🇺🇸 US | `vless` | `47.251.108.158:443` | United States | 111 ms | 28.6 Mbps | singbox |
| 23 | #23 🇺🇸 US → 🇺🇸 US | `vless` | `192.3.247.109:43578` | United States | 54 ms | 28.1 Mbps | xray |
| 24 | #24 🇨🇦 CA → 🇺🇸 US | `vless` | `172.64.154.8:2095` | United States | 72 ms | 25.3 Mbps | xray |
| 25 | #25 🇺🇸 US → 🇺🇸 US | `hysteria2` | `155.248.209.237:33333` | United States | 121 ms | 23.3 Mbps | singbox |

## Exit locations — which countries work

Every working proxy, grouped by the country of its **verified exit IP** (phase 2), with a dedicated subscription file per country. Currently 52 countries have at least one working exit.

| country | working | avg speed | best latency | share | list |
|---------|--------:|----------:|-------------:|------:|------|
| 🇺🇸 United States | 226 | 13.4 Mbps | 28 ms | 28% | [`US.txt`](subs/by-country/US.txt) |
| 🇳🇱 Netherlands | 140 | 4.7 Mbps | 414 ms | 18% | [`NL.txt`](subs/by-country/NL.txt) |
| 🇩🇪 Germany | 58 | 3.8 Mbps | 440 ms | 7% | [`DE.txt`](subs/by-country/DE.txt) |
| 🇫🇷 France | 50 | 2.7 Mbps | 536 ms | 6% | [`FR.txt`](subs/by-country/FR.txt) |
| 🇸🇬 Singapore | 34 | 3.1 Mbps | 547 ms | 4% | [`SG.txt`](subs/by-country/SG.txt) |
| 🇬🇧 United Kingdom | 30 | 4.4 Mbps | 401 ms | 4% | [`GB.txt`](subs/by-country/GB.txt) |
| 🇨🇦 Canada | 27 | 7.3 Mbps | 154 ms | 3% | [`CA.txt`](subs/by-country/CA.txt) |
| 🇯🇵 Japan | 22 | 3.6 Mbps | 336 ms | 3% | [`JP.txt`](subs/by-country/JP.txt) |
| 🇰🇷 South Korea | 22 | 3.3 Mbps | 490 ms | 3% | [`KR.txt`](subs/by-country/KR.txt) |
| 🇭🇰 Hong Kong | 22 | 3.1 Mbps | 739 ms | 3% | [`HK.txt`](subs/by-country/HK.txt) |
| 🇵🇱 Poland | 15 | 3.0 Mbps | 640 ms | 2% | [`PL.txt`](subs/by-country/PL.txt) |
| 🇸🇪 Sweden | 15 | 2.9 Mbps | 640 ms | 2% | [`SE.txt`](subs/by-country/SE.txt) |
| 🇫🇮 Finland | 12 | 3.1 Mbps | 690 ms | 2% | [`FI.txt`](subs/by-country/FI.txt) |
| 🇦🇺 Australia | 11 | 7.6 Mbps | 146 ms | 1% | [`AU.txt`](subs/by-country/AU.txt) |
| 🇮🇹 Italy | 9 | 4.1 Mbps | 497 ms | 1% | [`IT.txt`](subs/by-country/IT.txt) |
| 🇷🇸 Serbia | 9 | 3.5 Mbps | 931 ms | 1% | [`RS.txt`](subs/by-country/RS.txt) |
| 🇧🇬 Bulgaria | 8 | 3.3 Mbps | 706 ms | 1% | [`BG.txt`](subs/by-country/BG.txt) |
| 🇪🇸 Spain | 7 | 4.8 Mbps | 338 ms | 1% | [`ES.txt`](subs/by-country/ES.txt) |
| 🇮🇳 India | 7 | 3.2 Mbps | 941 ms | 1% | [`IN.txt`](subs/by-country/IN.txt) |
| 🇰🇿 Kazakhstan | 7 | 2.3 Mbps | 1333 ms | 1% | [`KZ.txt`](subs/by-country/KZ.txt) |
| 🇹🇼 Taiwan | 5 | 4.3 Mbps | 528 ms | 1% | [`TW.txt`](subs/by-country/TW.txt) |
| 🇲🇩 Moldova | 5 | 2.5 Mbps | 1044 ms | 1% | [`MD.txt`](subs/by-country/MD.txt) |
| 🇦🇹 Austria | 4 | 4.9 Mbps | 499 ms | 1% | [`AT.txt`](subs/by-country/AT.txt) |
| 🇪🇪 Estonia | 4 | 3.2 Mbps | 665 ms | 1% | [`EE.txt`](subs/by-country/EE.txt) |
| 🇷🇺 Russia | 4 | 1.0 Mbps | 1292 ms | 1% | [`RU.txt`](subs/by-country/RU.txt) |
| 🇮🇪 Ireland | 3 | 4.5 Mbps | 533 ms | 0% | [`IE.txt`](subs/by-country/IE.txt) |
| 🇱🇻 Latvia | 3 | 4.4 Mbps | 791 ms | 0% | [`LV.txt`](subs/by-country/LV.txt) |
| 🇹🇷 Turkey | 3 | 2.2 Mbps | 1014 ms | 0% | [`TR.txt`](subs/by-country/TR.txt) |
| 🇿🇦 South Africa | 3 | 3.0 Mbps | 939 ms | 0% | [`ZA.txt`](subs/by-country/ZA.txt) |
| 🇱🇰 LK | 3 | 2.1 Mbps | 1267 ms | 0% | [`LK.txt`](subs/by-country/LK.txt) |
| 🇺🇦 Ukraine | 2 | 3.3 Mbps | 609 ms | 0% | [`UA.txt`](subs/by-country/UA.txt) |
| 🇷🇴 Romania | 2 | 4.3 Mbps | 844 ms | 0% | [`RO.txt`](subs/by-country/RO.txt) |
| 🇨🇭 Switzerland | 2 | 3.2 Mbps | 1713 ms | 0% | [`CH.txt`](subs/by-country/CH.txt) |
| 🇱🇹 Lithuania | 2 | 2.5 Mbps | 861 ms | 0% | [`LT.txt`](subs/by-country/LT.txt) |
| 🇦🇪 UAE | 2 | 2.4 Mbps | 1127 ms | 0% | [`AE.txt`](subs/by-country/AE.txt) |
| 🇦🇩 AD | 2 | 1.4 Mbps | 6962 ms | 0% | [`AD.txt`](subs/by-country/AD.txt) |
| 🇬🇹 GT | 1 | 10.1 Mbps | 894 ms | 0% | [`GT.txt`](subs/by-country/GT.txt) |
| 🇨🇱 Chile | 1 | 5.5 Mbps | 549 ms | 0% | [`CL.txt`](subs/by-country/CL.txt) |
| 🇮🇱 Israel | 1 | 3.8 Mbps | 753 ms | 0% | [`IL.txt`](subs/by-country/IL.txt) |
| 🇬🇪 Georgia | 1 | 3.5 Mbps | 1218 ms | 0% | [`GE.txt`](subs/by-country/GE.txt) |
| 🇸🇦 Saudi Arabia | 1 | 2.8 Mbps | 1335 ms | 0% | [`SA.txt`](subs/by-country/SA.txt) |
| 🇨🇿 Czechia | 1 | 2.4 Mbps | 1213 ms | 0% | [`CZ.txt`](subs/by-country/CZ.txt) |
| 🇹🇭 Thailand | 1 | 2.3 Mbps | 4192 ms | 0% | [`TH.txt`](subs/by-country/TH.txt) |
| 🇩🇰 Denmark | 1 | 2.2 Mbps | 1361 ms | 0% | [`DK.txt`](subs/by-country/DK.txt) |
| 🇦🇲 Armenia | 1 | 1.1 Mbps | 2066 ms | 0% | [`AM.txt`](subs/by-country/AM.txt) |
| 🇳🇴 Norway | 1 | - | 593 ms | 0% | [`NO.txt`](subs/by-country/NO.txt) |
| 🇦🇱 AL | 1 | - | 682 ms | 0% | [`AL.txt`](subs/by-country/AL.txt) |
| 🇸🇰 Slovakia | 1 | - | 957 ms | 0% | [`SK.txt`](subs/by-country/SK.txt) |
| 🇦🇷 Argentina | 1 | - | 1004 ms | 0% | [`AR.txt`](subs/by-country/AR.txt) |
| 🇧🇷 Brazil | 1 | - | 1027 ms | 0% | [`BR.txt`](subs/by-country/BR.txt) |
| 🇲🇾 Malaysia | 1 | - | 1031 ms | 0% | [`MY.txt`](subs/by-country/MY.txt) |
| 🇮🇩 Indonesia | 1 | - | 5568 ms | 0% | [`ID.txt`](subs/by-country/ID.txt) |

A `??` exit means the geo lookup could not resolve the exit IP. Base64 variants of every country file sit next to them as `<CC>.base64.txt`.

## Protocol distribution

| protocol | tested | alive | working | alive rate |
|----------|-------:|------:|--------:|-----------:|
| `vless` | 3024 | 503 | 470 | 17% |
| `ss` | 481 | 194 | 191 | 40% |
| `vmess` | 856 | 93 | 89 | 11% |
| `trojan` | 98 | 36 | 33 | 37% |
| `hysteria2` | 37 | 13 | 13 | 35% |
| `http` | 4 | 0 | 0 | 0% |

Per-protocol working lists: [`subs/by-proto/`](subs/by-proto/) (one `vless.txt`, `vmess.txt`, ... per protocol, plus `.base64.txt` variants).

## Engine breakdown

Which core verified each working proxy. The engine fallback means a proxy that failed on its primary core got a second chance on the other one.

| engine | working | note |
|--------|--------:|------|
| Xray-core | 744 | [`allxray.txt`](subs/by-engine/allxray.txt) |
| sing-box | 52 | [`allsingbox.txt`](subs/by-engine/allsingbox.txt) |
| direct (curl) | 0 | plain http/socks, [`alldirect.txt`](subs/by-engine/alldirect.txt) |

## Speed & latency profile

| speed tier | proxies |
|-----------|--------:|
| >= 5 Mbps | 296 |
| 1 - 5 Mbps | 320 |
| 0.25 - 1 Mbps | 42 |
| < 0.25 Mbps | 0 |
| unmeasured | 138 |

Latency (phase-1 HTTPS round trip): median **691 ms**, p90 **3799 ms**. 43 proxies passed connectivity but failed egress verification (leaked the runner IP or broke on the exit check) and are excluded.

## Source health

254 active, 0 auto-retired (10 fetch failures / 10 all-dead runs / 10 days without anything new). Best contributors this run:

| source | kind | tested | alive | new this run |
|--------|------|-------:|------:|-------------:|
| `HP` | url | 494 | 431 | 49 |
| `RD-VL` | url | 2820 | 392 | 4856 |
| `SK` | url | 671 | 370 | 6223 |
| `HC` | url | 1631 | 349 | 201 |
| `NK` | url | 649 | 349 | 0 |
| `F0` | url | 389 | 316 | 9 |
| `EV` | url | 456 | 296 | 2000 |
| `ST-VL` | url | 2749 | 271 | 803 |
| `Ni` | url | 290 | 228 | 55 |
| `ET` | url | 269 | 192 | 2963 |
| `RD-SS` | url | 443 | 190 | 286 |
| `SB-VL` | url | 2399 | 156 | 0 |
| `KA` | url | 2788 | 136 | 12380 |
| `EV-SS` | url | 156 | 128 | 46 |
| `EV-VL` | url | 235 | 127 | 0 |
| `AG-PL` | url | 244 | 115 | 1180 |
| `SB` | url | 2568 | 107 | 0 |
| `WU` | url | 141 | 97 | 64 |
| `RD-VM` | url | 564 | 86 | 1857 |
| `WD` | url | 87 | 77 | 39 |

## History

working per run (last 4): ▁▁██

| date (UTC) | tested | alive | working | avg | max |
|------------|-------:|------:|--------:|----:|----:|
| 2026-09-29 15:48 | 4500 | 839 | 796 | 6.7M | 51.3M |
| 2026-09-29 14:48 | 4500 | 799 | 756 | 6.9M | 52.1M |
| 2026-09-29 14:12 | 4500 | 0 | 0 | - | - |
| 2026-09-29 13:39 | 0 | 0 | 0 | - | - |

## Subscription files

Everything under [`subs/`](subs/) is regenerated every run. Plain lists are one proxy URI per line; `.base64.txt` variants are the same list base64-encoded for clients that need the classic sub format.

| file | contents | direct subscription URL |
|------|----------|--------------------------|
| [`all.txt`](subs/all.txt) | ALL working proxies, ranked by speed (796) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.txt` |
| [`all.base64.txt`](subs/all.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/all.base64.txt` |
| [`top150.txt`](subs/top150.txt) | top 150 ranked (150) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.txt` |
| [`top150.base64.txt`](subs/top150.base64.txt) | same, base64 | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/top150.base64.txt` |
| [`by-proto/`](subs/by-proto/) | one list per protocol (5 protocols) | ...`/subs/by-proto/<proto>.txt` |
| [`by-engine/allxray.txt`](subs/by-engine/allxray.txt) | verified on Xray (744) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allxray.txt` |
| [`by-engine/allsingbox.txt`](subs/by-engine/allsingbox.txt) | verified on sing-box (52) | `https://raw.githubusercontent.com/G1010yzd10/proxy-scanner/main/subs/by-engine/allsingbox.txt` |
| [`by-country/`](subs/by-country/) | one list per exit country (52 countries, e.g. [`US.txt`](subs/by-country/US.txt), [`DE.txt`](subs/by-country/DE.txt)) | ...`/subs/by-country/<CC>.txt` |
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

