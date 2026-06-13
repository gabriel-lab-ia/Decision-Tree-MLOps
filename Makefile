OBSERVABILITY_SCRIPTS = scripts/demo_predict.py scripts/telemetry_smoke_check.py scripts/run_monitoring_summary.py scripts/export_model_explainability.py

.PHONY: help venv install lint format test train api validate demo telemetry-smoke monitoring-summary explain docker-up docker-down mlflow clean

help:
	@echo "Available commands:"
	@echo "  make venv        - Create local .venv with uv"
	@echo "  make install     - Install project dependencies"
	@echo "  make lint        - Run ruff and black checks"
	@echo "  make format      - Auto-format code"
	@echo "  make test        - Run tests"
	@echo "  make train       - Train model"
	@echo "  make validate    - Validate model metrics"
	@echo "  make api         - Run FastAPI app"
	@echo "  make demo        - Send demo transactions to the API"
	@echo "  make telemetry-smoke - Check recent telemetry fail-soft behavior"
	@echo "  make monitoring-summary - Print MongoDB monitoring summary"
	@echo "  make explain     - Print Decision Tree feature importances"
	@echo "  make docker-up   - Start Docker Compose services"
	@echo "  make docker-down - Stop Docker Compose services"
	@echo "  make mlflow      - Run MLflow UI"

venv:
	uv venv .venv --python 3.11

install:
	uv pip install -e ".[dev]"

lint:
	uv run ruff check src tests $(OBSERVABILITY_SCRIPTS)
	uv run black --check src tests $(OBSERVABILITY_SCRIPTS)

format:
	uv run ruff check src tests $(OBSERVABILITY_SCRIPTS) --fix
	uv run black src tests $(OBSERVABILITY_SCRIPTS)

test:
	uv run pytest

train:
	uv run python scripts/run_training.py

api:
	uv run python scripts/run_api.py

validate:
	uv run python scripts/validate_model.py

demo:
	uv run python scripts/demo_predict.py

telemetry-smoke:
	uv run python scripts/telemetry_smoke_check.py

monitoring-summary:
	uv run python scripts/run_monitoring_summary.py

explain:
	uv run python scripts/export_model_explainability.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

mlflow:
	uv run mlflow ui --host 0.0.0.0 --port 5000

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
