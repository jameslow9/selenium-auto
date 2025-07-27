# AQX Trading Platform - Test Automation Makefile
# Simplifies common development and testing tasks

.PHONY: help install test smoke critical trading clean setup dashboard lint format

# Default target
help:
	@echo "🚀 AQX Trading Platform - Test Automation"
	@echo "============================================"
	@echo ""
	@echo "Available commands:"
	@echo "  setup     - Install dependencies and setup environment"
	@echo "  test      - Run all tests"
	@echo "  smoke     - Run smoke tests"
	@echo "  critical  - Run critical tests"
	@echo "  trading   - Run trading tests"
	@echo "  view      - Run view tests"
	@echo "  bulk      - Run bulk operation tests"
	@echo "  parallel  - Run tests in parallel"
	@echo "  headless  - Run tests in headless mode"
	@echo "  dashboard - Generate test dashboard"
	@echo "  clean     - Clean up generated files"
	@echo "  lint      - Run code linting"
	@echo "  format    - Format code"
	@echo "  install   - Install Python dependencies"
	@echo ""
	@echo "Examples:"
	@echo "  make smoke"
	@echo "  make test"
	@echo "  make parallel"

# Environment setup
setup: install
	@echo "🔧 Setting up test environment..."
	@mkdir -p screenshots reports logs test_data scripts
	@echo "✅ Environment setup complete"

install:
	@echo "📦 Installing dependencies..."
	@pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Test execution targets
test:
	@echo "🧪 Running all tests..."
	@python run_tests.py --type all

smoke:
	@echo "💨 Running smoke tests..."
	@python run_tests.py --type smoke

critical:
	@echo "🔥 Running critical tests..."
	@python run_tests.py --type critical

trading:
	@echo "💰 Running trading tests..."
	@python run_tests.py --type trading

view:
	@echo "👁️  Running view tests..."
	@python run_tests.py --type view

bulk:
	@echo "📦 Running bulk operation tests..."
	@python run_tests.py --type bulk

regression:
	@echo "🔄 Running regression tests..."
	@python run_tests.py --type regression

# Advanced test execution
parallel:
	@echo "⚡ Running tests in parallel..."
	@python run_tests.py --type all --parallel

headless:
	@echo "👤 Running tests in headless mode..."
	@python run_tests.py --type all --headless

fast: headless parallel
	@echo "🚀 Running fast tests (headless + parallel)..."

# Specific test combinations
smoke-headless:
	@python run_tests.py --type smoke --headless

critical-parallel:
	@python run_tests.py --type critical --parallel

# Report generation
dashboard:
	@echo "📊 Generating test dashboard..."
	@python scripts/generate_dashboard.py
	@echo "✅ Dashboard generated at reports/test_dashboard.html"

reports: dashboard
	@echo "📋 All reports generated"

# Development tools
lint:
	@echo "🔍 Running code linting..."
	@python -m flake8 tests/ scripts/ --max-line-length=100 --ignore=E501,W503 || true
	@python -m pylint tests/ scripts/ --disable=all --enable=E,W,C --max-line-length=100 || true

format:
	@echo "🎨 Formatting code..."
	@python -m black tests/ scripts/ --line-length=100 || true
	@python -m isort tests/ scripts/ || true

check: lint
	@echo "✅ Code quality check complete"

# Cleanup
clean:
	@echo "🧹 Cleaning up generated files..."
	@rm -rf screenshots/* reports/* logs/* __pycache__ .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

deep-clean: clean
	@echo "🧹 Deep cleaning..."
	@rm -rf .tox/ .coverage htmlcov/ .pytest_cache/
	@echo "✅ Deep cleanup complete"

# Test data management
test-data:
	@echo "📝 Setting up test data..."
	@mkdir -p test_data
	@echo '{"test_accounts": [{"id": "998995", "password": "u#TuWNf2J2p$"}]}' > test_data/accounts.json
	@echo "✅ Test data setup complete"

# Docker support (future enhancement)
docker-build:
	@echo "🐳 Building Docker image..."
	@docker build -t aqx-selenium-tests .

docker-run:
	@echo "🐳 Running tests in Docker..."
	@docker run --rm -v $(PWD)/reports:/app/reports aqx-selenium-tests

# CI/CD helpers
ci-install:
	@pip install -r requirements.txt
	@pip install pytest-xdist pytest-html

ci-test:
	@python run_tests.py --type all --headless --parallel

ci-reports: dashboard
	@echo "📊 CI reports generated"

# Debugging helpers
debug:
	@echo "🐛 Running tests in debug mode..."
	@python run_tests.py --type smoke -v

debug-single:
	@echo "🐛 Running single test for debugging..."
	@pytest tests/test_aqx_platform.py::TestAQXLoginFunctionality::test_login_page_loads -v -s

list-tests:
	@echo "📋 Available tests:"
	@python run_tests.py --list

# Performance testing
perf:
	@echo "⚡ Running performance tests..."
	@time python run_tests.py --type all --parallel

# Security checks (future enhancement)
security:
	@echo "🔒 Running security checks..."
	@python -m bandit -r tests/ scripts/ || true

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation available in README.md"

# Development workflow helpers
dev-setup: setup test-data
	@echo "👨‍💻 Development environment ready"

quick-test: smoke
	@echo "⚡ Quick test complete"

full-test: test dashboard
	@echo "🎯 Full test suite complete"

# Git hooks simulation
pre-commit: lint test
	@echo "✅ Pre-commit checks passed"

pre-push: test dashboard
	@echo "✅ Pre-push checks passed"

# Monitoring
status:
	@echo "📊 Test automation status:"
	@echo "Last run: $(shell ls -la reports/ | head -2 | tail -1 | awk '{print $$6" "$$7" "$$8}')"
	@echo "Reports: $(shell ls reports/*.html 2>/dev/null | wc -l) HTML files"
	@echo "Screenshots: $(shell ls screenshots/*.png 2>/dev/null | wc -l) PNG files"

# All-in-one targets
all: install test dashboard
	@echo "🎉 Complete test automation cycle finished"

watch:
	@echo "👀 Watching for file changes..."
	@echo "Run 'make test' when files change"
	@# This would require a file watcher tool like inotify

# Version info
version:
	@echo "📍 Version Information:"
	@python --version
	@pip show selenium | grep Version || echo "Selenium: Not installed"
	@pip show pytest | grep Version || echo "Pytest: Not installed"