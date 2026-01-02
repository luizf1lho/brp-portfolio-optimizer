#!/bin/bash

# Script de inicializacao do BRP Portfolio Optimizer (MacOS/Linux)

echo ""
echo "========================================"
echo "   BRP Portfolio Optimizer v1.0"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python nao foi encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Nao foi possivel criar o ambiente virtual"
        exit 1
    fi
fi

# Ativar ambiente virtual
echo "[INFO] Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "[INFO] Verificando dependências..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERRO] Erro ao instalar dependências"
    exit 1
fi

# Executar aplicacao
echo ""
echo "[SUCESSO] Iniciando BRP Portfolio Optimizer..."
echo ""
echo "A aplicacao abriu em: http://localhost:8501"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

streamlit run app.py
