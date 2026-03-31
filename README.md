# Public Pool Store Clean

Кастомный CasaOS App Store для `public-pool-btc.ru`.

## Source

Используй этот source URL в CasaOS:

```text
https://github.com/Sert1985n/public-pool-store-clean/archive/refs/heads/main.zip
```

## Что внутри

- ноды монет в `Apps/<coin>/docker-compose.yml`
- `Miningcore`
- `Miningcore Web UI`
- `PostgreSQL`
- шаблоны и примеры конфигов


## Важные заметки

- `xna` и `ppc` ждут полной синхронизации нод
- `xmr wallet` настраивается после полной синхронизации `xmr`
- `bch2` требует отдельного патча движка `Miningcore` для разбора адреса
- `pepew` вынесен отдельно из-за несовместимости бинарника с CPU (Exit 132)
