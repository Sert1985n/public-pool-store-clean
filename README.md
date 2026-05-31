# Public Pool — CasaOS App Store

Модульный CasaOS App Store для Public Pool.

## Source URL для CasaOS

```text
https://github.com/Sert1985n/public-pool/archive/refs/heads/main.zip
```

До переименования репозитория временная ссылка:

```text
https://github.com/Sert1985n/public-pool-store-clean/archive/refs/heads/main.zip
```

## Категория CasaOS

Все приложения должны быть в одной категории:

```text
Public Pool
```

## Приложения

```text
Public Pool Pro
Public Pool PostgreSQL
Public Pool Redis
Public Pool Core
Public Pool Admin
Public Pool Web UI
Bitcoin Node
Bitcoin Cash Node
Bitcoin Cash II Node
Bitcoin Silver Node
Litecoin Node
Dogecoin Node
Peercoin Node
NeurAI Node
Monero Node
```

## Структура

```text
Apps/public-pool-pro/
Apps/public-pool-postgres/
Apps/public-pool-redis/
Apps/public-pool-core/
Apps/public-pool-admin/
Apps/public-pool-web/
Apps/bitcoin/
Apps/bitcoin-cash/
Apps/bitcoin-cash-ii/
Apps/bitcoin-silver/
Apps/litecoin/
Apps/dogecoin/
Apps/peercoin/
Apps/neurai/
Apps/monero/
```

## Данные

Все данные приложений хранятся в `/DATA/AppData/`.

```text
/DATA/AppData/public-pool-pro/web
/DATA/AppData/public-pool-pro/admin-db
/DATA/AppData/public-pool-pro/postgres
/DATA/AppData/public-pool-pro/redis

/DATA/AppData/public-pool-postgres/data
/DATA/AppData/public-pool-redis/data
/DATA/AppData/public-pool-core/config
/DATA/AppData/public-pool-core/logs
/DATA/AppData/public-pool-admin/database
/DATA/AppData/public-pool-admin/config
/DATA/AppData/public-pool-web/html

/DATA/AppData/public-pool-bitcoin/data
/DATA/AppData/public-pool-bitcoin-cash/data
/DATA/AppData/public-pool-bitcoin-cash-ii/data
/DATA/AppData/public-pool-bitcoin-silver/data
/DATA/AppData/public-pool-litecoin/data
/DATA/AppData/public-pool-dogecoin/data
/DATA/AppData/public-pool-peercoin/data
/DATA/AppData/public-pool-neurai/data
/DATA/AppData/public-pool-monero/data
```

## Public Pool Core

Конфиги Miningcore:

```text
/DATA/AppData/public-pool-core/config/config.json
/DATA/AppData/public-pool-core/config/coins.json
```

## Порядок установки

```text
1. Public Pool Pro
2. Public Pool Core
3. нужные монеты
```

Или по частям:

```text
1. Public Pool PostgreSQL
2. Public Pool Redis
3. нужные монеты
4. Public Pool Core
5. Public Pool Admin
6. Public Pool Web UI
```
