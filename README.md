# Public Pool Pro — CasaOS App Store

Чистый репозиторий CasaOS App Store для установки собственного multi-coin mining pool с Web UI панелью.

Цель проекта — одна понятная установка в CasaOS: добавил ссылку на магазин, выбрал приложение **Public Pool Pro**, нажал **Install**, получил рабочий стек пула с Web UI, API, базой данных и конфигурациями монет.

## Ссылка для добавления в CasaOS

В CasaOS открой:

```text
App Store → Custom Install / More → Add Source
```

Добавь эту ссылку:

```text
https://github.com/Sert1985n/public-pool-store-clean/archive/refs/heads/main.zip
```

После добавления в магазине должно появиться приложение **Public Pool Pro**.

## Что должно устанавливаться

Основное приложение должно поднимать полный стек пула:

```text
Public Pool Pro
├── PostgreSQL        # база данных пула
├── Redis             # быстрые live-данные и кэш
├── Pool Core         # stratum / shares / blocks / payouts
├── Pool API          # единый API для Web UI
├── Web UI            # главная страница, монеты, аккаунты, выплаты
└── Coin Configs      # конфигурации монет и daemon RPC
```

Все данные в панели должны быть реальными. Нельзя использовать фейковые значения, заглушки, нули вместо статистики или чужие данные с других пулов.

## Web UI

Панель должна быть современной, тёмной, быстрой и удобной для майнеров.

### Главная страница

На главной странице должен быть список всех монет:

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

Для каждой монеты должна быть отдельная страница:

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

Страница аккаунта должна иметь вкладки:

```text
Dashboard
Rewards
Payouts
```

Dashboard должен показывать:

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

Rewards должен показывать интервалы:

```text
Hour
12 Hours
24 Hours
Week
Month
```

Payouts должен показывать:

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
- делать отдельные сломанные панели на каждую монету;
- завязывать установку на ручные архивы и временные патчи.
```

## Правильная структура CasaOS App Store

Репозиторий должен иметь такую структуру:

```text
Apps/
└── public-pool-pro/
    ├── docker-compose.yml
    ├── icon.png
    ├── screenshot-1.png
    └── thumbnail.png
```

Главное приложение:

```text
Apps/public-pool-pro/docker-compose.yml
```

Именно оно должно быть основным приложением в CasaOS.

## Порты

Рекомендуемые порты по умолчанию:

```text
Web UI:        8095
Pool API:      внутренний порт контейнерной сети
PostgreSQL:    внутренний порт контейнерной сети
Redis:         внутренний порт контейнерной сети
Stratum:       отдельные порты по монетам
```

Web UI должен открываться из CasaOS по кнопке приложения.

## Хранение данных

Все важные данные должны храниться в постоянных директориях CasaOS:

```text
/DATA/AppData/public-pool-pro/postgres
/DATA/AppData/public-pool-pro/redis
/DATA/AppData/public-pool-pro/config
/DATA/AppData/public-pool-pro/coins
/DATA/AppData/public-pool-pro/logs
```

Удаление или обновление контейнеров не должно удалять базу, конфиги, блоки, выплаты и историю пула.

## Принцип сборки

Проект должен быть собран как чистая профессиональная сборка:

```text
1. одно основное приложение в CasaOS;
2. нормальный docker-compose.yml;
3. нормальный x-casaos metadata;
4. реальные конфиги монет;
5. собственный API;
6. новая Web UI без старых заглушек;
7. стабильный запуск после перезагрузки;
8. понятные логи;
9. безопасное хранение данных;
10. обновление без потери данных.
```

## Статус

Этот репозиторий предназначен для чистой сборки **Public Pool Pro**.

Старые тестовые панели, временные заглушки, непонятные per-coin приложения и ручные патчи не должны использоваться как основа. Их нужно заменить одним нормальным CasaOS-приложением, которое устанавливает полноценный mining pool stack и открывает единую Web UI панель.

## Назначение

**Public Pool Pro** должен быть готовой self-hosted системой для своего mining pool:

```text
CasaOS App Store → Public Pool Pro → Install → Web UI → рабочий пул
```

Без ручного собирания сломанных частей, без фейковых данных и без старых временных решений.
