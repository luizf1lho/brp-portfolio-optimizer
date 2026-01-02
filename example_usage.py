"""
Exemplo de uso do BRP Portfolio Optimizer (Modo Script/CLI)
Útil para integração em pipelines ou execução automática
"""

import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/optimizer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "brp_portfolio_optimizer" / "src"))

from data_processor import DataProcessor
from optimizer import PortfolioOptimizer
from metrics import MetricsCalculator
from reports import ReportGenerator


def main():
    """Exemplo de uso programático do otimizador."""
    
    logger.info("=" * 60)
    logger.info("BRP Portfolio Optimizer - Modo Script")
    logger.info("=" * 60)
    
    # Configurações
    csv_file = "data/trades.csv"  # Seu arquivo
    capital_inicial = 100000
    risk_tolerance_dd = 0.25  # 25%
    benchmark = "SPY"
    
    # 1. CARREGAMENTO DE DADOS
    logger.info("\n[ETAPA 1] Carregando dados...")
    processor = DataProcessor(csv_file)
    
    if not processor.load_and_validate():
        logger.error("Falha na validação do arquivo")
        return False
    
    daily_pnl, original_lots, metadata = processor.prepare_data()
    original_df = processor.get_original_df()
    
    logger.info(f"✓ {metadata['num_trades']} trades de {metadata['num_strategies']} estratégias")
    logger.info(f"✓ Período: {metadata['date_range'][0].date()} → {metadata['date_range'][1].date()}")
    
    # 2. OTIMIZAÇÃO
    logger.info("\n[ETAPA 2] Otimizando portfólio...")
    optimizer = PortfolioOptimizer(daily_pnl, risk_free_rate=0.0)
    optimizer.calculate_annual_metrics()
    optimal_weights = optimizer.optimize()
    
    weights_dict = optimizer.get_optimal_weights()
    logger.info("✓ Pesos ótimos calculados:")
    for strategy, weight in sorted(weights_dict.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            logger.info(f"  - {strategy}: {weight*100:.2f}%")
    
    # 3. POSITION SIZING
    logger.info("\n[ETAPA 3] Calculando multiplicadores...")
    multipliers = optimizer.calculate_multipliers(
        optimal_weights,
        capital_inicial,
        risk_tolerance_dd
    )
    
    logger.info("✓ Multiplicadores de lote:")
    for strategy, mult in sorted(multipliers.items(), key=lambda x: x[1], reverse=True):
        original_lote = original_lots[strategy]
        new_lote = round(original_lote * mult, 2)
        logger.info(f"  - {strategy}: {original_lote} → {new_lote} (×{mult:.2f})")
    
    # 4. CRIAR TRADES OTIMIZADOS
    logger.info("\n[ETAPA 4] Criando trades otimizados...")
    trades_original = original_df.copy()
    trades_optimized = original_df.copy()
    trades_optimized['Multiplier'] = trades_optimized['Strategy name (Global)'].map(multipliers)
    trades_optimized['Profit/Loss (Global)'] = (
        trades_optimized['Profit/Loss (Global)'] * trades_optimized['Multiplier']
    )
    
    # 5. CALCULAR MÉTRICAS
    logger.info("\n[ETAPA 5] Calculando métricas...")
    calc_original = MetricsCalculator(trades_original, capital_inicial)
    calc_optimized = MetricsCalculator(trades_optimized, capital_inicial)
    
    metrics_original = calc_original.calculate_all_metrics()
    metrics_optimized = calc_optimized.calculate_all_metrics()
    
    logger.info("✓ Portfólio Original:")
    logger.info(f"  - Sharpe: {metrics_original['Sharpe Ratio']}")
    logger.info(f"  - CAGR: {metrics_original['CAGR (%)']}%")
    logger.info(f"  - Max DD: {metrics_original['Max Drawdown (%)']}%")
    
    logger.info("✓ Portfólio Otimizado:")
    logger.info(f"  - Sharpe: {metrics_optimized['Sharpe Ratio']}")
    logger.info(f"  - CAGR: {metrics_optimized['CAGR (%)']}%")
    logger.info(f"  - Max DD: {metrics_optimized['Max Drawdown (%)']}%")
    
    melhoria_sharpe = ((metrics_optimized['Sharpe Ratio'] / metrics_original['Sharpe Ratio']) - 1) * 100
    logger.info(f"✓ Melhoria de Sharpe: {melhoria_sharpe:+.1f}%")
    
    # 6. GERAR RELATÓRIO
    logger.info("\n[ETAPA 6] Gerando relatório...")
    import pandas as pd
    
    metrics_df = pd.DataFrame([metrics_original, metrics_optimized], 
                             index=['Original', 'Otimizado']).T
    
    mt5_data = []
    for i, strat in enumerate(daily_pnl.columns):
        peso = optimal_weights[i] * 100
        if peso > 0.1:
            mt5_data.append({
                'Estratégia': strat,
                'Peso (%)': f"{peso:.2f}%",
                'Lote Original': original_lots[strat],
                'Lote Final (MT5)': round(original_lots[strat] * multipliers[strat], 2)
            })
    
    mt5_df = pd.DataFrame(mt5_data).sort_values(by='Lote Final (MT5)', ascending=False)
    
    report_gen = ReportGenerator(output_dir="outputs")
    
    # Gráfico
    equity_original = calc_original.get_equity_curve()
    equity_optimized = calc_optimized.get_equity_curve()
    chart_b64 = report_gen.generate_comparison_chart(equity_original, equity_optimized)
    
    # HTML
    html_path = report_gen.generate_html_report(metrics_df, mt5_df, chart_b64)
    logger.info(f"✓ Relatório HTML: {html_path}")
    
    # Excel
    excel_path = report_gen.generate_excel_report(
        metrics_df,
        mt5_df,
        trades_original,
        trades_optimized
    )
    logger.info(f"✓ Relatório Excel: {excel_path}")
    
    # 7. EXIBIR TABELA MT5
    logger.info("\n[ETAPA 7] Configuração MT5:")
    logger.info("\n" + mt5_df.to_string(index=False))
    
    logger.info("\n" + "=" * 60)
    logger.info("✓ Otimização concluída com sucesso!")
    logger.info("=" * 60 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)
