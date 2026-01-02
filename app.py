"""
Streamlit Application - Professional interface for Portfolio Optimizer
"""

import streamlit as st
import pandas as pd
import numpy as np
import logging
import sys
from pathlib import Path
import quantstats as qs
import yfinance as yf
from io import StringIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add src to path (supports both layouts)
current_dir = Path(__file__).parent
src_path = current_dir / "brp_portfolio_optimizer" / "src"

# If src doesn't exist at that path, try in the root directory
if not src_path.exists():
    src_path = current_dir / "src"

sys.path.insert(0, str(src_path))
sys.path.insert(0, str(current_dir))

try:
    from data_processor import DataProcessor
    from optimizer import PortfolioOptimizer
    from metrics import MetricsCalculator
    from reports import ReportGenerator
except ImportError as e:
    st.error(f"❌ Error importing modules: {e}")
    st.info("💡 Tip: Check if you are in the correct project directory")
    st.stop()

# Streamlit configuration
st.set_page_config(
    page_title="BRP Portfolio Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0 0 0 0;
    }
    .block-container {
        padding: 2rem 2rem;
    }
    h1 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
    .metric-box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 📊 BRP Portfolio Optimizer")
st.markdown("**Intelligent portfolio optimization with risk management**")
st.divider()

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    capital_inicial = st.number_input(
        "Initial Capital ($)",
        value=100000,
        min_value=1000,
        step=5000,
        help="Total capital for allocation"
    )
    
    risk_tolerance = st.slider(
        "DD Tolerance (%)",
        min_value=5,
        max_value=50,
        value=25,
        step=5,
        help="Maximum drawdown percentage accepted per strategy"
    )
    
    benchmark = st.selectbox(
        "Benchmark",
        options=["SPY", "^BVSP", "^GSPC", "QQQ"],
        help="Index for comparison"
    )
    
    st.markdown("---")
    st.markdown("**ℹ️ Information**")
    st.info("""
    This application optimizes the allocation of multiple trading strategies:
    
    1. **Upload**: Upload a CSV file with your trades
    2. **Analysis**: The system calculates optimal allocation
    3. **Report**: Generate a professional HTML report
    """)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Analysis", "📈 Results", "📋 Report", "📊 QuantStats"])

with tab1:
    st.markdown("## 1. Upload your CSV file")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file with your trades",
        type=["csv"],
        help="Format: Open time, Strategy name (Global), Profit/Loss (Global), Size"
    )
    
    if uploaded_file is not None:
        # Save temporary file
        temp_path = Path("temp_upload.csv")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.markdown(f'<div class="success-box">✅ File uploaded: {uploaded_file.name}</div>', unsafe_allow_html=True)
        
        # Process data
        with st.spinner("🔄 Processing data..."):
            try:
                # 1. Load and validate
                processor = DataProcessor(str(temp_path))
                if not processor.load_and_validate():
                    st.markdown('<div class="error-box">❌ Error validating file</div>', unsafe_allow_html=True)
                    st.stop()
                
                # 2. Prepare data
                daily_pnl, original_lots, metadata = processor.prepare_data()
                original_df = processor.get_original_df()
                
                # Display preview
                st.markdown("### Data preview")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Number of Trades", metadata['num_trades'])
                with col2:
                    st.metric("Strategies", metadata['num_strategies'])
                with col3:
                    st.metric("Period", f"{metadata['date_range'][0].date()} → {metadata['date_range'][1].date()}")
                
                st.dataframe(original_df.head(10), use_container_width=True)
                
                # 3. Optimize
                st.markdown("---")
                st.markdown("### ⚙️ Optimizing portfolio...")
                
                optimizer = PortfolioOptimizer(daily_pnl, risk_free_rate=0.0)
                ann_mean, ann_cov = optimizer.calculate_annual_metrics()
                optimal_weights = optimizer.optimize()
                multipliers = optimizer.calculate_multipliers(
                    optimal_weights,
                    capital_inicial,
                    risk_tolerance / 100
                )
                
                # 4. Create optimized trades
                trades_original = original_df.copy()
                trades_optimized = original_df.copy()
                trades_optimized['Multiplier'] = trades_optimized['Strategy name (Global)'].map(multipliers)
                trades_optimized['Profit/Loss (Global)'] = (
                    trades_optimized['Profit/Loss (Global)'] * trades_optimized['Multiplier']
                )
                
                # Save in session state
                st.session_state.processor = processor
                st.session_state.optimizer = optimizer
                st.session_state.daily_pnl = daily_pnl
                st.session_state.original_lots = original_lots
                st.session_state.metadata = metadata
                st.session_state.optimal_weights = optimal_weights
                st.session_state.multipliers = multipliers
                st.session_state.trades_original = trades_original
                st.session_state.trades_optimized = trades_optimized
                
                st.markdown('<div class="success-box">✅ Optimization complete!</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                logger.error(f"Processing error: {e}")
                st.stop()
    else:
        st.info("👈 Upload a CSV file to start the analysis")

with tab2:
    if 'trades_original' not in st.session_state:
        st.warning("⚠️ Please upload a file in the previous tab")
    else:
        # Calculate metrics
        calc_original = MetricsCalculator(
            st.session_state.trades_original,
            capital_inicial
        )
        calc_optimized = MetricsCalculator(
            st.session_state.trades_optimized,
            capital_inicial
        )
        
        metrics_original = calc_original.calculate_all_metrics()
        metrics_optimized = calc_optimized.calculate_all_metrics()
        
        # Prepare for display
        metrics_df = pd.DataFrame([metrics_original, metrics_optimized], 
                                 index=['Original', 'Optimized']).T
        
        st.markdown("## 📊 Metrics Comparison")
        st.dataframe(metrics_df, use_container_width=True)
        
        # Chart
        st.markdown("---")
        st.markdown("### Equity Curve Comparison")
        
        equity_original = calc_original.get_equity_curve()
        equity_optimized = calc_optimized.get_equity_curve()
        
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(pd.to_datetime(equity_original.index), equity_original, label='Original', alpha=0.6, linestyle='--')
        ax.plot(pd.to_datetime(equity_optimized.index), equity_optimized, label='Optimized', linewidth=2)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_title('Equity Evolution')
        ax.set_xlabel('Date')
        ax.set_ylabel('Balance ($)')
        
        st.pyplot(fig)
        
        # Allocation table
        st.markdown("---")
        st.markdown("### 🎯 Optimal Allocation")
        
        alloc_data = []
        for i, strat in enumerate(st.session_state.daily_pnl.columns):
            peso = st.session_state.optimal_weights[i] * 100
            if peso > 0.1:
                alloc_data.append({
                    'Strategy': strat,
                    'Weight (%)': f"{peso:.2f}%",
                    'Original Lot': st.session_state.original_lots[strat],
                    'Final Lot (MT5)': round(st.session_state.original_lots[strat] * st.session_state.multipliers[strat], 2)
                })
        
        mt5_df = pd.DataFrame(alloc_data).sort_values(by='Final Lot (MT5)', ascending=False)
        st.dataframe(mt5_df, use_container_width=True)
        
        # Save for report
        st.session_state.metrics_df = metrics_df
        st.session_state.mt5_df = mt5_df
        st.session_state.calc_original = calc_original
        st.session_state.calc_optimized = calc_optimized

with tab3:
    if 'trades_original' not in st.session_state:
        st.warning("⚠️ Run the analysis in the previous tab")
    else:
        st.markdown("## 📋 Report Generation")
        
        col1, col2 = st.columns(2)
        with col1:
            report_format = st.radio(
                "Report format",
                options=["HTML", "Excel"],
                horizontal=True
            )
        
        if st.button("📥 Generate Report", use_container_width=True):
            with st.spinner("⏳ Generating report..."):
                try:
                    report_gen = ReportGenerator(output_dir="outputs")
                    
                    # Generate chart
                    chart_b64 = report_gen.generate_comparison_chart(
                        st.session_state.calc_original.get_equity_curve(),
                        st.session_state.calc_optimized.get_equity_curve()
                    )
                    
                    if report_format == "HTML":
                        output_file = report_gen.generate_html_report(
                            st.session_state.metrics_df,
                            st.session_state.mt5_df,
                            chart_b64
                        )
                        
                        st.markdown(f'<div class="success-box">✅ Report generated successfully!</div>', 
                                  unsafe_allow_html=True)
                        
                        # Display HTML report
                        st.markdown("---")
                        st.markdown("### 📄 Report Preview")
                        with open(output_file, "r", encoding="utf-8") as f:
                            html_content = f.read()
                        st.components.v1.html(html_content, height=1500, scrolling=True)
                        
                        # Download button at the end
                        st.markdown("---")
                        st.markdown("### 📥 Download")
                        with open(output_file, "rb") as f:
                            st.download_button(
                                label=f"📥 Download {Path(output_file).name}",
                                data=f.read(),
                                file_name=Path(output_file).name,
                                mime="text/html",
                                use_container_width=True
                            )
                    else:
                        output_file = report_gen.generate_excel_report(
                            st.session_state.metrics_df,
                            st.session_state.mt5_df,
                            st.session_state.trades_original,
                            st.session_state.trades_optimized
                        )
                        
                        st.markdown(f'<div class="success-box">✅ Report generated: {Path(output_file).name}</div>', 
                                  unsafe_allow_html=True)
                        
                        # Download button for Excel
                        st.markdown("---")
                        with open(output_file, "rb") as f:
                            st.download_button(
                                label=f"📥 Download {Path(output_file).name}",
                                data=f.read(),
                                file_name=Path(output_file).name,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                    
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error generating report: {str(e)}</div>', 
                              unsafe_allow_html=True)

with tab4:
    if 'trades_original' not in st.session_state:
        st.warning("⚠️ Please upload a file in the previous tab")
    else:
        st.markdown("## 📊 QuantStats Report")
        st.markdown("Detailed performance analysis with QuantStats")
        
        # Choose which portfolio to analyze
        portfolio_choice = st.radio(
            "Select the portfolio:",
            ["Original", "Optimized"],
            horizontal=True
        )
        
        if st.button("🔄 Generate QuantStats Report", use_container_width=True):
            with st.spinner("⏳ Generating QuantStats analysis..."):
                try:
                    # Choose the correct data
                    if portfolio_choice == "Original":
                        calc = st.session_state.calc_original
                        trades_df = st.session_state.trades_original
                    else:
                        calc = st.session_state.calc_optimized
                        trades_df = st.session_state.trades_optimized
                    
                    # Get equity curve
                    equity_curve = calc.get_equity_curve()
                    
                    # Calculate daily returns
                    daily_returns = equity_curve.pct_change().dropna()
                    
                    # Fetch benchmark data
                    st.info(f"📊 Loading benchmark data: {benchmark}...")
                    
                    # Determine analysis period from trade data
                    start_date = st.session_state.metadata['date_range'][0]
                    end_date = st.session_state.metadata['date_range'][1]
                    
                    try:
                        # Download benchmark data
                        benchmark_data = yf.download(
                            benchmark,
                            start=start_date,
                            end=end_date,
                            progress=False
                        )
                        
                        if len(benchmark_data) > 0:
                            # Calculate benchmark returns - try different column names
                            price_col = None
                            if 'Adj Close' in benchmark_data.columns:
                                price_col = 'Adj Close'
                            elif 'Close' in benchmark_data.columns:
                                price_col = 'Close'
                            else:
                                # If neither exists, use the first price column
                                price_col = benchmark_data.columns[0]
                            
                            benchmark_returns = benchmark_data[price_col].pct_change().dropna()
                            
                            # Align indices
                            common_dates = daily_returns.index.intersection(benchmark_returns.index)
                            daily_returns_aligned = daily_returns.loc[common_dates]
                            benchmark_returns_aligned = benchmark_returns.loc[common_dates]
                            
                            st.success(f"✅ Benchmark {benchmark} loaded with {len(benchmark_returns_aligned)} days (column: {price_col})")
                        else:
                            st.warning(f"⚠️ No data for benchmark {benchmark}, using analysis without comparison")
                            benchmark_returns_aligned = None
                    except Exception as e:
                        st.warning(f"⚠️ Error loading benchmark: {str(e)}")
                        logger.error(f"Benchmark error: {e}")
                        benchmark_returns_aligned = None
                    
                    # Generate QuantStats HTML report
                    report_file = f"temp_qs_report_{portfolio_choice.lower()}.html"
                    
                    # Generate report with benchmark (if available)
                    qs.reports.html(
                        daily_returns,
                        benchmark=benchmark_returns_aligned,
                        output=report_file,
                        title=f"Portfolio Performance Report - {portfolio_choice} (Benchmark: {benchmark})",
                        download_filename=f"quantstats_report_{portfolio_choice}_{benchmark}.html"
                    )
                    
                    # Read and display report
                    with open(report_file, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    
                    # Display in Streamlit
                    st.components.v1.html(html_content, height=2000, scrolling=True)
                    
                    # Download button
                    with open(report_file, "rb") as f:
                        st.download_button(
                            label=f"📥 Download QuantStats Report ({portfolio_choice} vs {benchmark})",
                            data=f.read(),
                            file_name=f"quantstats_report_{portfolio_choice}_{benchmark}.html",
                            mime="text/html",
                            use_container_width=True
                        )
                    
                    st.markdown('<div class="success-box">✅ QuantStats report generated successfully!</div>', 
                              unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Error generating QuantStats report: {str(e)}</div>', 
                              unsafe_allow_html=True)
                    logger.error(f"QuantStats error: {e}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 12px;">
    <p>BRP Portfolio Optimizer v1.0 | Developed by BRP Quant Capital</p>
    <p>© 2026 - All rights reserved</p>
</div>
""", unsafe_allow_html=True)
