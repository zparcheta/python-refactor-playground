# Cinema Ticket Management System - Makefile
# ============================================

.PHONY: help install install-dev test test-verbose test-coverage test-unittest lint format run analyze fix clean setup check security docs build dist

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Cinema Ticket Management System$(RESET)"
	@echo "$(BLUE)===============================$(RESET)"
	@echo ""
	@echo "$(GREEN)Available commands:$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BLUE)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Quick start:$(RESET)"
	@echo "  make setup     # Setup development environment"
	@echo "  make test      # Run tests"
	@echo "  make run       # Run the application"

# Installation
install: ## Install basic dependencies
	@echo "$(GREEN)Installing dependencies...$(RESET)"
	pip install -r requirements.txt
	pip install -e .

install-dev: ## Install with development dependencies
	@echo "$(GREEN)Installing development dependencies...$(RESET)"
	pip install -e ".[dev]"
	pip install -r requirements.txt

setup: install-dev ## Setup complete development environment
	@echo "$(GREEN)Setting up development environment...$(RESET)"
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"
	@echo "$(GREEN)✓ Package installed in development mode$(RESET)"
	@echo ""
	@echo "$(BLUE)Development environment ready!$(RESET)"
	@echo "$(YELLOW)Run 'make help' to see available commands$(RESET)"

# Testing
test: ## Run tests with pytest
	@echo "$(GREEN)Running tests...$(RESET)"
	pytest

test-verbose: ## Run tests with verbose output
	@echo "$(GREEN)Running tests with verbose output...$(RESET)"
	pytest -v

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(RESET)"
	pytest --cov=src --cov-report=html --cov-report=term --cov-report=xml

test-unittest: ## Run tests with unittest
	@echo "$(GREEN)Running tests with unittest...$(RESET)"
	python -m unittest discover -v

# Code Quality
lint: ## Run all linting checks
	@echo "$(GREEN)Running linting checks...$(RESET)"
	@echo "$(YELLOW)Checking with ruff...$(RESET)"
	ruff check .
	@echo "$(YELLOW)Checking with black...$(RESET)"
	black --check .
	@echo "$(YELLOW)Checking with isort...$(RESET)"
	isort --check-only .
	@echo "$(YELLOW)Checking with mypy...$(RESET)"
	mypy src/ tests/ main.py --ignore-missing-imports
	@echo "$(GREEN)✓ All linting checks passed$(RESET)"

format: ## Format code with black and isort
	@echo "$(GREEN)Formatting code...$(RESET)"
	@echo "$(YELLOW)Formatting with black...$(RESET)"
	black .
	@echo "$(YELLOW)Organizing imports with isort...$(RESET)"
	isort .
	@echo "$(GREEN)✓ Code formatted$(RESET)"

check: lint test ## Run all checks (lint + test)
	@echo "$(GREEN)✓ All checks passed$(RESET)"

# Code Analysis and Fixing
analyze: ## Run comprehensive code quality analysis
	@echo "$(GREEN)Running code quality analysis...$(RESET)"
	python tools/analyze_code_quality.py

fix: ## Auto-fix code issues using libraries
	@echo "$(GREEN)Auto-fixing code issues...$(RESET)"
	python tools/auto_code_fixer_libraries_only.py

# Security
security: ## Run security analysis
	@echo "$(GREEN)Running security analysis...$(RESET)"
	@echo "$(YELLOW)Checking with bandit...$(RESET)"
	bandit -r src/ tests/ main.py
	@echo "$(YELLOW)Checking dependencies with safety...$(RESET)"
	safety check
	@echo "$(YELLOW)Auditing packages with pip-audit...$(RESET)"
	pip-audit

# Application
run: ## Run the main application
	@echo "$(GREEN)Running Cinema Ticket Management System...$(RESET)"
	python main.py

# Documentation
docs: ## Generate documentation
	@echo "$(GREEN)Generating documentation...$(RESET)"
	@echo "$(YELLOW)Documentation generation not implemented yet$(RESET)"

# Build and Distribution
build: clean ## Build the package
	@echo "$(GREEN)Building package...$(RESET)"
	python -m build

dist: build ## Create distribution packages
	@echo "$(GREEN)Distribution packages created in dist/$(RESET)"

# Cleanup
clean: ## Clean temporary files and build artifacts
	@echo "$(GREEN)Cleaning temporary files...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf .tox/
	rm -rf .venv/
	rm -rf venv/
	rm -f bandit_report.json
	rm -f coverage.xml
	@echo "$(GREEN)✓ Cleanup completed$(RESET)"

# Development workflow
dev-setup: setup ## Complete development setup
	@echo "$(GREEN)Development setup completed!$(RESET)"
	@echo "$(BLUE)Next steps:$(RESET)"
	@echo "  1. make test      # Run tests"
	@echo "  2. make lint      # Check code quality"
	@echo "  3. make run       # Run the application"

# Benchmarking
benchmark-initial: ## Record initial benchmark
	@echo "$(GREEN)Recording initial benchmark...$(RESET)"
	python tools/benchmark_code_quality.py --stage initial --description "Initial code quality state"

benchmark-post-autofix: ## Record post-autofix benchmark
	@echo "$(GREEN)Recording post-autofix benchmark...$(RESET)"
	python tools/benchmark_code_quality.py --stage post-autofix --description "After running automated fixes"

benchmark-post-ai: ## Record post-AI benchmark
	@echo "$(GREEN)Recording post-AI benchmark...$(RESET)"
	python tools/benchmark_code_quality.py --stage post-ai --description "After AI agent improvements"

benchmark-compare: ## Compare all benchmark stages
	@echo "$(GREEN)Comparing benchmark stages...$(RESET)"
	python tools/benchmark_code_quality.py --compare --table

benchmark-report: ## Generate comprehensive benchmark report
	@echo "$(GREEN)Generating benchmark report...$(RESET)"
	python tools/benchmark_code_quality.py --report

benchmark-full: benchmark-initial benchmark-post-autofix benchmark-post-ai benchmark-compare ## Run complete benchmark workflow
	@echo "$(GREEN)Complete benchmark workflow finished!$(RESET)"

# CI/CD helpers
ci-test: test-coverage lint security ## Run all CI checks
	@echo "$(GREEN)✓ All CI checks passed$(RESET)"

# Quick development commands
quick-test: ## Quick test run
	pytest -x

quick-lint: ## Quick lint check
	ruff check src/ tests/ main.py

# Performance
profile: ## Run performance profiling
	@echo "$(GREEN)Running performance profiling...$(RESET)"
	scalene main.py

# Dependencies
deps-update: ## Update dependencies
	@echo "$(GREEN)Updating dependencies...$(RESET)"
	pip install --upgrade -r requirements.txt

deps-check: ## Check for outdated dependencies
	@echo "$(GREEN)Checking for outdated dependencies...$(RESET)"
	pip list --outdated
