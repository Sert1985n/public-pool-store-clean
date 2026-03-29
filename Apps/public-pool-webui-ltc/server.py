#!/usr/bin/env python3
import os, json, mimetypes, urllib.parse, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SITE_ROOT = os.environ.get("SITE_ROOT", "/srv/site")
APP_MODE = os.environ.get("APP_MODE", "coin")
PORT = int(os.environ.get("PORT", "8500"))
API_UPSTREAM = os.environ.get("API_UPSTREAM", "").rstrip("/")
ID_API_UPSTREAM = os.environ.get("ID_API_UPSTREAM", "").rstrip("/")

COINS = [
    {"id":"btc","symbol":"BTC","name":"Bitcoin","env":"API_BTC","algo":"SHA-256"},
    {"id":"bch","symbol":"BCH","name":"Bitcoin Cash","env":"API_BCH","algo":"SHA-256"},
    {"id":"bsv","symbol":"BSV","name":"Bitcoin SV","env":"API_BSV","algo":"SHA-256"},
    {"id":"fb","symbol":"FB","name":"Fractal Bitcoin","env":"API_FB","algo":"SHA-256"},
    {"id":"ltc","symbol":"LTC","name":"Litecoin","env":"API_LTC","algo":"Scrypt"},
    {"id":"btcs","symbol":"BTCS","name":"Bitcoin Silver","env":"API_BTCS","algo":"Scrypt"},
    {"id":"xec","symbol":"XEC","name":"eCash","env":"API_XEC","algo":"SHA-256"},
    {"id":"dgb","symbol":"DGB_SCRYPT","name":"DigiByte","env":"API_DGB","algo":"Scrypt"},
    {"id":"rvn","symbol":"RVN","name":"Ravencoin","env":"API_RVN","algo":"KAWPOW"},
]

def json_bytes(obj):
    return json.dumps(obj, ensure_ascii=False).encode("utf-8")

def first(*vals, default=0):
    for v in vals:
        if v is None: continue
        if isinstance(v, str) and not v.strip(): continue
        return v
    return default

def to_num(v, default=0):
    try:
        if v is None: return default
        if isinstance(v, str): v = v.replace(",", "")
        return float(v)
    except Exception:
        return default

def upstream_join(base, path_and_query):
    if not base:
        return ""
    if base.endswith("/api/v1") and path_and_query.startswith("/api/v1"):
        return base + path_and_query[len("/api/v1"):]
    if base.endswith("/api") and path_and_query.startswith("/api/"):
        return base + path_and_query[len("/api"):]
    return base + path_and_query

def fetch_json(url, timeout=8):
    req = urllib.request.Request(url, headers={"User-Agent":"PoolPanel/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="ignore"))

def map_coin_stats(coin, payload):
    result = payload.get("result", payload) if isinstance(payload, dict) else {}
    pool = result.get("poolStats", {}) if isinstance(result, dict) else {}
    net = result.get("networkStats", {}) if isinstance(result, dict) else {}
    return {
        "coin": coin["symbol"],
        "name": first(result.get("name"), coin["name"], default=coin["name"]),
        "algo": first(result.get("algo"), result.get("algorithm"), pool.get("algo"), coin["algo"], default=coin["algo"]),
        "totalMiners": int(to_num(first(result.get("totalMiners"), result.get("minersTotal"), result.get("connectedMiners"), pool.get("connectedMiners"), default=0))),
        "totalHashrate": to_num(first(result.get("totalHashrate"), result.get("poolHashrate"), pool.get("poolHashrate"), default=0)),
        "networkHashrate": to_num(first(result.get("networkHashrate"), net.get("networkHashrate"), default=0)),
        "networkDifficulty": to_num(first(result.get("networkDifficulty"), net.get("networkDifficulty"), default=0)),
        "usd": to_num(first(result.get("usd"), result.get("priceUsd"), result.get("currentPrice"), default=0)),
        "usd_24h_change": to_num(first(result.get("usd_24h_change"), result.get("priceChange24h"), result.get("change24h"), default=0)),
        "reward": to_num(first(result.get("reward"), result.get("blockReward"), pool.get("reward"), net.get("blockReward"), default=0)),
    }

class Handler(BaseHTTPRequestHandler):
    server_version = "PoolPanel/1.0"

    def _send(self, status, body=b"", content_type="text/plain; charset=utf-8"):
        if isinstance(body, str): body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self): self.handle_any()
    def do_POST(self): self.handle_any()
    def do_PUT(self): self.handle_any()
    def do_DELETE(self): self.handle_any()
    def do_HEAD(self): self.handle_any()

    def proxy(self, base, strip_prefix=None):
        if not base:
            self._send(404, json_bytes({"status": False, "error": "upstream_not_configured"}), "application/json; charset=utf-8"); return
        path = self.path
        if strip_prefix and path.startswith(strip_prefix):
            path = path[len(strip_prefix):] or "/"
            if not path.startswith("/"): path = "/" + path
        target = upstream_join(base, path)
        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length else None
        headers = {k:v for k,v in self.headers.items() if k.lower() not in ("host","content-length","accept-encoding","connection")}
        try:
            req = urllib.request.Request(target, data=body, method=self.command, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                ct = resp.headers.get("Content-Type", "application/octet-stream")
                self._send(resp.status, data, ct)
        except urllib.error.HTTPError as e:
            self._send(e.code, e.read(), "application/json; charset=utf-8")
        except Exception as e:
            self._send(502, json_bytes({"status": False, "error": "proxy_error", "detail": str(e)}), "application/json; charset=utf-8")

    def handle_home_index(self):
        items = []
        for coin in COINS:
            api = os.environ.get(coin["env"], "").strip().rstrip("/")
            if not api:
                items.append({
                    "coin": coin["symbol"], "name": coin["name"], "algo": coin["algo"],
                    "totalMiners": 0, "totalHashrate": 0, "networkHashrate": 0,
                    "networkDifficulty": 0, "usd": 0, "usd_24h_change": 0, "reward": 0
                })
                continue
            try:
                payload = fetch_json(upstream_join(api, "/api/v1/stats"))
                items.append(map_coin_stats(coin, payload))
            except Exception:
                items.append({
                    "coin": coin["symbol"], "name": coin["name"], "algo": coin["algo"],
                    "totalMiners": 0, "totalHashrate": 0, "networkHashrate": 0,
                    "networkDifficulty": 0, "usd": 0, "usd_24h_change": 0, "reward": 0
                })
        self._send(200, json_bytes({"status": True, "result": items}), "application/json; charset=utf-8")

    def serve_static(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/": path = "/index.html"
        safe = os.path.normpath(path.lstrip("/"))
        full = os.path.abspath(os.path.join(SITE_ROOT, safe))
        if not full.startswith(os.path.abspath(SITE_ROOT)):
            self._send(403, "Forbidden"); return
        if os.path.isdir(full): full = os.path.join(full, "index.html")
        if not os.path.exists(full):
            self._send(404, "Not Found"); return
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        with open(full, "rb") as f:
            data = f.read()
        self._send(200, data, ctype)

    def handle_any(self):
        path = urllib.parse.urlparse(self.path).path
        if APP_MODE == "home" and path == "/api/v1/index":
            self.handle_home_index(); return
        if path.startswith("/id-api"):
            self.proxy(ID_API_UPSTREAM, strip_prefix="/id-api"); return
        if path.startswith("/api/"):
            self.proxy(API_UPSTREAM); return
        self.serve_static()

if __name__ == "__main__":
    os.chdir(SITE_ROOT)
    print(f"Serving {APP_MODE} from {SITE_ROOT} on :{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
