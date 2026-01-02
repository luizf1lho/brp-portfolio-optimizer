"""
Testes unitários para o BRP Portfolio Optimizer
Rode com: pytest tests/
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "brp_portfolio_optimizer" / "src"))

from data_processor import DataProcessor
from optimizer import PortfolioOptimizer
from metrics import MetricsCalculator


class TestDataProcessor:
    """Testes para o módulo DataProcessor."""
    
    @pytest.fixture
    def sample_df(self):
        """Cria um DataFrame de exemplo para testes."""
        dates = pd.date_range('2024-01-01', periods=50, freq='D')
        data = {
            'Open time': dates,
            'Strategy name (Global)': np.random.choice(['Strategy A', 'Strategy B'], 50),
            'Profit/Loss (Global)': np.random.randn(50) * 1000,
            'Size': np.random.uniform(0.1, 1.0, 50)
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def sample_csv(self, tmp_path, sample_df):
        """Cria um arquivo CSV temporário para testes."""
        csv_file = tmp_path / "test_trades.csv"
        sample_df.to_csv(csv_file, index=False)
        return str(csv_file)
    
    def test_load_and_validate_success(self, sample_csv):
        """Testa carregamento bem-sucedido."""
        processor = DataProcessor(sample_csv)
        assert processor.load_and_validate() == True
    
    def test_load_and_validate_file_not_found(self):
        """Testa erro quando arquivo não existe."""
        processor = DataProcessor("nonexistent.csv")
        assert processor.load_and_validate() == False
    
    def test_prepare_data(self, sample_csv):
        """Testa preparação de dados."""
        processor = DataProcessor(sample_csv)
        processor.load_and_validate()
        daily_pnl, original_lots, metadata = processor.prepare_data()
        
        assert isinstance(daily_pnl, pd.DataFrame)
        assert isinstance(original_lots, pd.Series)
        assert isinstance(metadata, dict)
        assert metadata['num_trades'] > 0
        assert metadata['num_strategies'] > 0


class TestPortfolioOptimizer:
    """Testes para o módulo PortfolioOptimizer."""
    
    @pytest.fixture
    def sample_daily_pnl(self):
        """Cria uma matrix de PnL diário de exemplo."""
        dates = pd.date_range('2024-01-01', periods=50)
        data = {
            'Strategy A': np.random.randn(50) * 100,
            'Strategy B': np.random.randn(50) * 100,
            'Strategy C': np.random.randn(50) * 100
        }
        return pd.DataFrame(data, index=dates)
    
    def test_calculate_annual_metrics(self, sample_daily_pnl):
        """Testa cálculo de métricas anualizadas."""
        optimizer = PortfolioOptimizer(sample_daily_pnl)
        ann_mean, ann_cov = optimizer.calculate_annual_metrics()
        
        assert isinstance(ann_mean, np.ndarray)
        assert isinstance(ann_cov, np.ndarray)
        assert len(ann_mean) == 3  # 3 estratégias
        assert ann_cov.shape == (3, 3)
    
    def test_optimize(self, sample_daily_pnl):
        """Testa otimização de pesos."""
        optimizer = PortfolioOptimizer(sample_daily_pnl)
        weights = optimizer.optimize()
        
        assert isinstance(weights, np.ndarray)
        assert len(weights) == 3
        assert np.isclose(np.sum(weights), 1.0)  # Soma = 1
        assert np.all(weights >= 0)  # Sem short
        assert np.all(weights <= 1)  # Sem alavancagem
    
    def test_calculate_multipliers(self, sample_daily_pnl):
        """Testa cálculo de multiplicadores."""
        optimizer = PortfolioOptimizer(sample_daily_pnl)
        weights = optimizer.optimize()
        
        multipliers = optimizer.calculate_multipliers(
            weights,
            capital_inicial=100000,
            risk_tolerance_dd=0.25
        )
        
        assert isinstance(multipliers, dict)
        assert len(multipliers) == 3
        assert all(v > 0 for v in multipliers.values())


class TestMetricsCalculator:
    """Testes para o módulo MetricsCalculator."""
    
    @pytest.fixture
    def sample_trades_df(self):
        """Cria um DataFrame de trades para testes."""
        dates = pd.date_range('2024-01-01', periods=100)
        data = {
            'Open time': dates,
            'Date': dates.date,
            'Strategy name (Global)': np.random.choice(['Strategy A', 'Strategy B'], 100),
            'Profit/Loss (Global)': np.random.randn(100) * 500 + 100,
            'Size': 0.5
        }
        df = pd.DataFrame(data)
        df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
        df['Week'] = pd.to_datetime(df['Date']).dt.to_period('W')
        df['Year'] = pd.to_datetime(df['Date']).dt.year
        return df
    
    def test_calculate_all_metrics(self, sample_trades_df):
        """Testa cálculo de todas as métricas."""
        calc = MetricsCalculator(sample_trades_df, capital_inicial=100000)
        metrics = calc.calculate_all_metrics()
        
        assert isinstance(metrics, dict)
        assert 'Sharpe Ratio' in metrics
        assert 'CAGR (%)' in metrics
        assert 'Max Drawdown (%)' in metrics
        assert 'Win Rate (%)' in metrics
        assert all(isinstance(v, (int, float)) for v in metrics.values())
    
    def test_get_equity_curve(self, sample_trades_df):
        """Testa obtenção da curva de equity."""
        calc = MetricsCalculator(sample_trades_df, capital_inicial=100000)
        equity_curve = calc.get_equity_curve()
        
        assert isinstance(equity_curve, pd.Series)
        assert equity_curve.iloc[0] > 0  # Começa com capital inicial


# Testes de Integração
class TestIntegration:
    """Testes de integração entre módulos."""
    
    @pytest.fixture
    def complete_workflow(self, tmp_path):
        """Cria um workflow completo para teste."""
        # Criar dados
        dates = pd.date_range('2024-01-01', periods=60, freq='D')
        data = {
            'Open time': dates,
            'Strategy name (Global)': np.random.choice(['StratA', 'StratB', 'StratC'], 60),
            'Profit/Loss (Global)': np.random.randn(60) * 1000 + 100,
            'Size': 0.5
        }
        df = pd.DataFrame(data)
        
        # Salvar como CSV
        csv_file = tmp_path / "integration_test.csv"
        df.to_csv(csv_file, index=False)
        
        return str(csv_file)
    
    def test_full_pipeline(self, complete_workflow):
        """Testa todo o pipeline de otimização."""
        # Carregar
        processor = DataProcessor(complete_workflow)
        assert processor.load_and_validate()
        
        daily_pnl, original_lots, metadata = processor.prepare_data()
        assert metadata['num_strategies'] > 0
        
        # Otimizar
        optimizer = PortfolioOptimizer(daily_pnl)
        weights = optimizer.optimize()
        assert np.isclose(np.sum(weights), 1.0)
        
        # Multiplicadores
        multipliers = optimizer.calculate_multipliers(weights, 100000, 0.25)
        assert len(multipliers) == metadata['num_strategies']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
