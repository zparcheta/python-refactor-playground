@echo off
REM Cinema Ticket Management System - Windows Batch Runner
REM =====================================================

setlocal enabledelayedexpansion

REM Colors (Windows 10+)
set "BLUE=[36m"
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "RESET=[0m"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%Error: Python is not installed or not in PATH%RESET%
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

REM Default command
if "%1"=="" (
    call :show_help
    exit /b 0
)

REM Route commands
if "%1"=="help" goto :show_help
if "%1"=="install" goto :install
if "%1"=="install-dev" goto :install_dev
if "%1"=="setup" goto :setup
if "%1"=="test" goto :test
if "%1"=="test-verbose" goto :test_verbose
if "%1"=="test-coverage" goto :test_coverage
if "%1"=="test-unittest" goto :test_unittest
if "%1"=="lint" goto :lint
if "%1"=="format" goto :format
if "%1"=="check" goto :check
if "%1"=="analyze" goto :analyze
if "%1"=="fix" goto :fix
if "%1"=="security" goto :security
if "%1"=="run" goto :run
if "%1"=="clean" goto :clean
if "%1"=="benchmark-initial" goto :benchmark_initial
if "%1"=="benchmark-post-autofix" goto :benchmark_post_autofix
if "%1"=="benchmark-post-ai" goto :benchmark_post_ai
if "%1"=="benchmark-compare" goto :benchmark_compare
if "%1"=="benchmark-report" goto :benchmark_report
if "%1"=="quick-test" goto :quick_test
if "%1"=="quick-lint" goto :quick_lint

echo %RED%Unknown command: %1%RESET%
call :show_help
exit /b 1

:show_help
echo %BLUE%Cinema Ticket Management System%RESET%
echo %BLUE%===============================%RESET%
echo.
echo %GREEN%Available commands:%RESET%
echo.
echo %BLUE%  help%RESET%          Show this help message
echo %BLUE%  install%RESET%       Install basic dependencies
echo %BLUE%  install-dev%RESET%   Install with development dependencies
echo %BLUE%  setup%RESET%         Setup complete development environment
echo %BLUE%  test%RESET%          Run tests with pytest
echo %BLUE%  test-verbose%RESET%  Run tests with verbose output
echo %BLUE%  test-coverage%RESET% Run tests with coverage report
echo %BLUE%  test-unittest%RESET% Run tests with unittest
echo %BLUE%  lint%RESET%          Run all linting checks
echo %BLUE%  format%RESET%        Format code with black and isort
echo %BLUE%  check%RESET%         Run all checks (lint + test)
echo %BLUE%  analyze%RESET%       Run comprehensive code quality analysis
echo %BLUE%  fix%RESET%           Auto-fix code issues using libraries
echo %BLUE%  security%RESET%       Run security analysis
echo %BLUE%  run%RESET%           Run the main application
echo %BLUE%  clean%RESET%          Clean temporary files and build artifacts
echo %BLUE%  benchmark-initial%RESET% Record initial benchmark
echo %BLUE%  benchmark-post-autofix%RESET% Record post-autofix benchmark
echo %BLUE%  benchmark-post-ai%RESET% Record post-AI benchmark
echo %BLUE%  benchmark-compare%RESET% Compare all benchmark stages
echo %BLUE%  benchmark-report%RESET% Generate comprehensive benchmark report
echo %BLUE%  quick-test%RESET%    Quick test run
echo %BLUE%  quick-lint%RESET%    Quick lint check
echo.
echo %YELLOW%Quick start:%RESET%
echo   run.bat setup     # Setup development environment
echo   run.bat test      # Run tests
echo   run.bat run       # Run the application
echo.
goto :eof

:install
echo %GREEN%Installing dependencies...%RESET%
pip install -r requirements.txt
pip install -e .
goto :eof

:install_dev
echo %GREEN%Installing development dependencies...%RESET%
pip install -e ".[dev]"
pip install -r requirements.txt
goto :eof

:setup
call :install_dev
echo %GREEN%Setting up development environment...%RESET%
echo %GREEN%✓ Dependencies installed%RESET%
echo %GREEN%✓ Package installed in development mode%RESET%
echo.
echo %BLUE%Development environment ready!%RESET%
echo %YELLOW%Run 'run.bat help' to see available commands%RESET%
goto :eof

:test
echo %GREEN%Running tests...%RESET%
pytest
goto :eof

:test_verbose
echo %GREEN%Running tests with verbose output...%RESET%
pytest -v
goto :eof

:test_coverage
echo %GREEN%Running tests with coverage...%RESET%
pytest --cov=src --cov-report=html --cov-report=term --cov-report=xml
goto :eof

:test_unittest
echo %GREEN%Running tests with unittest...%RESET%
python -m unittest discover -v
goto :eof

:lint
echo %GREEN%Running linting checks...%RESET%
echo %YELLOW%Checking with ruff...%RESET%
ruff check .
echo %YELLOW%Checking with black...%RESET%
black --check .
echo %YELLOW%Checking with isort...%RESET%
isort --check-only .
echo %YELLOW%Checking with mypy...%RESET%
mypy src/ tests/ main.py --ignore-missing-imports
echo %GREEN%✓ All linting checks passed%RESET%
goto :eof

:format
echo %GREEN%Formatting code...%RESET%
echo %YELLOW%Formatting with black...%RESET%
black .
echo %YELLOW%Organizing imports with isort...%RESET%
isort .
echo %GREEN%✓ Code formatted%RESET%
goto :eof

:check
call :lint
call :test
echo %GREEN%✓ All checks passed%RESET%
goto :eof

:analyze
echo %GREEN%Running code quality analysis...%RESET%
python tools/analyze_code_quality.py
goto :eof

:fix
echo %GREEN%Auto-fixing code issues...%RESET%
python tools/auto_code_fixer_libraries_only.py
goto :eof

:security
echo %GREEN%Running security analysis...%RESET%
echo %YELLOW%Checking with bandit...%RESET%
bandit -r src/ tests/ main.py
echo %YELLOW%Checking dependencies with safety...%RESET%
safety check
echo %YELLOW%Auditing packages with pip-audit...%RESET%
pip-audit
goto :eof

:run
echo %GREEN%Running Cinema Ticket Management System...%RESET%
python main.py
goto :eof

:clean
echo %GREEN%Cleaning temporary files...%RESET%
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f"
for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist .coverage del /q .coverage
if exist htmlcov rd /s /q htmlcov
if exist .pytest_cache rd /s /q .pytest_cache
if exist .mypy_cache rd /s /q .mypy_cache
if exist .ruff_cache rd /s /q .ruff_cache
if exist .tox rd /s /q .tox
if exist .venv rd /s /q .venv
if exist venv rd /s /q venv
if exist bandit_report.json del /q bandit_report.json
if exist coverage.xml del /q coverage.xml
echo %GREEN%✓ Cleanup completed%RESET%
goto :eof

:benchmark_initial
echo %GREEN%Recording initial benchmark...%RESET%
python tools/benchmark_code_quality.py --stage initial --description "Initial code quality state"
goto :eof

:benchmark_post_autofix
echo %GREEN%Recording post-autofix benchmark...%RESET%
python tools/benchmark_code_quality.py --stage post-autofix --description "After running automated fixes"
goto :eof

:benchmark_post_ai
echo %GREEN%Recording post-AI benchmark...%RESET%
python tools/benchmark_code_quality.py --stage post-ai --description "After AI agent improvements"
goto :eof

:benchmark_compare
echo %GREEN%Comparing benchmark stages...%RESET%
python tools/benchmark_code_quality.py --compare --table
goto :eof

:benchmark_report
echo %GREEN%Generating benchmark report...%RESET%
python tools/benchmark_code_quality.py --report
goto :eof

:quick_test
pytest -x
goto :eof

:quick_lint
ruff check src/ tests/ main.py
goto :eof
