# 🚀 SETUP - Guia de Instalação e Execução

## ⚡ Quick Start (30 segundos)

### Windows
```powershell
# Abra PowerShell e navegue até a pasta do projeto
cd c:\brp_quant_capital\5_monitoring_trades\brp_optimize_portfolio

# Execute o script
.\run.bat
```

### macOS / Linux
```bash
cd ~/brp_portfolio_optimizer
chmod +x run.sh
./run.sh
```

A aplicação abrirá automaticamente em `http://localhost:8501`

---

## 📋 Instalação Detalhada

### Pré-requisitos
- **Python 3.8+** instalado (verifique com: `python --version`)
- **pip** instalado
- Conexão com internet (para download de dependências)

### Passo 1: Clone ou Navegue até o Projeto

```bash
cd c:\brp_quant_capital\5_monitoring_trades\brp_optimize_portfolio
```

### Passo 2: Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Você deve ver `(venv)` no início da linha do terminal.

### Passo 3: Instale as Dependências

```bash
pip install -r requirements.txt
```

Isso instalará:
- pandas, numpy, scipy (cálculos)
- matplotlib (gráficos)
- streamlit (interface web)
- openpyxl (relatórios Excel)

### Passo 4: Execute a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

---

## 📚 Como Usar a Aplicação

### 1️⃣ Aba "Upload & Análise"

**Formato do CSV obrigatório:**

```
Open time,Strategy name (Global),Profit/Loss (Global),Size
01/01/2024 10:30,Strategy A,150.50,0.5
01/01/2024 11:45,Strategy B,-50.00,0.3
01/01/2024 14:20,Strategy A,200.75,0.5
```

**Colunas necessárias:**
- `Open time`: Data e hora do trade (formato: DD/MM/YYYY HH:MM)
- `Strategy name (Global)`: Nome da estratégia
- `Profit/Loss (Global)`: Lucro/prejuízo em dólares
- `Size`: Tamanho do lote original (ex: 0.5, 1.0)

**Configurações:**
- **Capital Inicial**: Quanto você tem para investir
- **Tolerância de DD**: Quanto risco aceita por estratégia (em %)
- **Benchmark**: Índice para comparação (SPY, ^BVSP, etc)

### 2️⃣ Aba "Resultados"

Aqui você verá:
- ✅ Gráfico comparando Original vs Otimizado
- ✅ Tabela com 20+ métricas
- ✅ Alocação ótima por estratégia
- ✅ Lotes para MT5

### 3️⃣ Aba "Relatório"

Gere relatórios:
- **HTML**: Dashboard profissional interativo
- **Excel**: Múltiplas abas com dados detalhados

---

## 💻 Modo Script (Programático)

Se preferir não usar a interface web:

```python
# Execute exemplo_uso.py
python example_usage.py
```

Isso gerará relatórios automaticamente em `outputs/`

---

## 📊 Entendendo os Resultados

### Sharpe Ratio
- **O que é**: Retorno por unidade de risco
- **Mais alto = Melhor** (>1.0 é bom)
- **Exemplo**: Sharpe 1.5 significa melhor eficiência que 1.0

### Max Drawdown
- **O que é**: Maior queda desde o pico
- **Mais baixo = Melhor** (% negativo)
- **Exemplo**: -15% significa perdeu no máximo 15% do valor

### Win Rate
- **O que é**: % de trades vencedores
- **Mais alto = Melhor**
- **Exemplo**: 60% = 6 em cada 10 trades ganham

### CAGR
- **O que é**: Taxa anual de retorno (composto)
- **Mais alto = Melhor**
- **Exemplo**: 30% CAGR = cresce 30% ao ano

### Profit Factor
- **O que é**: Ganhos totais / Perdas totais
- **Mais alto = Melhor** (>2.0 é excelente)
- **Exemplo**: 2.5 = ganha $2.50 para cada $1 perdido

---

## 🛠️ Troubleshooting

### ❌ Erro: "Python não encontrado"
```
Solução: Instale Python do python.org e selecione "Add to PATH"
```

### ❌ Erro: "ModuleNotFoundError"
```
Solução: Verifique se o ambiente virtual está ativado (venv)
Execute: pip install -r requirements.txt
```

### ❌ Erro: "Streamlit not found"
```
Solução: Execute dentro do ambiente virtual
pip install streamlit
```

### ❌ Arquivo CSV não aceito
```
Solução: Verifique se as colunas estão exatamente assim:
- Open time
- Strategy name (Global)
- Profit/Loss (Global)
- Size
```

### ❌ Porta 8501 já em uso
```
Solução: Execute em outra porta
streamlit run app.py --server.port 8502
```

---

## 📁 Estrutura de Pastas

```
brp_portfolio_optimizer/
├── app.py                      ← Execute isto (Streamlit)
├── example_usage.py            ← Ou isto (Script)
├── run.bat                     ← Ou isto (Windows)
├── run.sh                      ← Ou isto (macOS/Linux)
├── requirements.txt            ← Dependências
├── README.md                   ← Documentação completa
├── SETUP.md                    ← Este arquivo
│
├── brp_portfolio_optimizer/
│   ├── src/
│   │   ├── data_processor.py   ← Carrega e valida CSV
│   │   ├── optimizer.py        ← Calcula pesos ótimos
│   │   ├── metrics.py          ← Calcula métricas
│   │   └── reports.py          ← Gera relatórios
│   ├── config/
│   │   └── settings.py         ← Configurações
│   ├── data/                   ← Coloque seus CSVs aqui
│   └── outputs/                ← Relatórios gerados aqui
│
├── tests/
│   └── test_optimizer.py       ← Testes unitários
│
└── logs/
    └── optimizer.log           ← Arquivo de log
```

---

## 🧪 Executar Testes

```bash
# Instale pytest primeiro
pip install pytest

# Execute os testes
pytest tests/ -v
```

---

## 🌐 Acessar de Outro Computador

Se quiser acessar de outro PC na rede:

```bash
# No servidor (seu computador)
streamlit run app.py --server.address 0.0.0.0

# No cliente (outro computador)
Abra: http://<seu_ip>:8501
```

---

## 📈 Próximas Etapas

1. **Integração MT5**: Configure os lotes otimizados no seu Expert Advisor
2. **Backtesting**: Compare performance antes e depois
3. **Monitoramento**: Acompanhe a performance em tempo real
4. **Reotimização**: Execute novamente mensalmente com dados atualizados

---

## 📧 Suporte

Dúvidas? Consulte:
- [README.md](README.md) - Documentação técnica
- [example_usage.py](example_usage.py) - Código comentado
- Logs em `logs/optimizer.log`

---

**Versão**: 1.0.0  
**Última atualização**: Janeiro 2026  
**Desenvolvido por**: BRP Quant Capital
