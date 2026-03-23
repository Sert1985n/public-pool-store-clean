# Public Pool Web UI update

This update adds two installable CasaOS apps:

- `Apps/public-pool-webui-home` → central page on port `8500`
- `Apps/public-pool-webui-btc` → BTC reference page on port `8501`

Both apps:
- use current server hostname automatically
- fetch live data from `http://<current-host>:4000/api`
- do not hardcode an old server IP
- do not modify BCH 8502

Next step after upload:
- install `public-pool-webui-home`
- install `public-pool-webui-btc`
- then clone BTC page structure to BC2/BTCS/LCC/WJK/RVN
