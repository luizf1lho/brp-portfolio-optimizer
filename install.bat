@echo off
REM ================================================================
REM BRP Portfolio Optimizer - Automatic Installer (Windows)
REM ================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     📊 BRP Portfolio Optimizer - INSTALLER               ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if exist ".venv" (
    echo ⚠️  Virtual environment already exists, removing previous version...
    rmdir /s /q .venv >nul 2>&1
)

python -m venv .venv
if errorlevel 1 (
    echo ❌ ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Environment activated
echo.

REM Update pip
echo [4/4] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     ✅ INSTALLATION COMPLETED SUCCESSFULLY!              ║
echo ║                                                            ║
echo ║     Next step:                                            ║
echo ║     1. Double-click: run.bat                             ║
echo ║     2. Your browser will open http://localhost:8501      ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
