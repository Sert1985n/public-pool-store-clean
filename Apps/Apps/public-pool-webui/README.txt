This folder is ready for CasaOS App Store.

Put this folder in:
Apps/public-pool-webui

Files:
- docker-compose.yml
- icon.png
- app.tar.gz

What it does:
- installs one custom Miningcore Web UI
- downloads app.tar.gz from this GitHub repo at container start
- uses Miningcore API from host.docker.internal:4000/api
- keeps round coin icons via app/wwwroot/js/site.js

Default port:
- 81 -> 8080
