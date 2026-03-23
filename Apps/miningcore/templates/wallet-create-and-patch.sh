#!/usr/bin/env bash
set -euo pipefail
CFG=${1:-/media/ZimaOS-HD/miningcore/config.json}
SERVER_HOST=${2:-192.168.0.175}

echo "Open this file and replace XXX_*_WALLET with real addresses, then run it."
python3 - <<PY
import json, re
cfg_path = "'$CFG'"
server_host = "'$SERVER_HOST'"
addr_map = {
    "btc":"XXX_BTC_WALLET","bch":"XXX_BCH_WALLET","bc2":"XXX_BC2_WALLET","dgb":"XXX_DGB_WALLET",
    "doge":"XXX_DOGE_WALLET","grs":"XXX_GRS_WALLET","rvn":"XXX_RVN_WALLET","btcs":"XXX_BTCS_WALLET",
    "wjk":"XXX_WJK_WALLET","xna":"XXX_XNA_WALLET","lcc":"XXX_LCC_WALLET","lcc2":"XXX_LCC2_WALLET",
    "ltc":"XXX_LTC_WALLET","ppc":"XXX_PPC_WALLET","bch2":"XXX_BCH2_WALLET"
}
with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)
cfg["persistence"]["postgres"]["host"] = server_host
for pool in cfg.get("pools", []):
    pid = pool.get("id")
    if pid in addr_map:
        pool["address"] = addr_map[pid]
        pool["poolFeePercent"] = 1.5
        rr = pool.get("rewardRecipients") or []
        if rr:
            for item in rr:
                item["address"] = addr_map[pid]
                item["percentage"] = 1.5
        else:
            pool["rewardRecipients"] = [{"address": addr_map[pid], "percentage": 1.5}]
    for d in pool.get("daemons", []):
        d["host"] = server_host
        if "zmqBlockNotifySocket" in d and isinstance(d["zmqBlockNotifySocket"], str):
            d["zmqBlockNotifySocket"] = re.sub(r"tcp://[^:]+:", f"tcp://{server_host}:", d["zmqBlockNotifySocket"])
with open(cfg_path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("Updated config:", cfg_path)
PY
