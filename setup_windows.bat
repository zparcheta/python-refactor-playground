@echo off
REM Windows Setup Script for Cinema Ticket Management System
REM =======================================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Cinema Ticket Management System
echo Windows Setup Script
echo ========================================
echo.

REM Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
) else (
    echo ✓ Python is installed
    python --version
)

REM Check if pip is available
echo.
echo [2/4] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
) else (
    echo ✓ pip is available
)

REM Install dependencies
echo.
echo [3/4] Installing dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install package in development mode
    pause
    exit /b 1
)

echo ✓ Dependencies installed successfully

REM Test installation
echo.
echo [4/4] Testing installation...
python -c "import src.cinema; print('✓ Package imports correctly')" 2>nul
if errorlevel 1 (
    echo WARNING: Package import test failed, but installation may still work
) else (
    echo ✓ Package imports correctly
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo   1. Run the application: run.bat run
echo   2. Run tests: run.bat test
echo   3. See all commands: run.bat help
echo.
echo For the exercise, use: EXERCISE_SCRIPT_WINDOWS.md
echo.
pause
