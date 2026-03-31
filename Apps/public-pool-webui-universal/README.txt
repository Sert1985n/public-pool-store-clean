Public Pool Web UI Universal (GitHub-ready custom panel)

This CasaOS app uses the custom /app exported from the live working miningcorewebui container,
not the stock theretromike/miningcorewebui panel.

Important fix:
- docker-compose.yml now uses ENTRYPOINT instead of COMMAND
- this forces the container to unpack ./app.tar.gz into /app on every start
- this prevents fallback to the stock panel after refresh/restart

Behavior:
- one container
- external port 81
- coins loaded automatically from Miningcore API
- works with one Miningcore instance for all configured pools
- new coins appear automatically after you add them in Miningcore config and restart Miningcore

Runtime values:
- STRATUM_HOST=public-pool-btc.ru
- icon/thumbnail URL = RetroMike webui.png

Files:
- app.tar.gz       custom live /app
- docker-compose.yml
- icon.png

Patched to hide Support Me and Pool Configuration, and replace footer.
