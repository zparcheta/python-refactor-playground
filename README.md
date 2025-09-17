# Cinema Ticket Management System

A simple cinema ticket management system that serves as a playground for learning code refactoring techniques and code quality analysis.

## Project Structure

```
python-refactor-playground/
├── src/                           # Source code
│   └── cinema/                    # Main package
│       ├── __init__.py           # Package initialization
│       ├── cinema_manager.py     # Cinema management logic
│       ├── movie.py              # Movie class definition
│       └── ticket.py             # Ticket class definition
├── tests/                        # Test suite
│   ├── __init__.py              # Test package initialization
│   └── test_cinema.py           # Unit tests
├── tools/                        # Development tools
│   ├── analyze_code_quality.py  # Code quality analysis tool
│   └── auto_code_fixer_libraries_only.py # Auto code fixer
├── scripts/                      # Utility scripts (if any)
├── main.py                      # Main application entry point
├── setup.py                     # Package setup
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── ESTRUCTURA.md                # Project structure documentation
├── EXERCISE_README.md           # Exercise documentation
├── EXERCISE_SCRIPT.md           # Step-by-step guide (Linux/macOS)
├── EXERCISE_SCRIPT_WINDOWS.md   # Step-by-step guide (Windows)
├── run.bat                      # Windows batch runner
├── run.ps1                      # Windows PowerShell runner
└── setup_windows.bat            # Windows setup script
```

## Features

- **Movie Management**: Add movies with title, duration, genre, and price
- **Ticket Sales**: Sell tickets for specific movies and seats
- **Seat Management**: Track available seats (1-10 rows, 1-20 seats per row)
- **Revenue Tracking**: Monitor total revenue and ticket sales
- **Ticket Validation**: Prevent double-use of tickets
- **Refund System**: Refund unused tickets
- **Movie Reviews**: Add reviews and calculate average ratings

## Quick Start

### Windows Users
1. **Install dependencies:**
```cmd
run.bat install
```
*Or with PowerShell:*
```powershell
.\run.ps1 install
```

2. **Run the application:**
```cmd
run.bat run
```
*Or with PowerShell:*
```powershell
.\run.ps1 run
```

3. **Run tests:**
```cmd
run.bat test
```
*Or with PowerShell:*
```powershell
.\run.ps1 test
```

4. **Analyze code quality:**
```cmd
run.bat analyze
```
*Or with PowerShell:*
```powershell
.\run.ps1 analyze
```

5. **Auto-fix code issues:**
```cmd
run.bat fix
```
*Or with PowerShell:*
```powershell
.\run.ps1 fix
```

### Linux/macOS Users
1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python main.py
```

3. **Run tests:**
```bash
# Con pytest (recomendado)
pytest

# Con unittest
python -m unittest discover

# Con Makefile
make test
```

4. **Analyze code quality:**
```bash
make analyze
# o
python tools/analyze_code_quality.py
```

5. **Auto-fix code issues:**
```bash
make fix
# o
python tools/auto_code_fixer_libraries_only.py
```

## Development Setup

### Windows Users
For Windows, use the automated setup script:

```cmd
setup_windows.bat
```

Or manually install dependencies:

```cmd
pip install -e .
```

Or install with development dependencies:

```cmd
pip install -e ".[dev]"
```

### Linux/macOS Users
For development, install the package in editable mode:

```bash
pip install -e .
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Code Quality Issues (Intentional)

This project intentionally contains various code quality issues for educational purposes:

### Performance Issues
- Inefficient linear searches instead of using dictionaries/sets
- Inefficient seat management using lists instead of sets
- Inefficient ticket removal using loops instead of list comprehensions

### Code Style Issues
- Missing type annotations
- Inconsistent naming conventions
- Missing docstrings
- Long methods that could be broken down

### Logic Issues
- Incorrect rating calculation in Movie class
- Boolean comparisons using `==` instead of `is`
- Missing input validation

### Security Issues
- No input sanitization
- Potential for SQL injection (if using databases)

## Available Commands

### Windows Users

#### Using Batch Files (Command Prompt)
```cmd
run.bat help          # Show all available commands
run.bat test          # Run tests
run.bat test-coverage # Run tests with coverage
run.bat lint          # Run linting checks
run.bat format        # Format code
run.bat run           # Run the application
run.bat analyze       # Run code quality analysis
run.bat fix           # Auto-fix code issues
run.bat clean         # Clean temporary files
```

#### Using PowerShell (Recommended)
```powershell
.\run.ps1 help          # Show all available commands
.\run.ps1 test          # Run tests
.\run.ps1 test-coverage # Run tests with coverage
.\run.ps1 lint          # Run linting checks
.\run.ps1 format        # Format code
.\run.ps1 run           # Run the application
.\run.ps1 analyze       # Run code quality analysis
.\run.ps1 fix           # Auto-fix code issues
.\run.ps1 clean         # Clean temporary files
```

### Linux/macOS Users

#### Using Make (Recommended)
```bash
make help          # Show all available commands
make test          # Run tests
make test-coverage # Run tests with coverage
make lint          # Run linting checks
make format        # Format code
make run           # Run the application
make analyze       # Run code quality analysis
make fix           # Auto-fix code issues
make clean         # Clean temporary files
```

### Direct Commands (All Platforms)
- **`python main.py`** - Run the main application
- **`pytest`** - Run all tests (recommended)
- **`python -m unittest discover`** - Run tests with unittest
- **`python tools/analyze_code_quality.py`** - Run comprehensive code quality analysis
- **`python tools/auto_code_fixer_libraries_only.py`** - Run automated code fixing using libraries

## Code Quality Analysis

The quality analysis tool provides:

- **Complexity Metrics**: Cyclomatic complexity and maintainability index
- **Linting**: Ruff, Black, isort, Pylint, Flake8
- **Type Checking**: MyPy static type analysis
- **Security**: Bandit security analysis and dependency checking
- **Code Quality**: Dead code detection, duplicate code analysis
- **Performance**: Profiling with Scalene
- **Coverage**: Test coverage analysis

## Learning Objectives

This project helps you learn:

1. **Code Quality Metrics**: Understanding complexity, maintainability, and technical debt
2. **Static Analysis Tools**: Using linters, formatters, and type checkers
3. **Refactoring Techniques**: Improving code without changing functionality
4. **Testing**: Writing and running unit tests
5. **Performance Optimization**: Identifying and fixing bottlenecks
6. **Security Best Practices**: Finding and fixing security vulnerabilities
7. **Project Structure**: Organizing code in a professional manner

## Refactoring Exercises

Try these refactoring exercises:

1. **Fix the rating calculation** in `Movie.add_review()`
2. **Optimize seat management** by using sets instead of lists
3. **Add type annotations** to all methods
4. **Improve search algorithms** by using dictionaries
5. **Add input validation** and error handling
6. **Break down large methods** into smaller, focused functions
7. **Add comprehensive docstrings**
8. **Implement proper logging** instead of print statements

## Tools Used

- **Ruff**: Fast Python linter with auto-fixes
- **Black**: Code formatter
- **isort**: Import organizer
- **MyPy**: Type checker
- **Bandit**: Security linter
- **Radon**: Complexity metrics
- **Coverage**: Test coverage
- **Pylint**: Comprehensive linter
- **Flake8**: Style checker
- **autopep8**: PEP8 style fixes
- **pyupgrade**: Python syntax modernization
- **autoflake**: Code cleanup
- **vulture**: Dead code detection

## Windows-Specific Notes

### PowerShell Execution Policy
If you encounter execution policy errors with PowerShell scripts:
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### File Paths
- Windows uses backslashes (`\`) in file paths
- Use quotes around paths with spaces: `"C:\Program Files\Python\python.exe"`

### Environment Variables
- Ensure Python is in your `PATH` environment variable
- Check with: `echo %PATH%` (CMD) or `$env:PATH` (PowerShell)

### Exercise Scripts
- **Linux/macOS**: Use `EXERCISE_SCRIPT.md`
- **Windows**: Use `EXERCISE_SCRIPT_WINDOWS.md`

## Contributing

This is a learning project. Feel free to:
- Fix the intentional issues
- Add new features
- Improve the code structure
- Add more comprehensive tests
- Experiment with different refactoring techniques