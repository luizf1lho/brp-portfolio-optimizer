"""
ReportGenerator: Module for generating professional reports (HTML, Excel, etc).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import os
import re
from pathlib import Path
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates professional performance reports."""

    def __init__(self, output_dir: str = "outputs"):
        """
        Initializes the report generator.

        Args:
            output_dir (str): Output directory for reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_comparison_chart(
        self,
        equity_original: pd.Series,
        equity_optimized: pd.Series,
        oos_date: str = None
    ) -> str:
        """
        Generates comparative equity curve chart.

        Args:
            equity_original: Equity series of the original portfolio
            equity_optimized: Equity series of the optimized portfolio
            oos_date: OOS start date (YYYY-MM-DD format)

        Returns:
            str: Base64 encoded PNG image
        """
        plt.figure(figsize=(12, 6))
        plt.style.use("seaborn-v0_8-whitegrid")

        # Plot curves
        plt.plot(
            pd.to_datetime(equity_original.index),
            equity_original,
            label="Original (Flat)",
            color="#95a5a6",
            alpha=0.6,
            linestyle="--"
        )
        plt.plot(
            pd.to_datetime(equity_optimized.index),
            equity_optimized,
            label="Optimized (Smart Risk)",
            color="#2c3e50",
            linewidth=2.5
        )

        # OOS line
        if oos_date:
            oos_dt = pd.to_datetime(oos_date)
            plt.axvline(oos_dt, color="#e74c3c", linestyle=":", linewidth=2)
            plt.text(oos_dt, equity_optimized.max(), "  OOS START", 
                    color="#e74c3c", fontweight="bold", fontsize=9)

        plt.title("Optimization Comparison: Equity Curve", fontsize=12, pad=15, loc="left", fontweight="bold")
        plt.legend(frameon=True, framealpha=1, shadow=True)
        plt.tight_layout()

        # Convert to base64
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format="png", dpi=100)
        img_buf.seek(0)
        img_base64 = base64.b64encode(img_buf.read()).decode("utf-8")
        plt.close()

        logger.info("✅ Comparative chart generated")
        return img_base64

    def generate_html_report(
        self,
        metrics_comparison: pd.DataFrame,
        mt5_allocation: pd.DataFrame,
        chart_base64: str,
        filename: str = "Portfolio_Report.html"
    ) -> str:
        """
        Generates professional HTML report.

        Args:
            metrics_comparison: DataFrame with metrics comparison (Original vs Optimized)
            mt5_allocation: DataFrame with MT5 allocation (Strategy, Weight, Lot)
            chart_base64: Chart in base64
            filename: Output file name

        Returns:
            str: Full path to generated file
        """
        # CSS
        css = """
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Roboto', sans-serif;
            background: #ecf0f1;
            color: #2c3e50;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #1f77b4, #0d47a1);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .section {
            background: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-top: 4px solid #1f77b4;
        }
        
        .section h2 {
            font-size: 20px;
            margin-bottom: 20px;
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        table thead {
            background-color: #34495e;
            color: white;
        }
        
        table th, table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        table tbody tr:nth-of-type(even) {
            background-color: #f8f9fa;
        }
        
        table tbody tr:hover {
            background-color: #f1f4f8;
        }
        
        .metric-highlight {
            font-weight: bold;
            color: #1f77b4;
            font-size: 16px;
        }
        
        .positive { color: #27ae60; }
        .negative { color: #e74c3c; }
        
        img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin: 15px 0;
        }
        
        .footer {
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #bdc3c7;
        }
        """

        # Assemble HTML tables
        metrics_html = metrics_comparison.to_html(classes="table")
        mt5_html = mt5_allocation.to_html(classes="table", index=False)

        # Full HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portfolio Optimization Report</title>
            <style>
                {css}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Portfolio Optimization Report</h1>
                    <p>BRP Quant Capital - Portfolio Optimizer v1.0</p>
                </div>
                
                <div class="section">
                    <h2>1. Executive Analysis</h2>
                    <p>Comparison between the original portfolio (flat) and the optimized portfolio with intelligent risk management.</p>
                    <img src="data:image/png;base64,{chart_base64}" alt="Equity Curve Comparison">
                </div>
                
                <div class="section">
                    <h2>2. Performance Metrics</h2>
                    {metrics_html}
                </div>
                
                <div class="section">
                    <h2>3. MetaTrader 5 Configuration</h2>
                    <p>Use the lots below to configure your Expert Advisor.</p>
                    {mt5_html}
                </div>
                
                <div class="footer">
                    <p>Report generated automatically by BRP Portfolio Optimizer</p>
                    <p>Date: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Save
        output_path = self.output_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"✅ HTML report generated: {output_path}")
        return str(output_path)

    def generate_excel_report(
        self,
        metrics_comparison: pd.DataFrame,
        mt5_allocation: pd.DataFrame,
        trades_original: pd.DataFrame,
        trades_optimized: pd.DataFrame,
        filename: str = "Portfolio_Report.xlsx"
    ) -> str:
        """
        Generates Excel report with multiple sheets.

        Args:
            metrics_comparison: Metrics comparison
            mt5_allocation: MT5 allocation
            trades_original: Original trades
            trades_optimized: Optimized trades
            filename: File name

        Returns:
            str: Path to generated file
        """
        output_path = self.output_dir / filename

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            metrics_comparison.to_excel(writer, sheet_name="Metrics")
            mt5_allocation.to_excel(writer, sheet_name="MT5 Configuration", index=False)
            trades_original.to_excel(writer, sheet_name="Original Trades", index=False)
            trades_optimized.to_excel(writer, sheet_name="Optimized Trades", index=False)

        logger.info(f"✅ Excel report generated: {output_path}")
        return str(output_path)
