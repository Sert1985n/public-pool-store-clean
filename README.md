# Public Pool Pro — CasaOS App Store

Чистый модульный репозиторий CasaOS App Store для собственного multi-coin mining pool.

Цель проекта — сделать нормальный магазин приложений для CasaOS, где можно установить весь пул целиком или поставить отдельные части по необходимости: базу данных, pool-core / Miningcore, Web UI, админ-панель и отдельные монеты.

## Ссылка для добавления в CasaOS

В CasaOS открой:

```text
App Store → Custom Install / More → Add Source
```

Добавь эту ссылку:

```text
https://github.com/Sert1985n/public-pool-store-clean/archive/refs/heads/main.zip
```

После добавления в магазине должны появиться приложения Public Pool.

## Главный принцип

Репозиторий должен быть модульным.

Нужно иметь возможность установить:

```text
1. PostgreSQL отдельно
2. Redis отдельно
3. Pool Core / Miningcore отдельно
4. Web UI отдельно
5. Admin Panel отдельно
6. каждую монету отдельно
7. готовую полную сборку Public Pool Pro отдельно
```

Монеты должны быть отдельными CasaOS-приложениями, чтобы можно было поставить только нужные daemon-ноды.

## Что нельзя удалять

В папках монет нельзя удалять `icon.png`, если это нормальная иконка монеты.

Иконки нужны для CasaOS App Store, чтобы каждая монета отображалась красиво в магазине.

Пример:

```text
Apps/bitcoin/icon.png
Apps/bitcoin-cash/icon.png
Apps/litecoin/icon.png
Apps/dogecoin/icon.png
Apps/peercoin/icon.png
Apps/neurai/icon.png
Apps/monero/icon.png
```

Если старая папка монеты содержит плохой `docker-compose.yml`, его можно заменить, но `icon.png` лучше сохранить.

## Что нужно чистить

Удалять или заменять нужно старые временные файлы:

```text
- старые README_UPLOAD*.txt
- старые README_FIX.txt
- старые UPDATED_BY_CHATGPT*.md
- старые ICON_STATUS*.md
- старые WEB_UI_UPDATE*.md
- временные manifest-файлы
- старые архивы app.tar.gz / site.tar.gz
- старые ручные патчи панели
- старые docker-compose.yml с hardcoded путями
- старые docker-compose.yml с :latest без контроля
- старые docker-compose.yml с чужими/неподходящими образами
- старые per-coin Web UI заглушки
```

Не нужно оставлять мусор, который не используется для установки нормального приложения.

## Правильная структура репозитория

```text
Apps/
├── public-pool-pro/          # полная установка всего стека
├── public-pool-postgres/     # база PostgreSQL
├── public-pool-redis/        # Redis
├── public-pool-core/         # Miningcore / pool-core
├── public-pool-admin/        # админ-панель управления пулом
├── public-pool-web/          # Web UI для майнеров
├── bitcoin/                  # отдельная нода Bitcoin
├── bitcoin-cash/             # отдельная нода Bitcoin Cash
├── bitcoin-cash-ii/          # отдельная нода Bitcoin Cash II
├── bitcoin-silver/           # отдельная нода Bitcoin Silver
├── litecoin/                 # отдельная нода Litecoin
├── dogecoin/                 # отдельная нода Dogecoin
├── peercoin/                 # отдельная нода Peercoin
├── neurai/                   # отдельная нода Neurai
├── monero/                   # отдельная нода Monero
└── ...                       # другие монеты
```

Каждое приложение должно иметь:

```text
docker-compose.yml
icon.png
```

Для главных приложений желательно добавить:

```text
screenshot-1.png
thumbnail.png
```

## Категории в CasaOS

Нужны нормальные категории:

```text
Public Pool Core
Public Pool Coins
Public Pool Web
Public Pool Tools
```

Старые категории вроде `RetroMike`, `Templates`, `Utilities` и прочий мусор не нужны.

## Базовые приложения

### public-pool-postgres

Отдельное приложение PostgreSQL для базы пула.

Должно хранить данные в:

```text
/DATA/AppData/public-pool-postgres/data
```

Должно использовать нормальные переменные:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
TZ
```

### public-pool-redis

Отдельное приложение Redis для кэша и live-данных.

Должно хранить данные в:

```text
/DATA/AppData/public-pool-redis/data
```

### public-pool-core

Отдельное приложение для Miningcore / pool-core.

Задачи:

```text
- stratum ports
- shares
- blocks
- payouts
- miners
- balances
- pool API
- подключение к PostgreSQL
- подключение к coin daemons
```

Конфиги должны храниться в:

```text
/DATA/AppData/public-pool-core/config
/DATA/AppData/public-pool-core/coins
/DATA/AppData/public-pool-core/logs
```

### public-pool-admin

Админ-панель нужна отдельно.

Она должна позволять:

```text
- добавлять монеты в конфиг пула;
- включать и выключать монеты;
- настраивать stratum ports;
- задавать daemon RPC host / port / user / password;
- создавать wallet config для монет;
- добавлять pool wallet address;
- задавать payout scheme;
- задавать минимальную выплату;
- задавать fee;
- проверять daemon status;
- проверять синхронизацию ноды;
- проверять RPC;
- перегенерировать config для pool-core;
- перезапускать только pool-core, если пользователь сам нажал кнопку.
```

Админ-панель не должна сама удалять данные, кошельки, блокчейн или базу.

### public-pool-web

Web UI для майнеров.

Должен показывать:

```text
- главную страницу монет;
- страницу монеты;
- account page;
- workers;
- rewards;
- payouts;
- blocks;
- charts;
- network stats;
- prices.
```

## Приложения монет

Каждая монета должна быть отдельной папкой в `Apps/`.

Пример:

```text
Apps/bitcoin/
├── docker-compose.yml
└── icon.png

Apps/litecoin/
├── docker-compose.yml
└── icon.png
```

Каждая монета должна:

```text
- ставиться отдельно;
- иметь свой icon.png;
- хранить blockchain data в /DATA/AppData/<app-id>/data;
- открывать только нужные RPC/P2P/ZMQ порты;
- не использовать hardcoded /media/ZimaOS-HD/... пути;
- не использовать одинаковые container_name для разных приложений;
- не хранить пароли прямо как poolpassword без возможности изменения;
- иметь нормальный x-casaos metadata;
- иметь category: Public Pool Coins.
```

## Полная установка Public Pool Pro

`public-pool-pro` — это удобная полная сборка.

Она должна поднимать:

```text
PostgreSQL
Redis
Pool Core / Miningcore
Pool Admin Panel
Pool Web UI
```

Монеты можно не включать все сразу. Лучше сделать так, чтобы пользователь устанавливал нужные монеты отдельно.

## Web UI

Панель должна быть современной, тёмной, быстрой и удобной для майнеров.

### Главная страница

```text
Coin
Algorithm
Miners
Pool Hashrate
Network Hashrate
Network Difficulty
Reward
Price
Blocks
Quick buttons: Coin / Account / Help
```

### Страница монеты

```text
Hashrate chart
Difficulty chart
Ports
Blocks
Miners
Payments
Network stats
Pool fee
Minimum payout
Last block
Daemon status
```

### Account page

```text
Dashboard
Rewards
Payouts
```

Dashboard:

```text
Workers online/offline
Hashrate 30m
Average hashrate 3h
Worker table
Balance
Pending
Immature / unconfirmed
Blocks
Effort
Best share
Last share
```

Rewards:

```text
Hour
12 Hours
24 Hours
Week
Month
```

Payouts:

```text
Time
Amount
Transaction ID
Status
```

## Требования к данным

Панель должна брать статистику только из собственного стека:

```text
miners / workers       → Pool Core / database
hashrate               → shares / performance data
blocks                 → Pool Core / database
payments               → Pool Core / database
balance                → database
network height         → coin daemon RPC
network difficulty     → coin daemon RPC
network hashrate       → coin daemon RPC or calculated API
price                  → market API only as price source
```

Запрещено:

```text
- подставлять чужую статистику;
- копировать данные с Molepool или других пулов;
- показывать fake hashrate / fake reward / fake balance;
- использовать Web UI с заглушками вместо настоящего API;
- делать сломанные Web UI панели на каждую монету;
- завязывать установку на ручные архивы и временные патчи;
- удалять icon.png монет без причины.
```

## Хранение данных

Все важные данные должны храниться в `/DATA/AppData/`.

Примеры:

```text
/DATA/AppData/public-pool-postgres/data
/DATA/AppData/public-pool-redis/data
/DATA/AppData/public-pool-core/config
/DATA/AppData/public-pool-core/coins
/DATA/AppData/public-pool-core/logs
/DATA/AppData/public-pool-admin/data
/DATA/AppData/public-pool-web/config
/DATA/AppData/bitcoin/data
/DATA/AppData/litecoin/data
/DATA/AppData/dogecoin/data
```

Обновление контейнеров не должно удалять базу, blockchain data, wallets, blocks, payouts и историю пула.

## Принцип сборки

Проект должен быть собран как чистый модульный CasaOS App Store:

```text
1. отдельно ставятся базовые сервисы;
2. отдельно ставятся монеты;
3. отдельно ставится Web UI;
4. отдельно ставится admin panel;
5. есть полная сборка public-pool-pro;
6. у каждой монеты есть своя иконка;
7. данные не фейковые;
8. конфиги не хардкодятся под один сервер;
9. всё хранится в /DATA/AppData;
10. установка должна работать из CasaOS без ручной сборки.
```

## Назначение

Итоговая схема:

```text
CasaOS App Store
├── Public Pool Pro
├── Public Pool PostgreSQL
├── Public Pool Redis
├── Public Pool Core
├── Public Pool Admin
├── Public Pool Web UI
├── Bitcoin Node
├── Litecoin Node
├── Dogecoin Node
├── Peercoin Node
├── Neurai Node
├── Monero Node
└── другие монеты
```

Пользователь должен иметь выбор: установить всё сразу или поставить только нужные части по отдельности.
