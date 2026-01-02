# 📊 BRP Portfolio Optimizer

> **Otimização de Portfólio de Trading com Markowitz - Aplicação Web Profissional**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Objetivo

Transformar múltiplas estratégias de trading em um **portfólio otimizado** usando o modelo de **Markowitz Mean-Variance**, com interface web intuitiva e relatórios profissionais.

## ✨ Funcionalidades

- 📤 **Upload de Dados**: Carregue arquivos CSV com seus trades
- 🔍 **Validação Automática**: Verificação de integridade de dados
- ⚙️ **Otimização de Portfólio**: Algoritmo Markowitz com SciPy
- 📊 **Métricas Avançadas**: 20+ indicadores de performance (Sharpe, Sortino, Calmar, etc.)
- 📈 **QuantStats**: Análise detalhada com comparação vs benchmark
- 📋 **Relatórios**: Exportar em HTML e Excel
- 🎨 **Interface Web**: Dashboard profissional com Streamlit

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8 ou superior
- Windows, macOS ou Linux

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/brp-portfolio-optimizer.git
cd brp-portfolio-optimizer

# Execute o instalador (Windows)
install.bat

# Inicie a aplicação
run.bat
```

**Ou manualmente:**

```bash
# Crie ambiente virtual
python -m venv .venv

# Ative (Windows)
.venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Inicie
streamlit run app.py
```

## 📁 Estrutura do Projeto

```
brp_optimize_portfolio/
├── brp_portfolio_optimizer/
│   ├── src/
│   │   ├── data_processor.py      # Carregamento e validação de dados
│   │   ├── optimizer.py           # Algoritmo Markowitz
│   │   ├── metrics.py             # Cálculo de métricas
│   │   ├── reports.py             # Geração de relatórios
│   │   └── settings.py            # Configurações
│   └── __init__.py
├── app.py                          # Aplicação Streamlit
├── requirements.txt                # Dependências Python
├── install.bat                     # Script de instalação (Windows)
├── run.bat                         # Script para executar (Windows)
├── run.sh                          # Script para executar (Linux/Mac)
└── README.md                       # Este arquivo
```

## 📊 Formato de Entrada

Seu arquivo CSV deve conter:

| Open time | Strategy name (Global) | Profit/Loss (Global) | Size |
|-----------|------------------------|----------------------|------|
| 2025-01-15 10:30 | Strategy_A | 500.00 | 1.0 |
| 2025-01-15 14:45 | Strategy_B | -150.50 | 0.5 |
| 2025-01-16 09:15 | Strategy_A | 1200.00 | 1.5 |

## 🧮 Algoritmo

O otimizador usa **Markowitz Mean-Variance Optimization**:

```
Maximize: (μp - rf) / σp  (Sharpe Ratio)

Subject to:
  Σ weights = 1
  0 ≤ weight ≤ 1 para cada estratégia
  
Solver: SciPy SLSQP (Sequential Least Squares Programming)
```

## 📈 Métricas Calculadas

### Risco
- Volatilidade Anualizada
- Drawdown Máximo
- Calmar Ratio

### Retorno
- Retorno Total
- CAGR (Compound Annual Growth Rate)
- Retorno Mensal Médio

### Eficiência
- Sharpe Ratio
- Sortino Ratio
- Profit Factor
- Taxa de Acerto

## 🔧 Dependências

```
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
streamlit>=1.28.0
openpyxl>=3.8.0
quantstats>=0.0.59
yfinance>=0.2.0
python-dateutil>=2.8.0
```

## 💡 Exemplos de Uso

### 1. Upload e Análise
1. Acesse a aba "Upload & Análise"
2. Carregue seu arquivo CSV
3. Ajuste Capital Inicial, Tolerância de DD e Benchmark
4. Clique em "Otimizar"

### 2. Visualizar Resultados
1. Acesse a aba "Resultados"
2. Compare métricas Original vs Otimizado
3. Visualize as Equity Curves

### 3. Gerar Relatórios
1. Aba "Relatório": Crie HTML ou Excel profissional
2. Aba "QuantStats": Análise detalhada com benchmark

## 🐛 Troubleshooting

### "Streamlit not found"
```bash
# Solução
.venv\Scripts\python.exe -m streamlit run app.py
```

### "ModuleNotFoundError"
```bash
# Reinstale dependências
pip install -r requirements.txt --force-reinstall
```

### Porta 8501 em uso
```bash
# Use outra porta
streamlit run app.py --server.port 8502
```

## 📊 Exemplo de Saída

O otimizador retorna:
- **Pesos Otimizados**: Alocação em % para cada estratégia
- **Multiplicadores**: Fator de posicionamento por estratégia
- **Métricas Comparativas**: Antes vs Depois da otimização
- **Relatórios HTML/Excel**: Documentação profissional

## 🤝 Contribuindo

Sugestões e contribuições são bem-vindas!

1. Faça um Fork
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob MIT - veja [LICENSE](LICENSE) para detalhes.

## 👨‍💼 Autor

**BRP Quant Capital**
- 📧 Email: contact@brpquant.com
- 🌐 Website: www.brpquant.com

## 🙏 Agradecimentos

- Streamlit pela excelente framework web
- QuantStats pela análise de performance
- Comunidade Python

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**
