.PHONY: up down restart logs init

# Копировать шаблон .env
init:
	cp .env.example .env
	@echo "✓ .env создан, заполни переменные"

# Поднять всё
up:
	docker compose up -d

# Остановить и удалить volumes
down:
	docker compose down -v

# Рестарт
restart:
	docker compose restart

# Логи ClickHouse
logs:
	docker compose logs -f clickhouse

# Зайти в ClickHouse CLI
ch:
	docker compose exec clickhouse clickhouse-client \
		--user $${CLICKHOUSE_USER} \
		--password $${CLICKHOUSE_PASSWORD}

# Применить миграции
migrate:
	docker compose --profile migrate run --rm dbmate migrate

# Новая миграция
migrate-new:
	docker compose --profile migrate run --rm dbmate new $(name)

# Дропнуть миграции
migrate-down: 
	docker compose --profile migrate run --rm dbmate rollback