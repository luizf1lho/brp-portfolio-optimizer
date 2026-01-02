@echo off
REM Script corrigido para executar BRP Portfolio Optimizer

echo.
echo ========================================
echo   BRP Portfolio Optimizer v1.0
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao ativar ambiente virtual
    pause
    exit /b 1
)

REM Instalar dependências se necessário
echo [INFO] Verificando dependências...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Instalando dependências (primeira execução)...
    pip install -q -r requirements.txt
    if %errorlevel% neq 0 (
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

streamlit run app.py

pause
