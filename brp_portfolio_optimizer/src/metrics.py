"""
MetricsCalculator: Module for calculating performance metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Calculates performance and risk metrics for portfolios."""

    def __init__(self, trades_df: pd.DataFrame, capital_inicial: float):
        """
        Initializes the metrics calculator.

        Args:
            trades_df: DataFrame with trades (must have 'Profit/Loss (Global)' column and preferably 'Date')
            capital_inicial: Initial capital for return calculations
        """
        self.trades_df = trades_df.copy()
        self.capital_inicial = capital_inicial
        self.daily_pnl = None
        self.equity_curve = None
        
        # Ensure 'Date' column exists for grouping
        if 'Date' not in self.trades_df.columns:
            if 'Open time' in self.trades_df.columns:
                self.trades_df['Open time'] = pd.to_datetime(self.trades_df['Open time'], dayfirst=True)
                self.trades_df['Date'] = self.trades_df['Open time'].dt.date
            else:
                logger.warning("Columns 'Date' and 'Open time' not found. Creating index as date.")
                self.trades_df['Date'] = pd.date_range(start='2025-01-01', periods=len(self.trades_df), freq='D').date

    def _prepare_curves(self):
        """Prepares PnL and Equity curves."""
        if self.daily_pnl is not None:
            return  # Already prepared

        # Group PnL by day
        if 'Date' not in self.trades_df.columns:
            raise KeyError("Column 'Date' not found in DataFrame. Check input data.")
        
        # Create a copy of the dataframe for manipulation
        df_temp = self.trades_df.copy()
        
        # Convert Date column to datetime safely
        try:
            if df_temp["Date"].dtype == 'object':
                # Try to convert Period or date objects to datetime
                df_temp["Date"] = pd.to_datetime(df_temp["Date"].astype(str))
            else:
                df_temp["Date"] = pd.to_datetime(df_temp["Date"])
        except Exception as e:
            logger.warning(f"Failed to convert Date, creating sequential index: {e}")
            df_temp["Date"] = pd.date_range(start='2025-01-01', periods=len(df_temp), freq='D')
        
        # Group PnL by day
        self.daily_pnl = df_temp.groupby(df_temp["Date"].dt.date)["Profit/Loss (Global)"].sum()
        # Convert index to datetime for numeric operations
        self.daily_pnl.index = pd.to_datetime(self.daily_pnl.index)
        # Ensure values are numeric
        self.daily_pnl = self.daily_pnl.astype(float)
        self.equity_curve = self.daily_pnl.cumsum() + float(self.capital_inicial)

    def calculate_all_metrics(self) -> Dict:
        """
        Calculates all performance metrics.

        Returns:
            Dict: Dictionary with all metrics
        """
        self._prepare_curves()

        equity_series = pd.concat([pd.Series([self.capital_inicial]), self.equity_curve])
        daily_returns = equity_series.pct_change().dropna()

        # --- COUNTERS ---
        num_trades = len(self.trades_df)
        num_winning_trades = len(self.trades_df[self.trades_df["Profit/Loss (Global)"] > 0])
        num_losing_trades = len(self.trades_df[self.trades_df["Profit/Loss (Global)"] <= 0])

        # --- PROFIT/LOSS ---
        total_profit = self.trades_df["Profit/Loss (Global)"].sum()
        gross_profit = self.trades_df[self.trades_df["Profit/Loss (Global)"] > 0]["Profit/Loss (Global)"].sum()
        gross_loss = self.trades_df[self.trades_df["Profit/Loss (Global)"] <= 0]["Profit/Loss (Global)"].sum()

        # --- VOLATILITY AND SHARPE ---
        daily_vol = daily_returns.std()
        sharpe = (daily_returns.mean() / daily_vol * np.sqrt(252)) if daily_vol != 0 else 0

        # --- DRAWDOWNS ---
        hwm = self.equity_curve.cummax()
        dd_series = self.equity_curve - hwm
        max_dd_money = dd_series.min()
        max_dd_pct = ((self.equity_curve - hwm) / hwm).min() * 100

        # --- SORTINO (Downside Deviation) ---
        downside_returns = daily_returns[daily_returns < 0]
        downside_vol = downside_returns.std()
        sortino = (daily_returns.mean() / downside_vol * np.sqrt(252)) if downside_vol != 0 else 0

        # --- CALMAR (Return / Max DD) ---
        calmar = abs(total_profit / max_dd_money) if max_dd_money != 0 else np.inf

        # --- PROFIT FACTOR ---
        profit_factor = abs(gross_profit / gross_loss) if gross_loss != 0 else np.inf

        # --- WIN RATE ---
        win_rate = (num_winning_trades / num_trades * 100) if num_trades > 0 else 0

        # --- AVERAGE TRADES ---
        avg_profit_trade = gross_profit / num_winning_trades if num_winning_trades > 0 else 0
        avg_loss_trade = gross_loss / num_losing_trades if num_losing_trades > 0 else 0
        profit_loss_ratio = abs(avg_profit_trade / avg_loss_trade) if avg_loss_trade != 0 else np.inf

        # --- WORST DAY ---
        worst_day_money = self.daily_pnl.min()
        worst_day_pct = daily_returns.min() * 100

        # --- BEST DAY ---
        best_day_money = self.daily_pnl.max()
        best_day_pct = daily_returns.max() * 100

        # --- CAGR ---
        days = (self.trades_df["Open time"].max() - self.trades_df["Open time"].min()).days
        years = days / 365.25 if days > 0 else 1
        cagr = ((self.equity_curve.iloc[-1] / self.capital_inicial) ** (1 / years) - 1) * 100

        # --- TOTAL RETURN ---
        total_return_pct = ((self.equity_curve.iloc[-1] / self.capital_inicial) - 1) * 100

        # --- TEMPORAL AVERAGES ---
        if "Month" in self.trades_df.columns:
            avg_monthly = self.trades_df.groupby("Month")["Profit/Loss (Global)"].sum().mean()
        else:
            avg_monthly = 0

        if "Week" in self.trades_df.columns:
            avg_weekly = self.trades_df.groupby("Week")["Profit/Loss (Global)"].sum().mean()
        else:
            avg_weekly = 0

        if "Year" in self.trades_df.columns:
            avg_annual = self.trades_df.groupby("Year")["Profit/Loss (Global)"].sum().mean()
        else:
            avg_annual = 0

        # --- OPERATING DAYS ---
        days_operating = len(self.equity_curve)
        months_operating = days_operating / 21  # ~21 business days/month

        # Compilar tudo
        metrics = {
            # Retorno e Risco
            "Total Profit": round(total_profit, 2),
            "Total Return (%)": round(total_return_pct, 2),
            "CAGR (%)": round(cagr, 2),
            "Sharpe Ratio": round(sharpe, 2),
            "Sortino Ratio": round(sortino, 2),
            "Calmar Ratio": round(calmar, 2),
            
            # Drawdown
            "Max Drawdown ($)": round(max_dd_money, 2),
            "Max Drawdown (%)": round(max_dd_pct, 2),
            
            # Volatilidade
            "Daily Volatility (%)": round(daily_vol * 100, 2),
            "Annual Volatility (%)": round(daily_vol * np.sqrt(252) * 100, 2),
            
            # Trades
            "Total Trades": int(num_trades),
            "Winning Trades": int(num_winning_trades),
            "Losing Trades": int(num_losing_trades),
            "Win Rate (%)": round(win_rate, 2),
            "Profit Factor": round(profit_factor, 2),
            "Avg Profit Trade": round(avg_profit_trade, 2),
            "Avg Loss Trade": round(avg_loss_trade, 2),
            "Profit/Loss Ratio": round(profit_loss_ratio, 2),
            
            # Extremos
            "Best Day ($)": round(best_day_money, 2),
            "Best Day (%)": round(best_day_pct, 2),
            "Worst Day ($)": round(worst_day_money, 2),
            "Worst Day (%)": round(worst_day_pct, 2),
            
            # Médias
            "Avg Monthly Profit": round(avg_monthly, 2),
            "Avg Weekly Profit": round(avg_weekly, 2),
            "Avg Annual Profit": round(avg_annual, 2),
            
            # Tempo
            "Days Operating": int(days_operating),
            "Months Operating": round(months_operating, 1),
        }

        logger.info(f"✅ Metrics calculated: Sharpe={metrics['Sharpe Ratio']}, CAGR={metrics['CAGR (%)']}%")
        return metrics

    def get_equity_curve(self) -> pd.Series:
        """Returns the equity curve."""
        self._prepare_curves()
        return self.equity_curve

    def get_daily_pnl(self) -> pd.Series:
        """Returns the daily PnL."""
        self._prepare_curves()
        return self.daily_pnl
