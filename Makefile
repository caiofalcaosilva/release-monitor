# ==============================
# Project Config
# ==============================

PROJECT_NAME=release-monitor
SERVICE_NAME=release-monitor

COMPOSE=docker compose

# ==============================
# Docker Commands
# ==============================

.PHONY: build
build:
	$(COMPOSE) build

.PHONY: up
up:
	$(COMPOSE) up -d

.PHONY: down
down:
	$(COMPOSE) down

.PHONY: restart
restart: down up

.PHONY: logs
logs:
	$(COMPOSE) logs -f $(SERVICE_NAME)

.PHONY: ps
ps:
	$(COMPOSE) ps $(SERVICE_NAME)

.PHONY: rebuild
rebuild:
	$(COMPOSE) up -d --build

# ==============================
# Development (Local Python)
# ==============================

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: dev
dev:
	python -m app.main

# ==============================
# Maintenance
# ==============================

.PHONY: clean
clean:
	$(COMPOSE) down --volumes --remove-orphans

.PHONY: prune
prune:
	docker system prune -f

# ==============================
# Help
# ==============================

.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "Docker:"
	@echo "  make build     - Build Docker image"
	@echo "  make up        - Start container"
	@echo "  make down      - Stop container"
	@echo "  make restart   - Restart container"
	@echo "  make logs      - Follow logs"
	@echo "  make ps        - Show running containers"
	@echo "  make rebuild   - Rebuild and restart"
	@echo ""
	@echo "Development:"
	@echo "  make install   - Install dependencies locally"
	@echo "  make dev       - Run app locally"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean     - Remove containers and volumes"
	@echo "  make prune     - Docker system prune"