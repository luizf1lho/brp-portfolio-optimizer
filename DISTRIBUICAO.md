# 📦 Preparação para GitHub e Distribuição

Este documento descreve como preparar o projeto para GitHub e para distribuição a clientes.

## 🌐 Para GitHub

### ✅ Checklist Pré-Commit

```bash
# 1. Verificar .gitignore
git status --ignored

# 2. Remover arquivos desnecessários
python cleanup.bat  # Windows
rm -rf __pycache__ .streamlit *.log temp_*  # Linux/Mac

# 3. Atualizar CHANGELOG
# (descrever novos recursos, bugfixes)

# 4. Testar documentação
# Abrir README.md e verificar links

# 5. Commit final
git add .
git commit -m "Release v1.0.0 - Portfolio Optimizer"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main --tags
```

### 📋 Estrutura do Repositório

```
brp-portfolio-optimizer/
├── .github/
│   └── workflows/
│       └── tests.yml           # CI/CD (optional)
├── brp_portfolio_optimizer/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── data_processor.py
│   │   ├── optimizer.py
│   │   ├── metrics.py
│   │   ├── reports.py
│   │   └── settings.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_optimizer.py
├── app.py
├── requirements.txt
├── .gitignore
├── README.md                   # Documentação principal
├── README_GITHUB.md            # Documentação GitHub
├── CHANGELOG.md                # Histórico de versões
├── LICENSE                     # MIT ou sua licença
├── CONTRIBUTING.md             # Guia de contribuição
├── CODE_OF_CONDUCT.md          # (optional)
├── install.bat                 # Instalação Windows
├── run.bat                     # Execução Windows
├── run.sh                      # Execução Linux/Mac
├── cleanup.bat                 # Limpeza Windows
└── README_CLIENTE.txt          # Instruções clientes
```

### 📄 Arquivos Adicionais Recomendados para GitHub

1. **CHANGELOG.md** - Histórico de versões
2. **CONTRIBUTING.md** - Como contribuir
3. **CODE_OF_CONDUCT.md** - Código de conduta
4. **.github/workflows/tests.yml** - CI/CD (opcional)

---

## 📦 Para Clientes Não-Técnicos

### 🎁 Preparar Distribuição

```bash
# 1. Limpar projeto
python cleanup.bat

# 2. Remover ambiente virtual (para reduzir tamanho)
rmdir /s /q .venv  # Windows
rm -rf .venv       # Linux/Mac

# 3. Criar ZIP comprimido
# Windows: Clique direito > Enviar para > Pasta comprimida
# Ou use 7-Zip/WinRAR para melhor compressão

# 4. Tamanho esperado após compressão: ~50-100 MB
```

### 📋 Arquivos Essenciais para Cliente

```
Seu_Projeto.zip
├── brp_portfolio_optimizer/     (seu código)
├── app.py                        (aplicação)
├── requirements.txt              (dependências)
├── install.bat                   ⭐ IMPORTANTE
├── run.bat                       ⭐ IMPORTANTE
├── cleanup.bat                   (limpeza)
├── README_CLIENTE.txt            ⭐ IMPORTANTE
├── .gitignore
└── [outros arquivos]
```

### 🚀 Instruções para Cliente

**Documento: COMO_USAR.txt** (copiar para cliente junto com ZIP)

```
INSTRUÇÕES PARA O CLIENTE
════════════════════════════════════════════════════════════

1. DESCOMPACTE o arquivo ZIP em um local simples
   Exemplo: C:\Portfolio_Optimizer

2. CLIQUE 2 VEZES em: install.bat
   ⏳ Aguarde 3-5 minutos (não feche a janela!)

3. Quando terminar, CLIQUE 2 VEZES em: run.bat

4. Seu navegador abrirá automaticamente
   Se não abrir, acesse: http://localhost:8501

5. Pronto! Use o sistema normalmente

DÚVIDAS? Leia: README_CLIENTE.txt
```

### 📊 Tamanho de Distribuição

| Item | Tamanho |
|------|---------|
| Código-fonte | ~300 KB |
| Dependências (instaladas) | ~500 MB |
| ZIP comprimido (sem venv) | ~50-100 MB |

---

## 🔄 Fluxo de Distribuição Recomendado

### Opção 1: GitHub (Recomendado)
```
Cliente baixa repositório
↓
Executa install.bat (baixa dependências automaticamente)
↓
Executa run.bat
↓
Usa o sistema
```

**Vantagens:**
- ✅ Atualizações fáceis (git pull)
- ✅ Rastreamento de versão
- ✅ Comunidade pode contribuir
- ✅ Menor tamanho (sem node_modules equivalente)

### Opção 2: ZIP Distribuído
```
Cliente recebe ZIP (sem .venv)
↓
Descompacta
↓
Executa install.bat
↓
Executa run.bat
```

**Vantagens:**
- ✅ Entrega simples
- ✅ Não precisa Git
- ✅ Controle de versão manual

### Opção 3: Executável (Futuro)
```
Use PyInstaller para criar .exe
```

---

## 📝 Exemplos de Configuração

### .gitignore (Já configurado)
Exclui automaticamente:
- Ambiente virtual (.venv/)
- Cache Python (__pycache__/)
- Arquivos temporários (temp_*.*)
- IDE (.vscode/, .idea/)

### requirements.txt (Já configurado)
Pinned versions para reprodutibilidade:
```
pandas==1.3.0
streamlit==1.28.0
# etc...
```

---

## 🔐 Segurança

### ✅ Checklist de Segurança

- [ ] Remover secrets/API keys (se houver)
- [ ] Revisar logs para dados sensíveis
- [ ] Verificar que dados do cliente não estão no repo
- [ ] .gitignore cobre todos os arquivos sensíveis

```bash
# Verificar histórico de Git
git log --all --full-history -- arquivo_sensivel.txt

# Se encontrou, remover do histórico
git filter-branch --tree-filter 'rm -f arquivo_sensivel.txt' -- --all
```

---

## 📚 Recursos Adicionais

### GitHub
- [GitHub Docs](https://docs.github.com)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Badges Shields.io](https://shields.io)

### Distribuição
- [7-Zip](https://www.7-zip.org/) - Compressor
- [Advanced Installer](https://www.advancedinstaller.com/) - Criador de instaladores
- [PyInstaller](https://pyinstaller.org/) - Converter Python em .exe

---

## 🎯 Próximas Etapas

1. **Testes Automatizados (CI/CD)**
   - GitHub Actions para testar a cada commit
   - Badge de status

2. **Documentação Adicional**
   - API documentation
   - Exemplos de uso

3. **Versões Futuros**
   - Docker image
   - Executável standalone (.exe)
   - Web app publicado (Heroku/AWS)

---

**Versão:** 1.0.0  
**Última atualização:** Janeiro 2026
