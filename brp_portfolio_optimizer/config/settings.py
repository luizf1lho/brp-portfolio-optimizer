"""
Application default configuration file.
"""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they do not exist
for directory in [DATA_DIR, OUTPUTS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Optimization Configuration (Defaults)
DEFAULT_CAPITAL_INICIAL = 100000
DEFAULT_RISK_TOLERANCE_DD = 0.25  # 25% DD allowed per allocation
DEFAULT_RISK_FREE_RATE = 0.0

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Report Configuration
BENCHMARK_SYMBOL = "SPY"
REPORT_FORMAT = "html"  # html, excel, both

# File Configuration
ALLOWED_EXTENSIONS = [".csv"]
MAX_FILE_SIZE_MB = 100

# CSV Column Configuration
REQUIRED_COLUMNS = [
    "Open time",
    "Strategy name (Global)",
    "Profit/Loss (Global)",
    "Size"
]

# Metrics Configuration
RISK_METRICS = [
    "Max Drawdown ($)",
    "Max Drawdown (%)",
    "Daily Volatility (%)",
    "Annual Volatility (%)"
]

RETURN_METRICS = [
    "Total Profit",
    "Total Return (%)",
    "CAGR (%)"
]

EFFICIENCY_METRICS = [
    "Sharpe Ratio",
    "Sortino Ratio",
    "Calmar Ratio",
    "Profit Factor",
    "Win Rate (%)"
]
