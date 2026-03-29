import json, os, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

SITE_ROOT=os.environ.get("SITE_ROOT","/srv/site")
APP_MODE=os.environ.get("APP_MODE","coin")
PORT=int(os.environ.get("PORT","8080"))
API_UPSTREAM=os.environ.get("API_UPSTREAM","").strip()

def send_json(handler,obj,code=200):
    body=json.dumps(obj).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type","application/json; charset=utf-8")
    handler.send_header("Content-Length",str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)

def fetch_json(url, timeout=5):
    req=urllib.request.Request(url, headers={"User-Agent":"PublicPoolPanel/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8","ignore"))

def proxy(handler, base, path):
    try:
        req=urllib.request.Request(base.rstrip("/")+path, headers={"User-Agent":"PublicPoolPanel/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            body=resp.read()
            handler.send_response(resp.status)
            handler.send_header("Content-Type", resp.headers.get("Content-Type","application/json; charset=utf-8"))
            handler.send_header("Content-Length", str(len(body)))
            handler.end_headers()
            handler.wfile.write(body)
            return True
    except Exception:
        return False

def stub_stats():
    return {
        "algo": os.environ.get("COIN_ALGO",""),
        "scheme": "SOLO",
        "reward": 0,
        "fee": 0,
        "totalMiners": 0,
        "totalHashrate": 0,
        "currentEffort": 0,
        "lastBlockFound": 0,
        "newBlocks": 0,
        "totalBlocks": 0,
        "networkHashrate": 0,
        "networkDifficulty": 0,
        "currentHeight": 0,
        "btc": "0",
        "btc_24h_change": "0",
        "usd": "0",
        "usd_24h_change": "0",
        "chart": []
    }
def stub_blocks():
    return {"luck":{},"candidate":[],"blocks":[]}
def stub_miners():
    return {"miners":[],"totalCount":0}
def stub_account(login=""):
    return {
        "login": login,
        "currentHashrate": 0,
        "averageHashrate": 0,
        "lastBlockFound": 0,
        "blocksFound": 0,
        "personalShares": 0,
        "personalEffort": 0,
        "balance": 0,
        "pending": 0,
        "immature": 0,
        "daysReward": 0,
        "workerTotal": 0,
        "workerOnline": 0,
        "workerOffline": 0,
        "chart": [],
        "bestShare": {"time":0,"share":0,"netDiff":0,"port":0},
        "workers": []
    }

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):
        super().__init__(*a, directory=SITE_ROOT, **kw)

    def log_message(self, fmt, *args):
        print(fmt % args)

    def do_GET(self):
        path=urlparse(self.path).path

        if path == "/patch.js":
            return self.serve_patch()

        if APP_MODE == "home" and path == "/api/v1/index":
            coins=json.loads(os.environ.get("COINS_JSON","[]"))
            result=[]
            for c in coins:
                row={
                    "coin": c["symbol"],
                    "name": c["name"],
                    "algo": c.get("algo",""),
                    "totalMiners": 0,
                    "totalHashrate": 0,
                    "networkHashrate": 0,
                    "networkDifficulty": 0,
                    "usd": 0,
                    "usd_24h_change": 0,
                    "reward": 0
                }
                panel=os.environ.get("PANEL_"+c["symbol"],"")
                if panel:
                    try:
                        payload=fetch_json(panel.rstrip("/")+"/api/v1/stats")
                        data=payload.get("result", payload)
                        if isinstance(data, dict):
                            for key in ["totalMiners","totalHashrate","networkHashrate","networkDifficulty","usd","usd_24h_change","reward","algo"]:
                                if key in data and data[key] is not None:
                                    row[key]=data[key]
                    except Exception:
                        pass
                result.append(row)
            return send_json(self, {"status":True,"result":result})

        if APP_MODE == "home" and path.startswith("/coin/") and path.endswith(".png"):
            code=os.path.basename(path)[:-4].upper()
            fp=os.environ.get("ICON_"+code, "")
            if fp and os.path.isfile(fp):
                body=open(fp,"rb").read()
                self.send_response(200)
                self.send_header("Content-Type","image/png")
                self.send_header("Content-Length",str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self.send_response(404)
            self.end_headers()
            return

        if APP_MODE == "coin" and path.startswith("/api/v1/"):
            if API_UPSTREAM and proxy(self, API_UPSTREAM, self.path):
                return
            if path == "/api/v1/stats":
                return send_json(self, {"status":True,"result":stub_stats()})
            if path == "/api/v1/blocks":
                return send_json(self, {"status":True,"result":stub_blocks()})
            if path == "/api/v1/newBlock":
                return send_json(self, 0)
            if path.startswith("/api/v1/miners/"):
                return send_json(self, {"status":True,"result":stub_miners()})
            if path.startswith("/api/v1/account/") and path.endswith("/payments"):
                return send_json(self, {"status":True,"result":[]})
            if path.startswith("/api/v1/account/") and path.endswith("/rewards"):
                return send_json(self, {"status":True,"result":{"luck":{},"candidate":[],"blocks":[]}})
            if path.startswith("/api/v1/account/"):
                parts=path.split("/")
                login=parts[4] if len(parts)>4 else ""
                return send_json(self, {"status":True,"result":stub_account(login)})

        return super().do_GET()

    def serve_patch(self):
        title=os.environ.get("APP_TITLE","Pool Panel")
        home=os.environ.get("HOME_URL","/")
        phrases=[
            "Services","Agreements","Feedback","Anonymous Mining",
            "No Registration Required To Start.","Multithreaded Stratum",
            "Ultra-low latency, asynchronous I/O.","PoW Check",
            "Native code for maximum performance."
        ]
        body=("""(function(){const title=%s,home=%s,phrases=%s;
function clean(){
document.title=title;
document.querySelectorAll('footer').forEach(e=>e.remove());
document.querySelectorAll('a[href*="molepool.com"]').forEach(a=>a.href=home);
document.querySelectorAll('*').forEach(el=>{
 const t=(el.textContent||'').trim();
 if(t==='Molepool') el.textContent=title;
 if(phrases.includes(t)){ const p=el.closest('.v-col,.v-card,a,div,section')||el; if(p&&p!==document.body) p.remove(); }
});
}
clean();setTimeout(clean,300);setTimeout(clean,1500);
})();""" % (json.dumps(title), json.dumps(home), json.dumps(phrases))).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","application/javascript; charset=utf-8")
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__=="__main__":
    os.chdir(SITE_ROOT)
    srv=ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    srv.serve_forever()
