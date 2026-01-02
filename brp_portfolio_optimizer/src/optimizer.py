"""
PortfolioOptimizer: Portfolio optimization module using Markowitz and Position Sizing.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class PortfolioOptimizer:
    """Optimizes portfolio allocation using Markowitz Mean-Variance."""

    def __init__(self, daily_pnl: pd.DataFrame, risk_free_rate: float = 0.0):
        """
        Initializes the optimizer.

        Args:
            daily_pnl (pd.DataFrame): Daily PnL matrix (Date × Strategy)
            risk_free_rate (float): Risk-free rate for Sharpe Ratio
        """
        self.daily_pnl = daily_pnl
        self.risk_free_rate = risk_free_rate
        self.ann_mean = None
        self.ann_cov = None
        self.optimal_weights = None

    def calculate_annual_metrics(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculates annualized returns and covariance.

        Returns:
            Tuple: (annual_returns, annual_covariance)
        """
        # Assume 252 trading days per year
        ann_mean = self.daily_pnl.mean() * 252
        ann_cov = self.daily_pnl.cov() * 252

        self.ann_mean = ann_mean.values
        self.ann_cov = ann_cov.values

        logger.info("✅ Annualized metrics calculated")
        return self.ann_mean, self.ann_cov

    @staticmethod
    def _negative_sharpe(weights: np.ndarray, mean_returns: np.ndarray,
                         cov_matrix: np.ndarray, rf: float = 0.0) -> float:
        """
        Calculates negative Sharpe Ratio (for minimization).

        Args:
            weights: Portfolio weights
            mean_returns: Annualized mean returns
            cov_matrix: Covariance matrix
            rf: Risk-free rate

        Returns:
            float: -Sharpe Ratio
        """
        p_ret = np.sum(mean_returns * weights)
        p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        if p_vol == 0:
            return 0

        sharpe = (p_ret - rf) / p_vol
        return -sharpe

    def optimize(self) -> np.ndarray:
        """
        Optimizes portfolio weights by maximizing Sharpe Ratio.

        Returns:
            np.ndarray: Optimal normalized weights [0, 1]
        """
        if self.ann_mean is None or self.ann_cov is None:
            self.calculate_annual_metrics()

        num_assets = len(self.daily_pnl.columns)

        # Constraint: Sum of weights = 1
        constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}

        # Bounds: Weights between 0 and 1 (no shorting)
        bounds = tuple((0, 1) for _ in range(num_assets))

        # Initial guess: Equal Weight
        init_guess = np.array([1.0 / num_assets] * num_assets)

        # Optimize
        result = minimize(
            self._negative_sharpe,
            init_guess,
            args=(self.ann_mean, self.ann_cov, self.risk_free_rate),
            method="SLSQP",
            bounds=bounds,
            constraints=constraints
        )

        self.optimal_weights = result.x
        logger.info(f"✅ Optimization completed. Sharpe: {-result.fun:.2f}")

        return self.optimal_weights

    def calculate_multipliers(self, optimal_weights: np.ndarray, capital_inicial: float,
                             risk_tolerance_dd: float = 0.25) -> Dict[str, float]:
        """
        Calculates lot multipliers based on risk management.

        Args:
            optimal_weights: Optimal weights
            capital_inicial: Total capital
            risk_tolerance_dd: DD tolerance (e.g., 0.25 = 25%)

        Returns:
            Dict: {strategy_name: multiplier}
        """
        # Calculate Maximum Drawdown for each strategy
        cum_ret = self.daily_pnl.cumsum()
        peaks = cum_ret.cummax()
        drawdowns = cum_ret - peaks
        max_dd_money = drawdowns.min().abs()
        max_dd_money = max_dd_money.replace(0, 1)  # Avoid division by zero

        multipliers = {}
        for i, strategy in enumerate(self.daily_pnl.columns):
            weight = optimal_weights[i]
            allocated_capital = capital_inicial * weight
            risk_budget = allocated_capital * risk_tolerance_dd
            dd_value = max_dd_money[strategy]

            multiplier = risk_budget / dd_value if dd_value > 0 else 1.0
            multipliers[strategy] = multiplier

        logger.info(f"✅ Multipliers calculated for {len(multipliers)} strategies")
        return multipliers

    def get_optimal_weights(self) -> Dict[str, float]:
        """Returns optimal weights as a dictionary."""
        if self.optimal_weights is None:
            raise ValueError("Optimization not performed. Execute optimize() first.")

        return {
            strategy: weight
            for strategy, weight in zip(self.daily_pnl.columns, self.optimal_weights)
        }
