@echo off
REM ================================================================
REM BRP Portfolio Optimizer - Application Executor (Windows)
REM ================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     📊 BRP Portfolio Optimizer                           ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if venv exists
if not exist ".venv" (
    echo ❌ ERROR: Virtual environment not found!
    echo.
    echo Please run first:
    echo    1. Double-click: install.bat
    echo.
    pause
    exit /b 1
)

REM Activate venv
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Failed to activate environment
    pause
    exit /b 1
)

REM Check if streamlit is installed
echo [*] Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Streamlit not found, reinstalling...
    pip install streamlit >nul 2>&1
)

echo ✅ System ready!
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║     🚀 Starting application...                           ║
echo ║                                                            ║
echo ║     ✅ Access: http://localhost:8501                      ║
echo ║                                                            ║
echo ║     To exit: Close this window or press CTRL+C            ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Start Streamlit
streamlit run app.py

pause
        echo [ERRO] Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
)

REM Verificar se Streamlit está instalado
"%PYTHON_EXE%" -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Instalando dependências (primeira execução)...
    "%PYTHON_EXE%" -m pip install --upgrade pip -q
    if !errorlevel! neq 0 (
        echo [ERRO] Falha ao atualizar pip
        pause
        exit /b 1
    )
    "%PYTHON_EXE%" -m pip install -r requirements.txt -q
    if !errorlevel! neq 0 (
        echo [ERRO] Falha ao instalar dependências
        pause
        exit /b 1
    )
)

REM Executar aplicacao
echo.
echo [SUCESSO] Iniciando BRP Portfolio Optimizer...
echo.
echo A aplicacao abriu em: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

"%STREAMLIT_EXE%" run app.py

pause
