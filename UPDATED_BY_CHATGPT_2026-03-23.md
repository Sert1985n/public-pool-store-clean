# Update package prepared on 2026-03-23

Changes in this export:
- Added `Apps/zephyr` as a build-required Zephyr node template based on the official source repository.
- Applied local icon files for all app tiles and rewired compose `icon:` URLs to raw files in this repository.
- Replaced repeated placeholder icons with dedicated or generated fallback icons.
- Updated Monero node and wallet icons using the uploaded XMR icon source.
- Aligned `Apps/postgres` and `Apps/miningcore-webui` database credentials with the Miningcore template defaults:
  - database: `miningcore`
  - user: `miningcore`
  - password: `miningcore`
- Kept Miningcore templates and current-working example files in place for payouts / display configuration.
