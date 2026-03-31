Public Pool Web UI Universal (custom panel)

This CasaOS app uses the custom /app exported from the live working miningcorewebui container,
not the stock theretromike/miningcorewebui panel.

Behavior:
- one container
- external port 81
- coins loaded automatically from Miningcore API
- works with one Miningcore instance for all configured pools

Files:
- app.tar.gz       custom live /app
- docker-compose.yml
- icon.png

Patched to hide Support Me and Pool Configuration, and replace footer.
