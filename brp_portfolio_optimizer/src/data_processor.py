"""
DataProcessor: Module for loading, validating, and processing trade data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processes and validates trade data for portfolio analysis."""

    def __init__(self, filepath: str):
        """
        Initializes the processor with a CSV file.

        Args:
            filepath (str): Path to the CSV file
        """
        self.filepath = Path(filepath)
        self.df = None
        self.daily_pnl = None

    def load_and_validate(self) -> bool:
        """
        Loads and validates the CSV file.

        Returns:
            bool: True if successfully validated, False otherwise
        """
        try:
            # Check file existence
            if not self.filepath.exists():
                logger.error(f"File not found: {self.filepath}")
                return False

            # Load file
            self.df = pd.read_csv(self.filepath)
            logger.info(f"File loaded: {self.filepath}")

            # Validate required columns
            required_columns = ["Open time", "Strategy name (Global)", "Profit/Loss (Global)", "Size"]
            missing_cols = [col for col in required_columns if col not in self.df.columns]

            if missing_cols:
                logger.error(f"Missing columns: {missing_cols}")
                return False

            # Validate data types
            if self.df.empty:
                logger.error("Empty DataFrame")
                return False

            logger.info(f"✅ Validation OK. {len(self.df)} trades loaded.")
            return True

        except Exception as e:
            logger.error(f"Error loading file: {e}")
            return False

    def prepare_data(self) -> Tuple[pd.DataFrame, pd.Series, Dict]:
        """
        Prepares data for optimization.

        Returns:
            Tuple: (daily_pnl_matrix, original_lots, metadata)
        """
        if self.df is None:
            raise ValueError("Data not loaded. Execute load_and_validate() first.")

        df = self.df.copy()

        # Date conversion
        df["Open time"] = pd.to_datetime(df["Open time"], dayfirst=True)
        df["Date"] = df["Open time"].dt.date
        df["Year"] = df["Open time"].dt.year
        df["Month"] = df["Open time"].dt.to_period("M")
        df["Week"] = df["Open time"].dt.to_period("W")

        # Daily pivot (Date × Strategy → PnL)
        daily_pnl = df.pivot_table(
            index="Date",
            columns="Strategy name (Global)",
            values="Profit/Loss (Global)",
            aggfunc="sum"
        ).fillna(0)

        # Original lots (median per strategy)
        original_lots = df.groupby("Strategy name (Global)")["Size"].median()

        # Metadata
        metadata = {
            "num_trades": len(df),
            "num_strategies": len(daily_pnl.columns),
            "date_range": (df["Open time"].min(), df["Open time"].max()),
            "strategies": list(daily_pnl.columns),
            "original_df": df  # Keep for metrics later
        }

        self.daily_pnl = daily_pnl
        logger.info(f"✅ Data prepared: {metadata['num_strategies']} strategies, {metadata['num_trades']} trades")

        return daily_pnl, original_lots, metadata

    def get_daily_pnl(self) -> pd.DataFrame:
        """Returns the daily PnL matrix."""
        if self.daily_pnl is None:
            raise ValueError("Data not prepared. Execute prepare_data() first.")
        return self.daily_pnl

    def get_original_df(self) -> pd.DataFrame:
        """Returns the complete original DataFrame."""
        if self.df is None:
            raise ValueError("Data not loaded.")
        return self.df.copy()
