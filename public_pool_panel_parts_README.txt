Пакет разбит на 3 архива.
Распаковывать в корень репозитория public-pool-store-clean-main так, чтобы получились папки Apps/public-pool-panel-...

Части:
- part1: home + первые 11 монет
- part2: следующие 12 монет
- part3: последние 11 монет

После загрузки в GitHub:
- central home app: public-pool-panel-home, порт 8600
- coin apps: порты 8601-8634
- штатный miningcore-webui не заменяется

Файлы в каждом app:
- docker-compose.yml
- icon.png
- server.py
- site.tar.gz
