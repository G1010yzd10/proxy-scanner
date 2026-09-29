#!/usr/bin/env python3
"""GeoIP lookup (ip-api.com batch + fallback) and DNS resolution with caching."""
import json
import socket
import time
import urllib.request
import urllib.parse

IPAPI_BATCH = "http://ip-api.com/batch?fields=status,query,country,countryCode,as"
FREEGEO = "https://reallyfreegeoip.org/json/"

COUNTRIES = {
    "IR": "Iran", "DE": "Germany", "NL": "Netherlands", "US": "United States",
    "FR": "France", "GB": "United Kingdom", "TR": "Turkey", "RU": "Russia",
    "CA": "Canada", "FI": "Finland", "SE": "Sweden", "CH": "Switzerland",
    "AT": "Austria", "PL": "Poland", "RO": "Romania", "MD": "Moldova",
    "UA": "Ukraine", "CZ": "Czechia", "LT": "Lithuania", "LV": "Latvia",
    "EE": "Estonia", "HK": "Hong Kong", "SG": "Singapore", "JP": "Japan",
    "KR": "South Korea", "CN": "China", "IN": "India", "AE": "UAE",
    "AU": "Australia", "BR": "Brazil", "ZA": "South Africa", "ES": "Spain",
    "IT": "Italy", "PT": "Portugal", "IE": "Ireland", "NO": "Norway",
    "DK": "Denmark", "BE": "Belgium", "LU": "Luxembourg", "BG": "Bulgaria",
    "HU": "Hungary", "SK": "Slovakia", "SI": "Slovenia", "HR": "Croatia",
    "RS": "Serbia", "IL": "Israel", "KZ": "Kazakhstan", "AM": "Armenia",
    "GE": "Georgia", "AZ": "Azerbaijan", "ID": "Indonesia", "MY": "Malaysia",
    "VN": "Vietnam", "TH": "Thailand", "PH": "Philippines", "TW": "Taiwan",
    "AR": "Argentina", "CL": "Chile", "CO": "Colombia", "MX": "Mexico",
    "NZ": "New Zealand", "GR": "Greece", "CY": "Cyprus", "MT": "Malta",
    "IS": "Iceland", "SA": "Saudi Arabia", "QA": "Qatar", "EG": "Egypt",
}


class Geo:
    def __init__(self, cache=None, log=print):
        self.cache = cache or {}
        self.log = log
        self._last_batch_ts = 0.0

    def lookup_many(self, ips):
        """Return/update cache {ip: {"cc":..., "country":..., "as":...}}."""
        need = []
        for ip in ips:
            if ip and ip not in self.cache:
                need.append(ip)
        seen = set()
        need = [ip for ip in need if not (ip in seen or seen.add(ip))]
        for i in range(0, len(need), 100):
            chunk = need[i:i + 100]
            self._batch(chunk)
        return self.cache

    def _batch(self, chunk):
        # ip-api free tier: <=15 req/min -> sleep to stay under
        wait = 4.5 - (time.time() - self._last_batch_ts)
        if wait > 0:
            time.sleep(wait)
        self._last_batch_ts = time.time()
        try:
            req = urllib.request.Request(
                IPAPI_BATCH, data=json.dumps(chunk).encode(),
                headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode())
            for row in data:
                if row.get("status") == "success":
                    self.cache[row["query"]] = {"cc": row.get("countryCode", ""),
                                                "country": row.get("country", ""),
                                                "as": row.get("as", "")}
                else:
                    self.cache[row.get("query", "?")] = {"cc": "", "country": "", "as": ""}
            return
        except Exception as e:
            self.log(f"[geo] ip-api batch failed: {e}")
        # fallback: per-ip reallyfreegeoip
        for ip in chunk:
            try:
                with urllib.request.urlopen(FREEGEO + ip, timeout=8) as r:
                    d = json.loads(r.read().decode())
                self.cache[ip] = {"cc": d.get("country_code", ""),
                                  "country": d.get("country_name", ""), "as": ""}
            except Exception:
                self.cache[ip] = {"cc": "", "country": "", "as": ""}

    def cc(self, ip):
        if not ip:
            return ""
        e = self.cache.get(ip)
        return e["cc"] if e else ""


def resolve_host(host, dns_cache=None, max_age=7 * 86400):
    """Resolve a hostname via DoH (dns.google) with system fallback. Returns ip str or None."""
    now = time.time()
    if dns_cache is not None and host in dns_cache:
        e = dns_cache[host]
        if now - e.get("ts", 0) < max_age and e.get("ip"):
            return e["ip"]
    ip = _doh(host) or _system(host)
    if ip and dns_cache is not None:
        dns_cache[host] = {"ip": ip, "ts": now}
    return ip


def _doh(host):
    try:
        url = "https://dns.google/resolve?" + urllib.parse.urlencode({"name": host, "type": "A"})
        with urllib.request.urlopen(url, timeout=8) as r:
            d = json.loads(r.read().decode())
        for ans in d.get("Answer", []):
            if ans.get("type") == 1:
                return ans["data"]
    except Exception:
        pass
    return None


def _system(host):
    try:
        return socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
    except Exception:
        return None
