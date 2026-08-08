.PHONY: install lint fmt types test cov check clean

install:
	uv sync

lint:
	uv run ruff check src/ tests/

fmt:
	uv run ruff format src/ tests/

types:
	uv run mypy

test:
	uv run pytest

cov:
	uv run pytest --cov=keel --cov-report=term-missing --cov-report=html:artifacts/htmlcov

check: lint types test
	@echo "all checks passed"

clean:
	rm -rf .mypy_cache .pytest_cache .ruff_cache artifacts/htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
