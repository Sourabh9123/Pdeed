.PHONY: build up down restart logs ps local mongo-shell backend-shell

COMPOSE ?= docker compose

ifneq (,$(wildcard .env))
include .env
export
endif

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

local:
	$(COMPOSE) up -d mongo
	MONGODB_URL=$${LOCAL_MONGODB_URL:-mongodb://localhost:$${MONGODB_PORT:-27018}} uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

mongo-shell:
	$(COMPOSE) exec mongo mongosh printdeed

backend-shell:
	$(COMPOSE) exec backend sh
