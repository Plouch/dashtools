.PHONY: help build up down restart logs clean dev-backend dev-frontend test install-backend install-frontend

.DEFAULT_GOAL := help

COMPOSE := docker compose
COMPOSE_FILE := docker-compose.yml
BACKEND_DIR := backend
FRONTEND_DIR := frontend

GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m

help:
	@echo "$(GREEN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# Docker Compose Commands
build: ## Build Docker images
	@echo "$(GREEN)Building Docker images...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) build

up: ## Start all services (SQLite mode)
	@echo "$(GREEN)Starting services with SQLite...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) up -d

up-db: ## Start all services with PostgreSQL
	@echo "$(GREEN)Starting services with PostgreSQL...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) --profile with-db up -d

down: ## Stop all services
	@echo "$(GREEN)Stopping services...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) down

down-db: ## Stop all services including PostgreSQL
	@echo "$(GREEN)Stopping all services including PostgreSQL...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) --profile with-db down

restart: ## Restart all services
	@echo "$(GREEN)Restarting services...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) restart

restart-db: ## Restart all services including PostgreSQL
	@echo "$(GREEN)Restarting all services including PostgreSQL...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) --profile with-db restart

logs: ## Show logs from all services
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f

logs-backend: ## Show backend logs
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f backend

logs-frontend: ## Show frontend logs
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f frontend

logs-db: ## Show PostgreSQL logs
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f postgres

ps: ## Show running containers
	$(COMPOSE) -f $(COMPOSE_FILE) ps

# Development Commands
dev-backend: ## Start backend in development mode (local, not Docker)
	@echo "$(GREEN)Starting backend in development mode...$(NC)"
	cd $(BACKEND_DIR) && python app.py

dev-frontend: ## Start frontend in development mode (local, not Docker)
	@echo "$(GREEN)Starting frontend in development mode...$(NC)"
	cd $(FRONTEND_DIR) && npm run dev

dev: ## Start both backend and frontend in development mode (requires two terminals)
	@echo "$(YELLOW)Starting development servers...$(NC)"
	@echo "$(YELLOW)Backend: cd $(BACKEND_DIR) && python app.py$(NC)"
	@echo "$(YELLOW)Frontend: cd $(FRONTEND_DIR) && npm run dev$(NC)"

# Installation Commands
install-backend: ## Install backend dependencies
	@echo "$(GREEN)Installing backend dependencies...$(NC)"
	cd $(BACKEND_DIR) && \
	if command -v uv >/dev/null 2>&1; then \
		uv pip install -r requirements.txt; \
	else \
		pip install -r requirements.txt; \
	fi

install-frontend: ## Install frontend dependencies
	@echo "$(GREEN)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && \
	if [ -f pnpm-lock.yaml ]; then \
		npm install -g pnpm && pnpm install; \
	else \
		npm install; \
	fi

install: install-backend install-frontend ## Install all dependencies

# Build Commands
build-backend: ## Build only backend image
	$(COMPOSE) -f $(COMPOSE_FILE) build backend

build-frontend: ## Build only frontend image
	$(COMPOSE) -f $(COMPOSE_FILE) build frontend

rebuild: ## Rebuild all images without cache
	@echo "$(GREEN)Rebuilding all images...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) build --no-cache

rebuild-backend: ## Rebuild backend image without cache
	$(COMPOSE) -f $(COMPOSE_FILE) build --no-cache backend

rebuild-frontend: ## Rebuild frontend image without cache
	$(COMPOSE) -f $(COMPOSE_FILE) build --no-cache frontend

# Cleanup Commands
clean: ## Remove containers, networks, and volumes
	@echo "$(GREEN)Cleaning up Docker resources...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) down -v --remove-orphans

clean-all: clean ## Remove containers, networks, volumes, and images
	@echo "$(GREEN)Removing Docker images...$(NC)"
	$(COMPOSE) -f $(COMPOSE_FILE) down -v --rmi all --remove-orphans

clean-volumes: ## Remove all volumes (WARNING: deletes data)
	@echo "$(YELLOW)WARNING: This will delete all database data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE) -f $(COMPOSE_FILE) down -v; \
	fi

# Database Commands
db-shell: ## Open PostgreSQL shell (requires PostgreSQL service running)
	$(COMPOSE) -f $(COMPOSE_FILE) exec postgres psql -U $$(grep POSTGRES_USER .env 2>/dev/null | cut -d '=' -f2 || echo "dashtools") -d $$(grep POSTGRES_DB .env 2>/dev/null | cut -d '=' -f2 || echo "dashtools")

db-backup: ## Backup PostgreSQL database
	@echo "$(GREEN)Backing up PostgreSQL database...$(NC)"
	@mkdir -p backups
	$(COMPOSE) -f $(COMPOSE_FILE) exec -T postgres pg_dump -U $$(grep POSTGRES_USER .env 2>/dev/null | cut -d '=' -f2 || echo "dashtools") $$(grep POSTGRES_DB .env 2>/dev/null | cut -d '=' -f2 || echo "dashtools") > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Backup saved to backups/$(NC)"

# Testing Commands
test-backend: ## Run backend tests
	@echo "$(GREEN)Running backend tests...$(NC)"
	cd $(BACKEND_DIR) && python -m pytest tests/ || echo "No tests found"

test-frontend: ## Run frontend tests
	@echo "$(GREEN)Running frontend tests...$(NC)"
	cd $(FRONTEND_DIR) && npm test || echo "No tests found"

test: test-backend test-frontend ## Run all tests

# Utility Commands
shell-backend: ## Open shell in backend container
	$(COMPOSE) -f $(COMPOSE_FILE) exec backend /bin/bash || $(COMPOSE) -f $(COMPOSE_FILE) exec backend /bin/sh

shell-frontend: ## Open shell in frontend container
	$(COMPOSE) -f $(COMPOSE_FILE) exec frontend /bin/sh

status: ## Show status of all services
	@echo "$(GREEN)Service Status:$(NC)"
	@$(COMPOSE) -f $(COMPOSE_FILE) ps
	@echo ""
	@echo "$(GREEN)Health Check:$(NC)"
	@curl -s http://localhost:5000/api/health 2>/dev/null && echo "Backend: OK" || echo "Backend: Not responding"
	@curl -s http://localhost:80 2>/dev/null >/dev/null && echo "Frontend: OK" || echo "Frontend: Not responding"

# Quick Start
quickstart: build up ## Build and start all services (quick start)
	@echo "$(GREEN)Services started!$(NC)"
	@echo "$(GREEN)Frontend: http://localhost:80$(NC)"
	@echo "$(GREEN)Backend API: http://localhost:5000$(NC)"

quickstart-db: build up-db ## Build and start all services with PostgreSQL
	@echo "$(GREEN)Services started with PostgreSQL!$(NC)"
	@echo "$(GREEN)Frontend: http://localhost:80$(NC)"
	@echo "$(GREEN)Backend API: http://localhost:5000$(NC)"
	@echo "$(GREEN)PostgreSQL: localhost:5432$(NC)"

