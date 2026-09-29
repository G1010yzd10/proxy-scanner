#!/usr/bin/env python3
"""Persistent state: source health tracking with auto-retirement, plus the
job-local proxy registry and small cached stores (geo / dns / alive recall).

Committed to git (small, carries memory across ephemeral CI runners):
  state/sources.json      per-source health + rolling seen-hash window
  state/alive_recall.json full configs of recently-alive proxies (re-test pool)
  state/geo_cache.json    ip -> {cc, country, as}
  state/dns_cache.json    host -> ip
  state/history.jsonl     one line per run

Job-local scratch (gitignored, rebuilt every run):
  state/known.json        phash -> {proxy, srcs, first/last seen}
"""
import json
import os
import time

RETIRE_FAIL_STREAK = 10     # consecutive fetch failures
RETIRE_DEAD_STREAK = 10     # consecutive runs where every proxy of the source failed
RETIRE_STALE_DAYS = 10      # days since the source last contributed a new unique proxy
SEEN_PER_SOURCE = 120       # rolling window of recent hashes per source
ALIVE_RECALL_DAYS = 7       # re-test proxies that were alive within this window
ALIVE_RECALL_CAP = 1200     # max entries kept in alive_recall.json
GEO_CAP = 6000
DNS_CAP = 6000


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    os.replace(tmp, path)


def load_jsonl(path):
    out = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except Exception:
                        pass
    return out


def append_jsonl(path, entry):
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")


# ------------------------------------------------------------- sources ------

class SourceStates:
    """Health bookkeeping for every fetch-able source (URL subs + TG channels)."""

    def __init__(self, path):
        self.path = path
        raw = load_json(path, {})
        self.s = raw if isinstance(raw, dict) else {}

    def get(self, name, kind="url", url=""):
        e = self.s.get(name)
        if e is None:
            e = self.s[name] = {
                "kind": kind, "url": url, "first": time.time(), "runs": 0,
                "fails": 0, "last_ok": 0, "n": 0, "new": 0, "total_new": 0,
                "last_new": time.time(), "seen": [],
                "dead": 0, "tested": 0, "alive": 0, "retired": "",
            }
        return e

    def record_fetch(self, name, ok, n_uris, new_hashes, kind="url", url=""):
        e = self.get(name, kind, url)
        e["kind"], e["url"] = kind, url
        e["runs"] = e.get("runs", 0) + 1
        if ok:
            e["fails"] = 0
            e["last_ok"] = time.time()
            e["n"] = n_uris
            seen = e.get("seen") or []
            seenset = set(seen)
            fresh = [h for h in new_hashes if h not in seenset]
            for h in fresh:
                seen.append(h)
                seenset.add(h)
            e["seen"] = seen[-SEEN_PER_SOURCE:]
            e["new"] = len(fresh)
            e["total_new"] = e.get("total_new", 0) + len(fresh)
            if fresh:
                e["last_new"] = time.time()
        else:
            e["fails"] = e.get("fails", 0) + 1
            e["n"] = 0
            e["new"] = 0
        return e

    def record_results(self, name, tested, alive):
        e = self.get(name)
        e["tested"] = tested
        e["alive"] = alive
        if tested > 0 and alive == 0:
            e["dead"] = e.get("dead", 0) + 1
        elif tested > 0:
            e["dead"] = 0

    def retire_reason(self, name):
        e = self.s.get(name)
        if not e or e.get("retired"):
            return e.get("retired") if e else ""
        if e.get("fails", 0) >= RETIRE_FAIL_STREAK:
            return f"{RETIRE_FAIL_STREAK} consecutive fetch failures"
        if e.get("dead", 0) >= RETIRE_DEAD_STREAK:
            return f"{RETIRE_DEAD_STREAK} consecutive runs with 0 alive proxies"
        if time.time() - e.get("last_new", 0) > RETIRE_STALE_DAYS * 86400:
            return f"no new unique proxies for {RETIRE_STALE_DAYS} days"
        return ""

    def refresh_retirements(self):
        for name in list(self.s):
            r = self.retire_reason(name)
            if r and not self.s[name].get("retired"):
                self.s[name]["retired"] = r

    def active_names(self):
        return [n for n, e in self.s.items() if not e.get("retired")]

    def save(self):
        save_json(self.path, self.s)


# ------------------------------------------------------------ registry ------

class Registry:
    """Job-local registry of every proxy seen this run: phash -> meta."""

    def __init__(self, path):
        self.path = path
        self.m = load_json(path, {})

    def observe(self, proxy, phash, source, ts=None):
        ts = ts or time.time()
        e = self.m.get(phash)
        if e is None:
            e = self.m[phash] = {"p": proxy, "srcs": [], "first": ts, "last": ts}
            is_new = True
        else:
            is_new = False
        e["last"] = ts
        if source and source not in e["srcs"]:
            e["srcs"].append(source)
        return is_new

    def sources_of(self, phash):
        e = self.m.get(phash)
        return e["srcs"] if e else []

    def save(self):
        save_json(self.path, self.m)


# ----------------------------------------------------------- alive recall ---

def load_alive_recall(path):
    """{phash: {"p": proxy, "alive": ts, "lat": ms, "ecc": cc, "engine": x}}"""
    return load_json(path, {})


def update_alive_recall(path, results, now=None):
    """Merge this run's alive results into the recall pool; prune by age/cap."""
    now = now or time.time()
    pool = load_alive_recall(path)
    for r in results:
        if r.get("alive"):
            pool[r["phash"]] = {"p": r["proxy"], "alive": now,
                                "lat": r.get("latency_ms"),
                                "ecc": r.get("exit_cc", ""),
                                "engine": r.get("engine", "")}
    cutoff = now - ALIVE_RECALL_DAYS * 86400
    pool = {h: e for h, e in pool.items() if e.get("alive", 0) >= cutoff}
    if len(pool) > ALIVE_RECALL_CAP:
        kept = sorted(pool.items(), key=lambda kv: -kv[1].get("alive", 0))[:ALIVE_RECALL_CAP]
        pool = dict(kept)
    save_json(path, pool)
    return pool


# --------------------------------------------------------------- caches -----

class GeoCache:
    def __init__(self, path):
        self.path = path
        self.m = load_json(path, {})

    def __contains__(self, ip):
        return ip in self.m

    def __getitem__(self, ip):
        return self.m[ip]

    def update(self, d):
        self.m.update(d)
        if len(self.m) > GEO_CAP:
            items = sorted(self.m.items(), key=lambda kv: -kv[1].get("ts", 0))
            self.m = dict(items[:GEO_CAP])

    def save(self):
        save_json(self.path, self.m)


class DnsCache:
    def __init__(self, path):
        self.path = path
        self.m = load_json(path, {})

    def get(self, host, max_age=7 * 86400):
        e = self.m.get(host)
        if e and time.time() - e.get("ts", 0) < max_age and e.get("ip"):
            return e["ip"]
        return None

    def put(self, host, ip):
        if ip:
            self.m[host] = {"ip": ip, "ts": time.time()}
        if len(self.m) > DNS_CAP:
            items = sorted(self.m.items(), key=lambda kv: -kv[1].get("ts", 0))
            self.m = dict(items[:DNS_CAP])

    def save(self):
        save_json(self.path, self.m)
