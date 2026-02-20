.PHONY: help run install test test-all lint format docker-build docker-up docker-down docker-logs

help:
	@echo "Available commands:"
	@echo "  make run          Start the API server (hot reload)"
	@echo "  make install      Install all dependencies"
	@echo "  make test         Run tests (no Ollama required)"
	@echo "  make test-all     Run all tests including integration (Ollama required)"
	@echo "  make lint         Check code with ruff"
	@echo "  make format       Format code with black"
	@echo "  make docker-build Build the Docker image"
	@echo "  make docker-up    Start all services (API + Ollama)"
	@echo "  make docker-down  Stop all services"
	@echo "  make docker-logs  Stream API logs"

run:
	PYTHONPATH=app uvicorn app.main:app --reload

install:
	pip install -r requirements.txt

test:
	pytest -m "not integration"

test-all:
	pytest

lint:
	ruff check app

format:
	black app tests

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f api
