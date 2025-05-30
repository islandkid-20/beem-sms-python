.PHONY: install install-dev test lint format type-check clean build upload docs

# Installation
install:
	pip install -e .

install-dev:
	pip install -e .[dev]

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=beem_sms --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 beem_sms tests --max-line-length=88 --extend-ignore=E203,W503

format:
	black beem_sms tests
	@command -v isort >/dev/null 2>&1 && isort beem_sms tests || echo "⚠️  isort not found, skipping import sorting"

format-check:
	black --check beem_sms tests
	@command -v isort >/dev/null 2>&1 && isort --check-only beem_sms tests || echo "⚠️  isort not found, skipping import sort check"

type-check:
	mypy beem_sms

# Security
security:
	bandit -r beem_sms/

# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

# Documentation
docs:
	cd docs && make html

docs-serve:
	cd docs/_build/html && python -m http.server 8000

# Build and upload
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

build: clean
	python -m build

upload-test: build
	python -m twine upload --repository testpypi dist/*

upload: build
	python -m twine upload dist/*

# Virtual environment
venv:
	python3 -m venv venv
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

# Development
dev-setup: venv
	@echo "Activating virtual environment and installing dependencies..."
	bash -c "source venv/bin/activate && pip install --upgrade pip && pip install -e .[dev] && pre-commit install"
	@echo "Development environment setup complete!"
	@echo "To activate: source venv/bin/activate"

check: format-check lint type-check test
	@echo "All checks passed!"