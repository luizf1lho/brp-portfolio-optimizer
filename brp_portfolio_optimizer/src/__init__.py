"""
BRP Portfolio Optimizer - Módulo de otimização de portfólio profissional
Versão: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "BRP Quant Capital"

from .data_processor import DataProcessor
from .optimizer import PortfolioOptimizer
from .metrics import MetricsCalculator
from .reports import ReportGenerator

__all__ = [
    "DataProcessor",
    "PortfolioOptimizer",
    "MetricsCalculator",
    "ReportGenerator",
]
