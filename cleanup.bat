@echo off
REM ================================================================
REM BRP Portfolio Optimizer - Cleanup Temporary Files
REM ================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     🧹 Cleaning Temporary Files                         ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Ask for confirmation
echo This will remove:
echo   • Temporary files
echo   • Python cache
echo   • Generated reports
echo   • Log files
echo.
echo Will NOT remove:
echo   • Virtual environment (.venv)
echo   • Application code
echo   • Configuration file
echo.

set /p confirm="Continue? (y/n): "
if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo [*] Cleaning temporary files...

REM Clean temporary files
if exist "temp_*.csv" (
    del /q temp_*.csv 2>nul
    echo ✅ Temporary CSV files removed
)

if exist "temp_*.html" (
    del /q temp_*.html 2>nul
    echo ✅ Temporary HTML files removed
)

if exist "quantstats_report_*.html" (
    del /q quantstats_report_*.html 2>nul
    echo ✅ QuantStats reports removed
)

REM Clean Python cache
if exist "__pycache__" (
    rmdir /s /q __pycache__ 2>nul
    echo ✅ Python cache (__pycache__) removed
)

REM Clean Streamlit cache
if exist ".streamlit" (
    rmdir /s /q .streamlit 2>nul
    echo ✅ Streamlit cache removed
)

REM Clean logs
if exist "*.log" (
    del /q *.log 2>nul
    echo ✅ Log files removed
)

REM Clean cache in subdirectories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     ✅ Cleanup Complete!                                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
