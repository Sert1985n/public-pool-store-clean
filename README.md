# Public Pool Pro — CasaOS App Store

Чистый репозиторий CasaOS App Store для собственного multi-coin mining pool с Web UI панелью и отдельными приложениями монет.

Идея простая: добавил ссылку магазина в CasaOS, увидел приложения, установил то, что нужно:

```text
Public Pool Pro        # основной стек пула: база, API, Web UI, pool core
Coin Node Apps         # отдельные ноды монет, которые можно ставить по одной
```

## Ссылка для добавления в CasaOS

В CasaOS открой:

```text
App Store → Custom Install / More → Add Source
```

Добавь эту ссылку:

```text
https://github.com/Sert1985n/public-pool-store-clean/archive/refs/heads/main.zip
```

После добавления в магазине должны появиться:

```text
Public Pool Pro
Bitcoin Node
Bitcoin Cash Node
Litecoin Node
Dogecoin Node
Peercoin Node
Monero Node
Neurai Node
другие монеты, которые добавлены в Apps/
```

## Как должна работать установка

Есть два типа приложений.

### 1. Public Pool Pro

Основное приложение пула:

```text
Public Pool Pro
├── PostgreSQL        # база данных пула
├── Redis             # быстрые live-данные и кэш
├── Pool Core         # stratum / shares / blocks / payouts
├── Pool API          # единый API для Web UI
└── Web UI            # главная страница, монеты, аккаунты, выплаты
```

Это приложение должно открывать главную Web UI панель пула.

### 2. Coin Node Apps

Каждая монета может устанавливаться отдельно:

```text
Apps/bitcoin/
├── docker-compose.yml
└── icon.png

Apps/bitcoin-cash/
├── docker-compose.yml
└── icon.png

Apps/litecoin/
├── docker-compose.yml
└── icon.png
```

Так можно поставить только нужные монеты, а не запускать всё сразу.

## Что нельзя делать

В репозитории не должно быть старого мусора:

```text
- временные README_UPLOAD / README_FIX файлы;
- отчёты UPDATED_BY_CHATGPT;
- старые инструкции установки панели;
- архивы временных частей панели;
- заглушки вместо настоящего API;
- fake hashrate / fake reward / fake balance;
- чужая статистика с других пулов;
- жёсткие локальные пути без CasaOS-переменных;
- пароли по умолчанию без возможности изменить;
- приложения без нормального x-casaos metadata;
- приложения без icon.png.
```

## Что должно остаться в чистом репозитории

```text
README.md
category-list.json
Apps/
├── public-pool-pro/
│   ├── docker-compose.yml
│   └── icon.png
├── bitcoin/
│   ├── docker-compose.yml
│   └── icon.png
├── bitcoin-cash/
│   ├── docker-compose.yml
│   └── icon.png
├── litecoin/
│   ├── docker-compose.yml
│   └── icon.png
└── другие монеты...
```

## Требования к каждому приложению CasaOS

Каждая папка в `Apps/` должна быть отдельным устанавливаемым приложением.

Минимум:

```text
docker-compose.yml
icon.png
```

Желательно:

```text
screenshot-1.png
thumbnail.png
```

В `docker-compose.yml` обязательно должно быть:

```text
name
services
x-casaos
```

`x-casaos` должен содержать:

```text
architectures
main
title
description
tagline
developer
author
category
icon
port_map, если есть Web UI
```

## Хранение данных

Все данные должны храниться в CasaOS-директориях:

```text
/DATA/AppData/public-pool-pro/...
/DATA/AppData/bitcoin/...
/DATA/AppData/bitcoin-cash/...
/DATA/AppData/litecoin/...
```

Не использовать старые жёсткие пути вида:

```text
/media/ZimaOS-HD/NodeData/...
```

Такие пути нужно заменить на нормальные CasaOS volume paths.

## Web UI Public Pool Pro

Главная страница должна показывать:

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

Страница монеты должна показывать:

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

Account page должна иметь:

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

## Источники данных

Панель должна брать данные только из собственного стека:

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

## Цель

Сделать нормальный CasaOS App Store:

```text
CasaOS → Add Source → Public Pool Pro + отдельные монеты → Install → работает
```

Без старого мусора, без фейковых данных, без временных панелей и без ручной сборки сломанных частей.
