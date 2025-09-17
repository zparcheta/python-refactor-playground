# Cinema Ticket Management System - PowerShell Runner
# ==================================================

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [switch]$Help
)

# Colors
$Colors = @{
    Blue = "Cyan"
    Green = "Green"
    Yellow = "Yellow"
    Red = "Red"
    Reset = "White"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-ColorOutput "Cinema Ticket Management System" $Colors.Blue
    Write-ColorOutput "===============================" $Colors.Blue
    Write-Host ""
    Write-ColorOutput "Available commands:" $Colors.Green
    Write-Host ""
    
    $commands = @(
        @{Name="help"; Description="Show this help message"},
        @{Name="install"; Description="Install basic dependencies"},
        @{Name="install-dev"; Description="Install with development dependencies"},
        @{Name="setup"; Description="Setup complete development environment"},
        @{Name="test"; Description="Run tests with pytest"},
        @{Name="test-verbose"; Description="Run tests with verbose output"},
        @{Name="test-coverage"; Description="Run tests with coverage report"},
        @{Name="test-unittest"; Description="Run tests with unittest"},
        @{Name="lint"; Description="Run all linting checks"},
        @{Name="format"; Description="Format code with black and isort"},
        @{Name="check"; Description="Run all checks (lint + test)"},
        @{Name="analyze"; Description="Run comprehensive code quality analysis"},
        @{Name="fix"; Description="Auto-fix code issues using libraries"},
        @{Name="security"; Description="Run security analysis"},
        @{Name="run"; Description="Run the main application"},
        @{Name="clean"; Description="Clean temporary files and build artifacts"},
        @{Name="benchmark-initial"; Description="Record initial benchmark"},
        @{Name="benchmark-post-autofix"; Description="Record post-autofix benchmark"},
        @{Name="benchmark-post-ai"; Description="Record post-AI benchmark"},
        @{Name="benchmark-compare"; Description="Compare all benchmark stages"},
        @{Name="benchmark-report"; Description="Generate comprehensive benchmark report"},
        @{Name="quick-test"; Description="Quick test run"},
        @{Name="quick-lint"; Description="Quick lint check"}
    )
    
    foreach ($cmd in $commands) {
        Write-ColorOutput ("  {0,-20}" -f $cmd.Name) $Colors.Blue -NoNewline
        Write-ColorOutput $cmd.Description $Colors.Reset
    }
    
    Write-Host ""
    Write-ColorOutput "Quick start:" $Colors.Yellow
    Write-ColorOutput "  .\run.ps1 setup     # Setup development environment" $Colors.Reset
    Write-ColorOutput "  .\run.ps1 test      # Run tests" $Colors.Reset
    Write-ColorOutput "  .\run.ps1 run       # Run the application" $Colors.Reset
    Write-Host ""
}

function Test-PythonInstalled {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python not found"
        }
        return $true
    }
    catch {
        Write-ColorOutput "Error: Python is not installed or not in PATH" $Colors.Red
        Write-ColorOutput "Please install Python 3.9+ from https://python.org" $Colors.Reset
        exit 1
    }
}

function Invoke-Install {
    Write-ColorOutput "Installing dependencies..." $Colors.Green
    pip install -r requirements.txt
    pip install -e .
}

function Invoke-InstallDev {
    Write-ColorOutput "Installing development dependencies..." $Colors.Green
    pip install -e ".[dev]"
    pip install -r requirements.txt
}

function Invoke-Setup {
    Invoke-InstallDev
    Write-ColorOutput "Setting up development environment..." $Colors.Green
    Write-ColorOutput "✓ Dependencies installed" $Colors.Green
    Write-ColorOutput "✓ Package installed in development mode" $Colors.Green
    Write-Host ""
    Write-ColorOutput "Development environment ready!" $Colors.Blue
    Write-ColorOutput "Run '.\run.ps1 help' to see available commands" $Colors.Yellow
}

function Invoke-Test {
    Write-ColorOutput "Running tests..." $Colors.Green
    pytest
}

function Invoke-TestVerbose {
    Write-ColorOutput "Running tests with verbose output..." $Colors.Green
    pytest -v
}

function Invoke-TestCoverage {
    Write-ColorOutput "Running tests with coverage..." $Colors.Green
    pytest --cov=src --cov-report=html --cov-report=term --cov-report=xml
}

function Invoke-TestUnittest {
    Write-ColorOutput "Running tests with unittest..." $Colors.Green
    python -m unittest discover -v
}

function Invoke-Lint {
    Write-ColorOutput "Running linting checks..." $Colors.Green
    Write-ColorOutput "Checking with ruff..." $Colors.Yellow
    ruff check .
    Write-ColorOutput "Checking with black..." $Colors.Yellow
    black --check .
    Write-ColorOutput "Checking with isort..." $Colors.Yellow
    isort --check-only .
    Write-ColorOutput "Checking with mypy..." $Colors.Yellow
    mypy src/ tests/ main.py --ignore-missing-imports
    Write-ColorOutput "✓ All linting checks passed" $Colors.Green
}

function Invoke-Format {
    Write-ColorOutput "Formatting code..." $Colors.Green
    Write-ColorOutput "Formatting with black..." $Colors.Yellow
    black .
    Write-ColorOutput "Organizing imports with isort..." $Colors.Yellow
    isort .
    Write-ColorOutput "✓ Code formatted" $Colors.Green
}

function Invoke-Check {
    Invoke-Lint
    Invoke-Test
    Write-ColorOutput "✓ All checks passed" $Colors.Green
}

function Invoke-Analyze {
    Write-ColorOutput "Running code quality analysis..." $Colors.Green
    python tools/analyze_code_quality.py
}

function Invoke-Fix {
    Write-ColorOutput "Auto-fixing code issues..." $Colors.Green
    python tools/auto_code_fixer_libraries_only.py
}

function Invoke-Security {
    Write-ColorOutput "Running security analysis..." $Colors.Green
    Write-ColorOutput "Checking with bandit..." $Colors.Yellow
    bandit -r src/ tests/ main.py
    Write-ColorOutput "Checking dependencies with safety..." $Colors.Yellow
    safety check
    Write-ColorOutput "Auditing packages with pip-audit..." $Colors.Yellow
    pip-audit
}

function Invoke-Run {
    Write-ColorOutput "Running Cinema Ticket Management System..." $Colors.Green
    python main.py
}

function Invoke-Clean {
    Write-ColorOutput "Cleaning temporary files..." $Colors.Green
    
    # Remove __pycache__ directories
    Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
        Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    # Remove .pyc files
    Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
    
    # Remove .egg-info directories
    Get-ChildItem -Path . -Recurse -Directory -Filter "*.egg-info" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Remove other directories
    $dirsToRemove = @("build", "dist", "htmlcov", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".venv", "venv")
    foreach ($dir in $dirsToRemove) {
        if (Test-Path $dir) {
            Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
    
    # Remove files
    $filesToRemove = @(".coverage", "bandit_report.json", "coverage.xml")
    foreach ($file in $filesToRemove) {
        if (Test-Path $file) {
            Remove-Item -Path $file -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-ColorOutput "✓ Cleanup completed" $Colors.Green
}

function Invoke-BenchmarkInitial {
    Write-ColorOutput "Recording initial benchmark..." $Colors.Green
    python tools/benchmark_code_quality.py --stage initial --description "Initial code quality state"
}

function Invoke-BenchmarkPostAutofix {
    Write-ColorOutput "Recording post-autofix benchmark..." $Colors.Green
    python tools/benchmark_code_quality.py --stage post-autofix --description "After running automated fixes"
}

function Invoke-BenchmarkPostAI {
    Write-ColorOutput "Recording post-AI benchmark..." $Colors.Green
    python tools/benchmark_code_quality.py --stage post-ai --description "After AI agent improvements"
}

function Invoke-BenchmarkCompare {
    Write-ColorOutput "Comparing benchmark stages..." $Colors.Green
    python tools/benchmark_code_quality.py --compare --table
}

function Invoke-BenchmarkReport {
    Write-ColorOutput "Generating benchmark report..." $Colors.Green
    python tools/benchmark_code_quality.py --report
}

function Invoke-QuickTest {
    pytest -x
}

function Invoke-QuickLint {
    ruff check src/ tests/ main.py
}

# Main execution
if ($Help) {
    Show-Help
    exit 0
}

# Check Python installation
Test-PythonInstalled

# Route commands
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Invoke-Install }
    "install-dev" { Invoke-InstallDev }
    "setup" { Invoke-Setup }
    "test" { Invoke-Test }
    "test-verbose" { Invoke-TestVerbose }
    "test-coverage" { Invoke-TestCoverage }
    "test-unittest" { Invoke-TestUnittest }
    "lint" { Invoke-Lint }
    "format" { Invoke-Format }
    "check" { Invoke-Check }
    "analyze" { Invoke-Analyze }
    "fix" { Invoke-Fix }
    "security" { Invoke-Security }
    "run" { Invoke-Run }
    "clean" { Invoke-Clean }
    "benchmark-initial" { Invoke-BenchmarkInitial }
    "benchmark-post-autofix" { Invoke-BenchmarkPostAutofix }
    "benchmark-post-ai" { Invoke-BenchmarkPostAI }
    "benchmark-compare" { Invoke-BenchmarkCompare }
    "benchmark-report" { Invoke-BenchmarkReport }
    "quick-test" { Invoke-QuickTest }
    "quick-lint" { Invoke-QuickLint }
    default {
        Write-ColorOutput "Unknown command: $Command" $Colors.Red
        Show-Help
        exit 1
    }
}
