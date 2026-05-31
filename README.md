# Public Pool Pro — CasaOS App Store

Модульный CasaOS App Store для Public Pool.

## Source URL для CasaOS

```text
https://github.com/Sert1985n/public-pool-store-clean/archive/refs/heads/main.zip
```

## Приложения

Базовые сервисы:

```text
Public Pool Pro
Public Pool PostgreSQL
Public Pool Redis
Public Pool Core
Public Pool Admin
Public Pool Web UI
```

Монеты устанавливаются отдельно из раздела `Public Pool Coins`.

## Структура

```text
Apps/
├── public-pool-pro/
├── public-pool-postgres/
├── public-pool-redis/
├── public-pool-core/
├── public-pool-admin/
├── public-pool-web/
├── bitcoin/
├── bitcoin-cash/
├── litecoin/
├── dogecoin/
├── peercoin/
├── neurai/
├── monero/
└── ...
```

## Данные

Все данные приложений хранятся в `/DATA/AppData/`.

Примеры:

```text
/DATA/AppData/public-pool-postgres/data
/DATA/AppData/public-pool-redis/data
/DATA/AppData/public-pool-core/config
/DATA/AppData/public-pool-core/logs
/DATA/AppData/public-pool-bitcoin/data
/DATA/AppData/public-pool-bitcoin-cash/data
```

## Ноды монет

Каждая монета — отдельное приложение CasaOS с собственным `docker-compose.yml` и `icon.png`.

Bitcoin-like ноды запускаются в prune-режиме. Monero использует свой prune-режим.

## Public Pool Core

`Public Pool Core` запускает Miningcore / pool-core и использует конфиги:

```text
/DATA/AppData/public-pool-core/config/config.json
/DATA/AppData/public-pool-core/config/coins.json
```

## Public Pool Admin

`Public Pool Admin` открывает файловую админ-панель для конфигов пула и данных `/DATA/AppData/`.

## Public Pool Web UI

`Public Pool Web UI` открывает веб-панель пула.

## Порядок установки

Минимальный порядок:

```text
1. Public Pool PostgreSQL
2. Public Pool Redis
3. нужные Coin Nodes
4. Public Pool Core
5. Public Pool Admin
6. Public Pool Web UI
```

Или поставить `Public Pool Pro` как общий стек, а монеты добавить отдельно.
