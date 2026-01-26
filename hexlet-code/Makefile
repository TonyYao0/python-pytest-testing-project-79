install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl --force

lint:
	uv run flake8 page_loader

test:
	uv run pytest
	uv run pytest --cov=page_loader

test-coverage:
	uv run pytest --cov=page_loader --cov-report xml

check:
	uv run pytest
	uv run flake8 page_loader

.PHONY: install build test lint check package-install