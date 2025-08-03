# Makefile for WanderWise

.PHONY: install run dev test lint format docker-build docker-run clean

install:
	poetry install

run:
	poetry run python -m wanderwise.main

dev:
	poetry run uvicorn wanderwise.main:app --reload --host 0.0.0.0 --port 8000

test:
	poetry run pytest --cov=src --cov-report=term-missing

lint:
	poetry run black --check src
	poetry run isort --check-only src
	poetry run flake8 src
	poetry run mypy src
	poetry run bandit -r src

format:
	poetry run black src
	poetry run isort src

clean:
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov

docker-build:
	docker build -t wanderwise .

docker-run:
	docker run --env-file .env -p 8000:8000 wanderwise
