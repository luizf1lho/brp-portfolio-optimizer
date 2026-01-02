# 📊 BRP Portfolio Optimizer

Aplicação profissional e modular para otimização de portfólio de estratégias de trading usando Markowitz Mean-Variance e gestão inteligente de risco.

## ✨ Características

- ✅ **Upload de CSV**: Interface amigável para carregar dados de trades
- ✅ **Otimização Markowitz**: Maximização do Sharpe Ratio com restrições de risco
- ✅ **Position Sizing**: Dimensionamento inteligente de lotes baseado em histórico de drawdown
- ✅ **Métricas Completas**: 20+ métricas de performance (Sharpe, Sortino, Calmar, etc)
- ✅ **Relatórios Profissionais**: HTML e Excel com gráficos e tabelas
- ✅ **Configuração MT5**: Tabela pronta para usar em MetaTrader 5
- ✅ **Interface Interativa**: Streamlit com controles ajustáveis

## 🚀 Quick Start

### 1. Instalação

```bash
# Clone ou navegue até o projeto
cd brp_portfolio_optimizer

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# MacOS/Linux:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 2. Execute a Aplicação

```bash
streamlit run app.py
```

Acesse em seu navegador: `http://localhost:8501`

### 3. Use o Aplicativo

1. **Carregue seu CSV** com colunas:
   - `Open time` (data/hora do trade)
   - `Strategy name (Global)` (nome da estratégia)
   - `Profit/Loss (Global)` (lucro/prejuízo em $)
   - `Size` (tamanho do lote original)

2. **Configure os parâmetros**:
   - Capital Inicial
   - Tolerância de Drawdown
   - Benchmark para comparação

3. **Analise os resultados**:
   - Visualize o comparativo Original vs Otimizado
   - Veja as métricas detalhadas
   - Gere relatório em HTML ou Excel

4. **Baixe o relatório** e configure no MT5

## 📁 Estrutura do Projeto

```
brp_portfolio_optimizer/
├── app.py                          # Aplicação Streamlit (Frontend)
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── brp_portfolio_optimizer/        # Pacote principal
│   ├── src/
│   │   ├── __init__.py
│   │   ├── data_processor.py       # Carregamento e validação de dados
│   │   ├── optimizer.py            # Otimização Markowitz + Position Sizing
│   │   ├── metrics.py              # Cálculo de métricas de performance
│   │   └── reports.py              # Geração de relatórios HTML/Excel
│   ├── config/
│   │   └── settings.py             # Configurações e constantes
│   ├── data/                       # Dados de entrada (CSV)
│   ├── outputs/                    # Relatórios gerados
│   ├── logs/                       # Arquivos de log
│   └── tests/                      # Testes unitários (futuro)
```

## 🧮 Como Funciona

### 1. Data Processing
- Carrega CSV e valida colunas obrigatórias
- Converte datas e cria períodos (Year, Month, Week)
- Pivota dados em matriz diária (Date × Strategy → PnL)
- Calcula lotes originais (mediana por estratégia)

### 2. Otimização (Markowitz)
- Calcula retornos anualizados (×252 dias úteis)
- Computa matriz de covariância anualizada
- **Minimiza**: $-\text{Sharpe} = -\frac{\mu_p - r_f}{\sigma_p}$
- **Restrições**: 
  - Soma dos pesos = 1 (100% do capital)
  - Pesos ∈ [0, 1] (sem short, sem alavancagem)

### 3. Position Sizing
```
Risk Budget = Capital Alocado × Tolerância de DD
Multiplicador = Risk Budget / Drawdown Histórico Máximo
Lote Final = Lote Original × Multiplicador
```

Isso garante que cada estratégia operando com seu lote otimizado,
o drawdown histórico máximo nunca exceda o orçamento de risco alocado.

### 4. Análise de Performance

**Métricas de Risco:**
- Max Drawdown ($ e %)
- Daily/Annual Volatility
- Pior Dia

**Métricas de Retorno:**
- Total Profit / Total Return %
- CAGR (Compound Annual Growth Rate)

**Métricas de Eficiência:**
- Sharpe Ratio (Retorno/Volatilidade)
- Sortino Ratio (Retorno/Downside Volatility)
- Calmar Ratio (Retorno/Max DD)
- Profit Factor (Ganhos/Perdas)
- Win Rate %

## 📊 Exemplo de Uso

```python
from src.data_processor import DataProcessor
from src.optimizer import PortfolioOptimizer
from src.metrics import MetricsCalculator
from src.reports import ReportGenerator

# 1. Carregar dados
processor = DataProcessor("data/trades.csv")
processor.load_and_validate()
daily_pnl, original_lots, metadata = processor.prepare_data()

# 2. Otimizar
optimizer = PortfolioOptimizer(daily_pnl)
optimal_weights = optimizer.optimize()
multipliers = optimizer.calculate_multipliers(optimal_weights, capital_inicial=100000)

# 3. Calcular métricas
calc = MetricsCalculator(trades_optimized, capital_inicial=100000)
metrics = calc.calculate_all_metrics()

# 4. Gerar relatório
report_gen = ReportGenerator(output_dir="outputs")
chart_b64 = report_gen.generate_comparison_chart(equity_orig, equity_opt)
report_path = report_gen.generate_html_report(metrics_df, mt5_df, chart_b64)
```

## ⚙️ Configurações

Edite `config/settings.py` para customizar:

- **DEFAULT_CAPITAL_INICIAL**: Capital padrão
- **DEFAULT_RISK_TOLERANCE_DD**: Tolerância de DD
- **BENCHMARK_SYMBOL**: Índice para comparação
- **REQUIRED_COLUMNS**: Colunas obrigatórias do CSV

## 🔍 Validações Implementadas

- ✅ Arquivo CSV existe
- ✅ Colunas obrigatórias presentes
- ✅ Tipos de dados corretos
- ✅ DataFrame não vazio
- ✅ Datas válidas
- ✅ Valores numéricos válidos

## 📈 Saídas Geradas

- **Relatório HTML**: Dashboard interativo com:
  - Gráfico comparativo (Original vs Otimizado)
  - Tabela de métricas
  - Configuração MT5
  
- **Relatório Excel**: Múltiplas abas:
  - Métricas
  - Configuração MT5
  - Trades Original
  - Trades Otimizado

## 🛠️ Tecnologias

- **Python 3.8+**
- **Pandas**: Manipulação de dados
- **NumPy**: Cálculos numéricos
- **SciPy**: Otimização (minimize)
- **Matplotlib**: Visualização
- **Streamlit**: Interface web
- **OpenPyXL**: Relatórios Excel

## 📝 Próximas Melhorias

- [ ] Backtesting walk-forward (IS/OOS automático)
- [ ] Análise de correlação entre estratégias
- [ ] Stress testing (cenários extremos)
- [ ] API para integração com brokers
- [ ] Testes unitários completos
- [ ] Docker container
- [ ] Deployment em nuvem

## 📧 Suporte

Para dúvidas ou problemas, entre em contato com:
**BRP Quant Capital**

## 📜 Licença

© 2026 BRP Quant Capital - Todos os direitos reservados

---

**Versão**: 1.0.0  
**Última atualização**: Janeiro 2026
