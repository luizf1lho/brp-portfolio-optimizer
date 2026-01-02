# 🔧 TROUBLESHOOTING - Erro "streamlit not found"

## ❌ Problema
```
streamlit : The term 'streamlit' is not recognized as the name of a cmdlet
```

## ✅ Solução (3 opções)

### **Opção 1: Usar o script corrigido (RECOMENDADO)**

Clique 2× em:
```
run.bat  (Windows)
```

Ou execute:
```bash
cd c:\brp_quant_capital\5_monitoring_trades\brp_optimize_portfolio
.\run.bat
```

---

### **Opção 2: Instalação Manual Completa**

```powershell
# 1. Navegue até o diretório do projeto
cd c:\brp_quant_capital\5_monitoring_trades\brp_optimize_portfolio

# 2. Crie um novo ambiente virtual (apagará o antigo)
Remove-Item .venv -Recurse -Force
python -m venv .venv

# 3. Ative o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 4. Atualize o pip
python -m pip install --upgrade pip

# 5. Instale todas as dependências
pip install pandas numpy scipy matplotlib streamlit openpyxl quantstats python-dateutil

# 6. Execute a aplicação
streamlit run app.py
```

---

### **Opção 3: Usar Python diretamente**

```powershell
cd c:\brp_quant_capital\5_monitoring_trades\brp_optimize_portfolio

# Execute o Python do ambiente virtual
.\.venv\Scripts\python.exe -m streamlit run app.py
```

---

## 🔍 Verificação

Se ainda não funcionar, execute:

```powershell
# Verificar se Python está instalado
python --version

# Verificar se o ambiente virtual existe
Test-Path ".venv"  # Deve retornar True

# Verificar se Streamlit está instalado
.\.venv\Scripts\python.exe -c "import streamlit; print('OK')"
```

---

## 📝 Notas Importantes

1. **Ambiente Virtual**: O projeto usa `.venv` (com ponto antes)
2. **Python 3.8+**: Versão mínima necessária
3. **Windows PowerShell**: Use `Activate.ps1` (não `.bat`)
4. **Dependências**: Todas listadas em `requirements.txt`

---

## ✨ Se ainda não funcionar

1. Abra PowerShell como **Administrador**
2. Execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Tente novamente

---

## 💡 Quick Reference

| Ação | Comando |
|------|---------|
| Ativar ambiente | `.\.venv\Scripts\Activate.ps1` |
| Instalar deps | `pip install -r requirements.txt` |
| Executar app | `streamlit run app.py` |
| Desativar venv | `deactivate` |

---

**Versão**: 1.0.0  
**Data**: Janeiro 2026
