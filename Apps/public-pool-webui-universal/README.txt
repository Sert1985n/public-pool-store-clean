Universal CasaOS app for Miningcore Web UI.

What it does:
- runs one panel for all coins
- uses one external port: 81
- loads coin list dynamically from Miningcore API
- new enabled pools appear automatically after you add them to Miningcore config and restart Miningcore

Default API:
- http://host.docker.internal:4000/api

Files:
- docker-compose.yml
- app.tar.gz
- icon.png

Notes:
- uninstall or stop any old panel already using port 81 before installing this app
- this app expects Miningcore API to be reachable on port 4000 on the same server
