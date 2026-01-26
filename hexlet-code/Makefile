install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl --force

test:
	uv run pytest
	uv run pytest --cov=page_loader

lint:
	uv run flake8 page_loader

check:
	uv run pytest
	uv run flake8 page_loader

.PHONY: install build test lint check package-install