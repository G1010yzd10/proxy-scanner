#!/usr/bin/env python3
"""Stage 3: TEST - for every candidate proxy, establish a REAL tunnel and verify.

Two phases:
  1. connectivity: HTTPS request to gstatic/generate_204 through the proxy
     (via a local xray or sing-box socks inbound, or curl -x for plain
     http/socks proxies). DNS goes through the proxy (--socks5-hostname).
  2. verification: egress identity (exit IP + country + AS via ip-api through
     the tunnel; must differ from the runner's own IP) + 1 MB throughput test.

If an engine fails for a proxy, the other engine gets one retry (some configs
only work on one core). Results -> data/results.json.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import engines  # noqa: E402
from lib.geo import Geo, COUNTRIES  # noqa: E402
from lib.states import (load_json, save_json, update_alive_recall,  # noqa: E402
                        SourceStates, GeoCache)

CHECK_URL = "https://www.gstatic.com/generate_204"
EXIT_URL = "http://ip-api.com/json/?fields=status,query,countryCode,as"
EXIT_URL2 = "https://api.ip.sb/geoip"
SPEED_URL = "https://speed.cloudflare.com/__down?bytes=1048576"

P1_MAXTIME = 9          # connectivity check
P2_MAXTIME = 12         # exit identity
SP_MAXTIME = 15         # 1 MB throughput
BATCH = 240             # proxies per engine process
P1_WORKERS = 48
P2_WORKERS = 24
XRAY_PORT = 30000
SB_PORT = 31000
ENGINE_STARTUP_WAIT = 2.5
ENGINE_LOG_KEPT = 20    # chars of engine log kept in error messages


def log(msg):
    print(f"[test] {msg}", flush=True)


def now():
    return time.time()


# ------------------------------------------------------------------ curl ----

def curl(args, timeout=None):
    """Run curl, return (exit_code, stdout_last_line)."""
    cmd = ["curl", "-sS", "-o", "/dev/null"] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout or (P1_MAXTIME + 25))
        out = (r.stderr or "").strip().splitlines()
        return r.returncode, out[-1] if out else ""
    except subprocess.TimeoutExpired:
        return 124, "killed"
    except Exception as e:
        return 125, str(e)[:100]


def proxy_args(p, local_port=None):
    """curl proxy flags: local engine port, or the proxy itself for http/socks."""
    if local_port:
        return ["--socks5-hostname", f"127.0.0.1:{local_port}"]
    proto = p.get("proto")
    host, port = p["server"], p["port"]
    if proto == "http":
        base = f"http://{host}:{port}"
        if p.get("user"):
            import urllib.parse
            cred = f"{urllib.parse.quote(p['user'], safe='')}:" \
                   f"{urllib.parse.quote(p.get('password', ''), safe='')}"
            base = f"http://{cred}@{host}:{port}"
        return ["-x", base]
    # socks (remote, DNS through it)
    args = ["--socks5-hostname", f"{host}:{port}"]
    if p.get("user"):
        args += ["--proxy-user", f"{p['user']}:{p.get('password', '')}"]
    return args


def fmt_w(keys):
    """-w format string for the keys we parse."""
    return "-w", "%" + "|%".join(keys)


def check_connectivity(p, local_port):
    """Phase 1: returns (alive, latency_ms, error)."""
    w = fmt_w(["http_code", "time_total"])
    code, out = curl(["--max-time", str(P1_MAXTIME), *proxy_args(p, local_port),
                      *w, CHECK_URL])
    if code != 0:
        return False, None, f"curl{code}:{out[:80]}"
    parts = out.split("|")
    if len(parts) < 2 or parts[0] != "204":
        return False, None, f"http:{parts[0] if parts else '?'}"
    try:
        lat = int(float(parts[1]) * 1000)
    except ValueError:
        lat = None
    return True, lat, ""


def check_exit(p, local_port):
    """Phase 2 identity: returns (exit_ip, cc, as_, err). Body fetched to stdout."""
    cmd = ["curl", "-sS", "--max-time", str(P2_MAXTIME), *proxy_args(p, local_port),
           EXIT_URL]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=P2_MAXTIME + 20)
        if r.returncode == 0 and r.stdout.strip().startswith("{"):
            j = json.loads(r.stdout)
            if j.get("status") == "success":
                return j.get("query", ""), j.get("countryCode", ""), j.get("as", ""), ""
        # try https fallback (some http proxies only allow CONNECT)
        cmd2 = ["curl", "-sS", "--max-time", str(P2_MAXTIME), *proxy_args(p, local_port),
                EXIT_URL2]
        r2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=P2_MAXTIME + 20)
        if r2.returncode == 0 and r2.stdout.strip().startswith("{"):
            j = json.loads(r2.stdout)
            ip = j.get("ip") or j.get("query") or ""
            cc = j.get("country_code") or ""
            asn = j.get("asn") or ""
            org = j.get("organization") or ""
            return ip, cc, (f"AS{asn} {org}" if asn else org), ""
        return "", "", "", f"exit_lookup_failed:{(r.stderr or r2.stderr)[:60]}"
    except subprocess.TimeoutExpired:
        return "", "", "", "exit_timeout"
    except Exception as e:
        return "", "", "", f"exit_err:{str(e)[:60]}"


def check_speed(p, local_port):
    """Phase 2 throughput: 1 MB download, returns kbps (kilobits/s) or None."""
    w = fmt_w(["size_download", "speed_download"])
    code, out = curl(["--max-time", str(SP_MAXTIME), *proxy_args(p, local_port),
                      *w, SPEED_URL], timeout=SP_MAXTIME + 20)
    parts = out.split("|")
    if len(parts) < 2:
        return None
    try:
        size = float(parts[0])
        spd = float(parts[1])
    except ValueError:
        return None
    if size < 100_000:   # <100KB received -> unusable measurement
        return None
    return int(spd * 8 / 1000)


# --------------------------------------------------------------- engines ----

class EngineBatch:
    """Run one engine with N proxies mapped to local socks ports 1:1."""

    def __init__(self, engine, xray_bin, sb_bin, tag):
        self.engine, self.xray_bin, self.sb_bin, self.tag = engine, xray_bin, sb_bin, tag
        self.proc = None
        self.cfg_path = f"/tmp/ps_{engine}_{tag}.json"
        self.log_path = f"/tmp/ps_{engine}_{tag}.log"

    def __enter__(self):
        return self

    def start(self, items, ports):
        if self.engine == "xray":
            cfg = engines.build_xray_config(items, ports)
            cmd = [self.xray_bin, "run", "-c", self.cfg_path]
        else:
            cfg = engines.build_singbox_config(items, ports)
            cmd = [self.sb_bin, "run", "-c", self.cfg_path]
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False)
        self.logf = open(self.log_path, "w", encoding="utf-8")
        self.proc = subprocess.Popen(cmd, stdout=self.logf, stderr=self.logf)
        time.sleep(ENGINE_STARTUP_WAIT)
        if self.proc.poll() is not None:
            err = self._logtail()
            raise RuntimeError(f"{self.engine} crashed on start: {err}")

    def _logtail(self):
        try:
            with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()[-300:]
        except OSError:
            return ""

    def __exit__(self, *exc):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        if getattr(self, "logf", None):
            try:
                self.logf.close()
            except Exception:
                pass


def run_engine_pass(items, engine, xray_bin, sb_bin, fn, workers, tag, ports_base):
    """Start engine in BATCHes; for each proxy call fn(proxy, local_port).

    Returns dict phash -> fn result; crashed batches are marked ("engine_failed",).
    """
    out = {}
    for bi in range(0, len(items), BATCH):
        if engine == "direct":
            chunk = items[bi:bi + BATCH]
            with ThreadPoolExecutor(max_workers=workers) as ex:
                for p, res in zip(chunk, ex.map(lambda p: fn(p, None), chunk)):
                    out[p["phash"]] = res
            continue
        chunk = items[bi:bi + BATCH]
        ports = [ports_base + i for i in range(len(chunk))]
        # skip proxies this engine cannot represent
        idx = [i for i, p in enumerate(chunk) if engines.engine_supports(engine, p)]
        if not idx:
            for i, p in enumerate(chunk):
                out[p["phash"]] = ("unsupported",)
            continue
        sub_items = [chunk[i] for i in idx]
        sub_ports = [ports[i] for i in idx]
        port_of = {p["phash"]: pt for p, pt in zip(sub_items, sub_ports)}
        try:
            with EngineBatch(engine, xray_bin, sb_bin, f"{tag}_{bi // BATCH}") as eng:
                eng.start(sub_items, sub_ports)
                with ThreadPoolExecutor(max_workers=workers) as ex:
                    futs = [(p, ex.submit(fn, p, port_of[p["phash"]])) for p in sub_items]
                    for p, fu in futs:
                        out[p["phash"]] = fu.result()
        except RuntimeError as e:
            log(f"  ! batch {bi // BATCH} ({engine}) failed: {str(e)[:120]}")
            for p in sub_items:
                out[p["phash"]] = ("engine_failed", str(e)[:ENGINE_LOG_KEPT])
        for i, p in enumerate(chunk):
            if p["phash"] not in out:
                out[p["phash"]] = ("unsupported",)
    return out


# ------------------------------------------------------------------ main ----

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--xray-bin", default="xray")
    ap.add_argument("--singbox-bin", default="sing-box")
    ap.add_argument("--limit", type=int, default=0, help="debug: cap candidates")
    ap.add_argument("--time-budget", type=int, default=2700)
    ap.add_argument("--skip-speed", action="store_true")
    args = ap.parse_args()
    root = args.root
    data_dir = os.path.join(root, "data")
    state_dir = os.path.join(root, "state")
    t0 = time.time()

    plan = load_json(os.path.join(data_dir, "test_plan.json"), [])
    if args.limit:
        plan = plan[:args.limit]
    log(f"candidates: {len(plan)}")

    # runner's own egress identity (for the "did egress really change" check)
    runner_ip, runner_cc = "", ""
    try:
        r = subprocess.run(["curl", "-sS", "--max-time", "10", EXIT_URL],
                           capture_output=True, text=True, timeout=20)
        j = json.loads(r.stdout)
        runner_ip, runner_cc = j.get("query", ""), j.get("countryCode", "")
    except Exception:
        pass
    log(f"runner egress: {runner_ip} ({runner_cc})")

    results = {}   # phash -> dict
    by_hash = {p["phash"]: p for p in plan}
    for p in plan:
        results[p["phash"]] = {"phash": p["phash"], "proto": p["proto"],
                               "server": p["server"], "port": p["port"],
                               "name": p.get("name", ""), "srcs": p.get("srcs", []),
                               "alive": False, "work": False, "latency_ms": None,
                               "exit_ip": "", "exit_cc": "", "exit_as": "",
                               "speed_kbps": None, "engine": "", "error": "untested"}

    def budget_left():
        return args.time_budget - (time.time() - t0)

    # -------------------------------------------------- phase 1: connect ----
    def p1(p, port):
        alive, lat, err = check_connectivity(p, port)
        return (alive, lat, err)

    def phase1(items, force_engine=None):
        groups = {"direct": [], "xray": [], "singbox": []}
        for p in items:
            eng = force_engine or engines.primary_engine(p)
            groups.setdefault(eng, []).append(p)
        for eng, gitems in groups.items():
            if not gitems:
                continue
            if budget_left() <= 60:
                log(f"  time budget nearly exhausted, skipping {len(gitems)} {eng}")
                continue
            log(f"  phase1 [{eng}]: {len(gitems)} proxies")
            tag = f"p1{force_engine or ''}"
            ports_base = XRAY_PORT if eng == "xray" else SB_PORT
            res = run_engine_pass(gitems, eng, args.xray_bin, args.singbox_bin,
                                  p1, P1_WORKERS, tag, ports_base)
            for h, (alive, lat, err) in res.items():
                if alive:
                    results[h].update(alive=True, latency_ms=lat, error="",
                                      engine=force_engine or engines.primary_engine(
                                          by_hash[h]))
                elif results[h]["error"] in ("untested",):
                    results[h].update(alive=False, error=err or "dead",
                                      engine=force_engine or "")
            log(f"    -> {sum(1 for h, r in res.items() if r[0])} reachable")

    log("phase 1: connectivity")
    phase1(plan)

    # fallback pass: swap engines for the failed ones
    failed = [p for p in plan if not results[p["phash"]]["alive"]
              and results[p["phash"]]["error"] not in ("unsupported", "engine_failed")]
    retry_sb = [p for p in failed if engines.primary_engine(p) == "xray"
                and engines.engine_supports("singbox", p)]
    retry_xr = [p for p in failed if engines.primary_engine(p) == "singbox"
                and engines.engine_supports("xray", p)]
    log(f"phase 1 fallback: {len(retry_sb)} -> sing-box, {len(retry_xr)} -> xray")
    if retry_sb:
        phase1(retry_sb, force_engine="singbox")
    if retry_xr:
        phase1(retry_xr, force_engine="xray")

    alive_items = [p for p in plan if results[p["phash"]]["alive"]]
    log(f"phase 1 done: {len(alive_items)} reachable in {int(time.time() - t0)}s")

    # ------------------------------------------- phase 2: verify + speed ----
    def p2(p, port):
        ip, cc, as_, err = check_exit(p, port)
        return (ip, cc, as_, err)

    def phase2(items):
        groups = {"direct": [], "xray": [], "singbox": []}
        for p in items:
            eng = "direct" if p.get("proto") in ("http", "socks", "socks5") \
                else results[p["phash"]].get("engine") or engines.primary_engine(p)
            if eng not in ("xray", "singbox", "direct"):
                eng = "direct" if p.get("proto") in ("http", "socks", "socks5") else "xray"
            groups.setdefault(eng, []).append(p)
        for eng, gitems in groups.items():
            if not gitems:
                continue
            if budget_left() <= 60:
                log(f"  time budget nearly exhausted, skipping exit check for {len(gitems)}")
                continue
            log(f"  phase2 [{eng}]: {len(gitems)} proxies")
            tag = "p2"
            ports_base = XRAY_PORT if eng == "xray" else SB_PORT
            res = run_engine_pass(gitems, eng, args.xray_bin, args.singbox_bin,
                                  p2, P2_WORKERS, tag, ports_base)
            for h, (ip, cc, as_, err) in res.items():
                r = results[h]
                if ip:
                    r.update(exit_ip=ip, exit_cc=cc, exit_as=as_)
                    r["work"] = bool(runner_ip and ip != runner_ip)
                    if not r["work"]:
                        r["error"] = "egress_not_changed"
                else:
                    r["error"] = err or "exit_lookup_failed"

    log("phase 2: egress identity")
    phase2(alive_items)

    working = [p for p in alive_items if results[p["phash"]]["work"]]
    log(f"phase 2 done: {len(working)} verified working "
        f"(egress actually changed) in {int(time.time() - t0)}s")

    # throughput on working proxies, fastest-first so budget cuts hurt least
    if not args.skip_speed:
        working.sort(key=lambda p: results[p["phash"]]["latency_ms"] or 9999)

        def sp(p, port):
            return check_speed(p, port)

        groups = {"direct": [], "xray": [], "singbox": []}
        for p in working:
            eng = "direct" if p.get("proto") in ("http", "socks", "socks5") \
                else results[p["phash"]].get("engine") or "xray"
            groups.setdefault(eng, []).append(p)
        for eng, gitems in groups.items():
            if not gitems or budget_left() <= 60:
                continue
            log(f"  speed [{eng}]: {len(gitems)} proxies")
            ports_base = XRAY_PORT if eng == "xray" else SB_PORT
            res = run_engine_pass(gitems, eng, args.xray_bin, args.singbox_bin,
                                  sp, P2_WORKERS, "sp", ports_base)
            for h, kbps in res.items():
                if isinstance(kbps, int):
                    results[h]["speed_kbps"] = kbps
        log(f"speed done at {int(time.time() - t0)}s")

    # --------------------------------------- server-side geo (inbound cc) ----
    hosts = sorted({p["server"] for p in plan if p["server"]})
    geo_cache = GeoCache(os.path.join(state_dir, "geo_cache.json"))
    geo = Geo(geo_cache.m, log=lambda m: None)
    want = [h for h in hosts if h not in geo_cache]
    if want and budget_left() > 120:
        log(f"geo: looking up {len(want)} server addresses")
        geo.lookup_many(want[:2400])
        geo_cache.update(geo.cache)
        geo_cache.save()
    for p in plan:
        r = results[p["phash"]]
        e = geo_cache.m.get(p["server"])
        if e:
            r["cc"] = e.get("cc", "")
        else:
            r["cc"] = ""

    # ---------------------------------------------------------- bookkeeping --
    out = [results[p["phash"]] for p in plan]
    save_json(os.path.join(data_dir, "results.json"), out)

    # source health: tested / alive per source
    states = SourceStates(os.path.join(state_dir, "sources.json"))
    per_src = {}
    for r in out:
        for s in r.get("srcs") or []:
            d = per_src.setdefault(s, [0, 0])
            d[0] += 1
            d[1] += 1 if (r["alive"] and r["work"]) else 0
    for s, (tested, alive) in per_src.items():
        states.record_results(s, tested, alive)
    states.refresh_retirements()
    states.save()

    # alive recall pool (full configs of the working ones, for re-testing)
    recall_input = [{"phash": r["phash"], "proxy": p, "alive": r["work"],
                     "latency_ms": r["latency_ms"], "exit_cc": r["exit_cc"],
                     "engine": r["engine"]}
                    for p, r in zip(plan, out) if r["work"]]
    update_alive_recall(os.path.join(state_dir, "alive_recall.json"), recall_input)

    n_alive = sum(1 for r in out if r["alive"])
    n_work = sum(1 for r in out if r["work"])
    speeds = [r["speed_kbps"] for r in out if r["speed_kbps"]]
    stats = {
        "ts": time.time(),
        "tested": len(out), "alive": n_alive, "working": n_work,
        "exit_checked": sum(1 for r in out if r["exit_ip"]),
        "speed_tested": len(speeds),
        "avg_speed_kbps": int(sum(speeds) / len(speeds)) if speeds else 0,
        "max_speed_kbps": max(speeds) if speeds else 0,
        "duration_s": int(time.time() - t0),
        "runner_ip": runner_ip, "runner_cc": runner_cc,
        "errors": top_errors(out),
    }
    save_json(os.path.join(data_dir, "test_stats.json"), stats)
    log(json.dumps(stats, indent=2))


def top_errors(out, n=8):
    cnt = {}
    for r in out:
        if not r["alive"] and r.get("error"):
            k = r["error"].split(":")[0][:40]
            cnt[k] = cnt.get(k, 0) + 1
    return dict(sorted(cnt.items(), key=lambda kv: -kv[1])[:n])


if __name__ == "__main__":
    main()
