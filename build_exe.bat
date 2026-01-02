@echo off
REM Build script for BRP Portfolio Optimizer
REM Creates standalone .exe executable

echo.
echo ============================================================
echo   BRP PORTFOLIO OPTIMIZER - BUILD EXECUTABLE
echo ============================================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo.
echo Cleaning previous builds...
if exist dist (
    rmdir /s /q dist
)
if exist build (
    rmdir /s /q build
)
if exist *.spec (
    del *.spec
)

echo.
echo Building executable (this may take 2-5 minutes)...
echo.

REM Build with PyInstaller
pyinstaller ^
    --onefile ^
    --windowed ^
    --name="BRP_Portfolio_Optimizer" ^
    --add-data="brp_portfolio_optimizer;brp_portfolio_optimizer" ^
    --add-data="licenses.json;." ^
    --hidden-import=streamlit ^
    --hidden-import=pandas ^
    --hidden-import=numpy ^
    --hidden-import=scipy ^
    --hidden-import=matplotlib ^
    --hidden-import=quantstats ^
    --hidden-import=yfinance ^
    --hidden-import=openpyxl ^
    --hidden-import=IPython ^
    --collect-all=streamlit ^
    app.py

echo.
echo ============================================================
if exist "dist\BRP_Portfolio_Optimizer.exe" (
    echo.
    echo SUCCESS! Executable created at:
    echo.
    echo   dist\BRP_Portfolio_Optimizer.exe
    echo.
    echo To distribute:
    echo   1. Copy dist\BRP_Portfolio_Optimizer.exe
    echo   2. Copy licenses.json
    echo   3. Copy client documentation
    echo   4. Create client package folder
    echo.
    echo Size: 
    for %%A in ("dist\BRP_Portfolio_Optimizer.exe") do (
        echo   %%~zA bytes
    )
    echo.
) else (
    echo.
    echo ERROR: Build failed! Check the output above.
    echo.
)

echo ============================================================
echo.
pause
