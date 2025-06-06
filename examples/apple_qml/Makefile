# Apple QML System - Makefile für Development Workflows

# === VARIABLEN ===
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
FLAKE8 := flake8
MYPY := mypy
ISORT := isort

# Verzeichnisse
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs
EXAMPLES_DIR := examples
OUTPUT_DIR := outputs

# === HILFE ===
.PHONY: help
help:
	@echo "Apple QML System - Development Commands"
	@echo "======================================="
	@echo ""
	@echo "Setup:"
	@echo "  install          Install package and dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  setup            Complete development setup"
	@echo ""
	@echo "Code Quality:"
	@echo "  format           Format code with black and isort"
	@echo "  lint             Run all linters"
	@echo "  type-check       Run type checking with mypy"
	@echo "  check-all        Run all code quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-fast        Run tests without slow integration tests"
	@echo "  test-cov         Run tests with coverage report"
	@echo "  test-html        Generate HTML coverage report"
	@echo ""
	@echo "Examples:"
	@echo "  example-basic    Run basic usage example"
	@echo "  example-advanced Run advanced training example"
	@echo "  examples-all     Run all examples"
	@echo ""
	@echo "Documentation:"
	@echo "  docs             Generate documentation"
	@echo "  docs-serve       Serve documentation locally"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean            Clean up generated files"
	@echo "  clean-all        Deep clean including cache"
	@echo ""
	@echo "CI/CD:"
	@echo "  ci               Run all CI checks"
	@echo "  pre-commit       Run pre-commit hooks"

# === SETUP ===
.PHONY: install
install:
	$(PIP) install -e .

.PHONY: install-dev
install-dev:
	$(PIP) install -e ".[dev]"
	@if git rev-parse --git-dir > /dev/null 2>&1; then \
		pre-commit install; \
	else \
		echo "⚠️  Git repository nicht gefunden - pre-commit übersprungen"; \
	fi

.PHONY: setup
setup: install-dev
	mkdir -p $(OUTPUT_DIR)/{models,visualizations,logs,data}
	@echo "Development environment setup complete!"

# === CODE QUALITY ===
.PHONY: format
format:
	$(BLACK) $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)
	$(ISORT) $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)

.PHONY: lint
lint:
	$(FLAKE8) $(SRC_DIR) $(TEST_DIR) $(EXAMPLES_DIR)

.PHONY: type-check
type-check:
	$(MYPY) $(SRC_DIR)

.PHONY: check-all
check-all: format lint type-check
	@echo "All code quality checks passed!"

# === TESTING ===
.PHONY: test
test:
	$(PYTEST) $(TEST_DIR) -v

.PHONY: test-fast
test-fast:
	$(PYTEST) $(TEST_DIR) -v -m "not slow"

.PHONY: test-cov
test-cov:
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=term-missing

.PHONY: test-html
test-html:
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# === EXAMPLES ===
.PHONY: example-basic
example-basic:
	cd $(EXAMPLES_DIR) && $(PYTHON) basic_usage.py

.PHONY: example-advanced
example-advanced:
	cd $(EXAMPLES_DIR) && $(PYTHON) advanced_training.py

.PHONY: examples-all
examples-all: example-basic example-advanced
	@echo "All examples completed successfully!"

# === DOKUMENTATION ===
.PHONY: docs
docs:
	cd $(DOCS_DIR) && $(PYTHON) -m sphinx -b html . _build/html

.PHONY: docs-serve
docs-serve: docs
	cd $(DOCS_DIR)/_build/html && $(PYTHON) -m http.server 8000

# === CLEANUP ===
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

.PHONY: clean-all
clean-all: clean
	rm -rf $(OUTPUT_DIR)/*
	rm -rf .tox/
	rm -rf venv/
	rm -rf .venv/
	@echo "Deep clean completed!"

# === CI/CD ===
.PHONY: ci
ci: check-all test-cov
	@echo "All CI checks passed!"

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

# === DEVELOPMENT HELPERS ===
.PHONY: jupyter
jupyter:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

.PHONY: profile
profile:
	$(PYTHON) -m cProfile -o profile.stats $(EXAMPLES_DIR)/basic_usage.py
	@echo "Profile saved to profile.stats"

.PHONY: requirements
requirements:
	$(PIP) freeze > requirements.lock

# === QUANTUM SPECIFIC ===
.PHONY: test-quantum
test-quantum:
	$(PYTEST) $(TEST_DIR) -v -k "quantum" --tb=short

.PHONY: benchmark
benchmark:
	$(PYTHON) $(EXAMPLES_DIR)/benchmark.py

# === PACKAGING ===
.PHONY: build
build: clean
	$(PYTHON) setup.py sdist bdist_wheel

.PHONY: upload-test
upload-test: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: upload
upload: build
	twine upload dist/*

# === INSTALLATION VERIFICATION ===
.PHONY: verify
verify:
	$(PYTHON) -c "import src; print('✅ Package import successful')"
	$(PYTHON) -c "from src import QuantumAppleModel; print('✅ Main classes import successful')"
	$(PYTHON) -c "import qiskit; print('✅ Qiskit available')"
	$(PYTHON) -c "import numpy, scipy, matplotlib; print('✅ Scientific stack available')"
	@echo "🎉 Installation verification complete!"

# === DEFAULT TARGET ===
.DEFAULT_GOAL := help