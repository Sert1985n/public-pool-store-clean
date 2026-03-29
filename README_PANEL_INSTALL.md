# CasaOS Molepool-based Web UI patch

Этот архив подготовлен на основе ваших файлов `molepool_full.zip`.

Что сделано:
- используются именно ваши статические панели из `molepool_full.zip`
- добавлены CasaOS app-пакеты для home + 9 coin pages
- убираются блоки:
  - GMiner firmware
  - Gate exchange
  - Anonymous Mining
  - Multithreaded Stratum
  - PoW Check
  - Services / Agreements / Feedback
- ссылки на `*.molepool.com` переписываются на локальные порты CasaOS
- `https://id.molepool.com/api` переписывается на локальный `/id-api`
- home panel получает `/api/v1/index` от встроенного Python proxy/aggregator
- coin panels проксируют `/api/v1/*` в ваши backend API
- иконки приложений взяты из ваших архивных панелей (`coin.png`)

После копирования в репозиторий:
1. commit
2. push в `main`
3. в CasaOS использовать source URL:
   `https://github.com/Sert1985n/public-pool-store-clean/archive/refs/heads/main.zip`

Порты:
- 8500 home
- 8501 btc
- 8502 bch
- 8503 bsv
- 8504 fb
- 8505 ltc
- 8506 btcs
- 8507 xec
- 8508 dgb
- 8509 rvn
