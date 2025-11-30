"""
FinRobot Web Interface - Streamlit App
A beautiful UI for AI-powered financial analysis
"""

import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_default_response():
    """Default AI response when no specific query is detected"""
    return """👋 Hello! I'm your **AI Financial Analyst**. I can help you with:

📊 **Stock Analysis** - Ask about any stock ticker
> *Example: "Tell me about AAPL" or "What's NVDA's price?"*

📈 **Market Insights** - Get current market data
> *Example: "How is MSFT performing?" or "Analyze TSLA"*

💡 **Investment Info** - General financial guidance
> *Example: "Compare GOOGL and META"*

**Try asking:**
- "What is the price of NVDA?"
- "Tell me about Apple stock"
- "Analyze Microsoft for me"
"""

# Page config
st.set_page_config(
    page_title="FinRobot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 0;
    }
    
    .sub-header {
        text-align: center;
        color: #888;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #fff !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1e3f 0%, #2d2d5a 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #3d3d7a;
    }
    
    [data-testid="stMetric"] label {
        color: #a0a0ff !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #fff !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Text inputs */
    .stTextInput input {
        background: #1e1e3f;
        border: 1px solid #3d3d7a;
        border-radius: 8px;
        color: #fff;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #1e1e3f;
        border-radius: 8px;
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Info boxes */
    .stAlert {
        background: #1e1e3f;
        border: 1px solid #3d3d7a;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_configured' not in st.session_state:
    # Check if environment variables are set
    st.session_state.api_configured = bool(os.environ.get('OPENAI_API_KEY') or os.environ.get('FINNHUB_API_KEY'))

# Load API keys from config if exists
try:
    from finrobot.utils import register_keys_from_json
    if os.path.exists('config_api_keys'):
        register_keys_from_json('config_api_keys')
        st.session_state.api_configured = True
except:
    pass

# Sidebar
with st.sidebar:
    st.markdown("## 🤖 FinRobot")
    st.markdown("*AI Financial Analysis*")
    st.markdown("---")
    
    # API Key configuration
    with st.expander("🔑 API Keys", expanded=not st.session_state.api_configured):
        openai_key = st.text_input("OpenAI API Key", type="password", 
                                    value=os.environ.get('OPENAI_API_KEY', ''))
        finnhub_key = st.text_input("Finnhub API Key", type="password",
                                     value=os.environ.get('FINNHUB_API_KEY', ''))
        
        if st.button("💾 Save Keys"):
            if openai_key:
                os.environ['OPENAI_API_KEY'] = openai_key
            if finnhub_key:
                os.environ['FINNHUB_API_KEY'] = finnhub_key
            if openai_key or finnhub_key:
                st.session_state.api_configured = True
                st.success("✅ Keys saved!")
                st.rerun()
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 📌 Navigation")
    page = st.radio("Select Feature", [
        "🏠 Dashboard",
        "📊 Stock Analysis",
        "🤖 AI Chat",
        "📈 Charts",
        "📉 Backtesting",
        "📄 Reports"
    ], label_visibility="collapsed")

# Main content
st.markdown('<h1 class="main-header">🤖 FinRobot AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Financial Analysis Platform</p>', unsafe_allow_html=True)

# ============================================================
# DASHBOARD PAGE
# ============================================================
if page == "🏠 Dashboard":
    st.markdown("### 📊 Market Overview")
    
    try:
        from finrobot.data_source import YFinanceUtils
        
        # Stock metrics in columns
        tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
        cols = st.columns(5)
        
        for ticker, col in zip(tickers, cols):
            with col:
                try:
                    info = YFinanceUtils.get_stock_info(ticker)
                    price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                    prev_close = info.get('previousClose', price)
                    change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0
                    
                    st.metric(
                        label=ticker,
                        value=f"${price:.2f}",
                        delta=f"{change_pct:+.2f}%"
                    )
                except Exception as e:
                    st.metric(label=ticker, value="--", delta="N/A")
        
        st.markdown("---")
        
        # Quick info cards
        st.markdown("### 🎯 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            📈 **Stock Analysis**
            
            Deep dive into any stock with AI-powered insights, financials, and news.
            """)
            
        with col2:
            st.success("""
            🤖 **AI Chat**
            
            Chat with our financial AI to get instant market insights and recommendations.
            """)
            
        with col3:
            st.warning("""
            📉 **Backtesting**
            
            Test trading strategies on historical data with detailed performance metrics.
            """)
        
        # Footer stats
        st.markdown("---")
        st.markdown("### 📈 Platform Stats")
        stat1, stat2, stat3, stat4 = st.columns(4)
        
        with stat1:
            st.metric("Data Sources", "5+", help="YFinance, Finnhub, SEC, FMP, Reddit")
        with stat2:
            st.metric("AI Agents", "5", help="Market Analyst, Expert Investor, etc.")
        with stat3:
            st.metric("Analysis Types", "6", help="Fundamental, Technical, Sentiment, etc.")
        with stat4:
            st.metric("Report Types", "4", help="Quick, Full, Technical, Comparison")
            
    except ImportError as e:
        st.error(f"Error loading data sources: {e}")
        st.info("Please ensure all dependencies are installed.")

# ============================================================
# STOCK ANALYSIS PAGE
# ============================================================
elif page == "📊 Stock Analysis":
    st.markdown("### 📊 Stock Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL", max_chars=5).upper()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🔍 Analyze", use_container_width=True)
    
    if analyze_btn and ticker:
        with st.spinner(f"Analyzing {ticker}..."):
            try:
                from finrobot.data_source import YFinanceUtils, FinnHubUtils
                
                # Get data
                info = YFinanceUtils.get_stock_info(ticker)
                
                if not info:
                    st.error(f"Could not find data for {ticker}")
                else:
                    # Header
                    st.markdown(f"## {info.get('longName', ticker)}")
                    st.caption(f"{info.get('industry', 'N/A')} | {info.get('sector', 'N/A')}")
                    
                    # Key metrics
                    st.markdown("### 📈 Key Metrics")
                    m1, m2, m3, m4 = st.columns(4)
                    
                    with m1:
                        price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                        st.metric("Price", f"${price:.2f}")
                    with m2:
                        mcap = info.get('marketCap', 0)
                        if mcap >= 1e12:
                            st.metric("Market Cap", f"${mcap/1e12:.2f}T")
                        else:
                            st.metric("Market Cap", f"${mcap/1e9:.2f}B")
                    with m3:
                        st.metric("PE Ratio", f"{info.get('trailingPE', 0):.1f}")
                    with m4:
                        st.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 0):.2f}")
                    
                    m5, m6, m7, m8 = st.columns(4)
                    with m5:
                        st.metric("Forward PE", f"{info.get('forwardPE', 0):.1f}")
                    with m6:
                        div_yield = info.get('dividendYield', 0) or 0
                        st.metric("Div Yield", f"{div_yield*100:.2f}%")
                    with m7:
                        st.metric("Beta", f"{info.get('beta', 0):.2f}")
                    with m8:
                        st.metric("52W Low", f"${info.get('fiftyTwoWeekLow', 0):.2f}")
                    
                    # Tabs for different info
                    tab1, tab2, tab3 = st.tabs(["📝 About", "💰 Financials", "📰 News"])
                    
                    with tab1:
                        summary = info.get('longBusinessSummary', 'No description available.')
                        st.write(summary)
                    
                    with tab2:
                        try:
                            income = YFinanceUtils.get_income_stmt(ticker)
                            if income is not None and not income.empty:
                                st.markdown("#### Income Statement")
                                st.dataframe(income.head(10), use_container_width=True)
                            else:
                                st.info("Income statement not available")
                        except Exception as e:
                            st.info(f"Financial data not available: {e}")
                    
                    with tab3:
                        try:
                            end_date = datetime.now().strftime("%Y-%m-%d")
                            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                            news = FinnHubUtils.get_company_news(ticker, start_date, end_date, max_news_num=5)
                            
                            if news is not None and not news.empty:
                                for _, article in news.iterrows():
                                    with st.container():
                                        st.markdown(f"**{article['headline']}**")
                                        st.caption(f"📅 {article.get('datetime', 'Unknown date')} | 🔗 {article.get('source', 'Unknown')}")
                                        st.markdown("---")
                            else:
                                st.info("No recent news available")
                        except Exception as e:
                            st.info(f"News not available: {e}")
                    
            except Exception as e:
                st.error(f"Error analyzing {ticker}: {str(e)}")

# ============================================================
# AI CHAT PAGE
# ============================================================
elif page == "🤖 AI Chat":
    st.markdown("### 🤖 Chat with AI Financial Analyst")
    
    if not st.session_state.api_configured:
        st.warning("⚠️ Please configure your API keys in the sidebar to use the AI Chat feature.")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about stocks, markets, or investments..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    from finrobot.data_source import YFinanceUtils
                    import re
                    
                    # Extract ticker if mentioned
                    ticker_match = re.search(r'\b([A-Z]{1,5})\b', prompt.upper())
                    
                    if ticker_match and any(word in prompt.lower() for word in ['price', 'stock', 'analyze', 'tell', 'about', 'what']):
                        ticker = ticker_match.group(1)
                        
                        # Skip common words
                        if ticker not in ['I', 'A', 'THE', 'IS', 'IT', 'TO', 'FOR', 'AND', 'OR', 'OF', 'IN', 'ON', 'AT']:
                            try:
                                info = YFinanceUtils.get_stock_info(ticker)
                                if info and info.get('longName'):
                                    price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                                    mcap = info.get('marketCap', 0)
                                    mcap_str = f"${mcap/1e12:.2f}T" if mcap >= 1e12 else f"${mcap/1e9:.2f}B"
                                    
                                    response = f"""Here's what I found about **{ticker}** ({info.get('longName', 'N/A')}):

| Metric | Value |
|--------|-------|
| 💰 Current Price | **${price:.2f}** |
| 📊 Market Cap | {mcap_str} |
| 📈 PE Ratio | {info.get('trailingPE', 0):.1f} |
| 📉 52-Week Range | ${info.get('fiftyTwoWeekLow', 0):.2f} - ${info.get('fiftyTwoWeekHigh', 0):.2f} |
| 💵 Dividend Yield | {(info.get('dividendYield', 0) or 0)*100:.2f}% |

**About the company:**
{(info.get('longBusinessSummary', 'No description available.'))[:400]}...

*Want more details? Try "Analyze {ticker}" in the Stock Analysis tab!*"""
                                else:
                                    response = f"I couldn't find data for **{ticker}**. Please check if it's a valid stock ticker."
                            except:
                                response = f"I couldn't retrieve data for **{ticker}**. Please try again."
                        else:
                            response = get_default_response()
                    else:
                        response = get_default_response()
                    
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================
# CHARTS PAGE
# ============================================================
elif page == "📈 Charts":
    st.markdown("### 📈 Stock Charts")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        ticker = st.text_input("Ticker Symbol", value="AAPL", key="chart_ticker").upper()
    with col2:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90))
    with col3:
        end_date = st.date_input("End Date", datetime.now())
    
    chart_type = st.selectbox("Chart Type", ["Candlestick", "Line", "OHLC"])
    
    if st.button("📈 Generate Chart", use_container_width=True):
        with st.spinner("Generating chart..."):
            try:
                import matplotlib.pyplot as plt
                import mplfinance as mpf
                from finrobot.data_source import YFinanceUtils
                
                # Get data
                data = YFinanceUtils.get_stock_data(
                    ticker, 
                    start_date.strftime("%Y-%m-%d"), 
                    end_date.strftime("%Y-%m-%d")
                )
                
                if data is not None and not data.empty:
                    # Handle multi-index columns
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                    
                    # Chart type mapping
                    type_map = {"Candlestick": "candle", "Line": "line", "OHLC": "ohlc"}
                    
                    # Create chart
                    fig, axes = mpf.plot(
                        data, 
                        type=type_map[chart_type], 
                        style='nightclouds',
                        title=f'{ticker} Stock Price',
                        ylabel='Price ($)',
                        volume=True,
                        returnfig=True,
                        figsize=(12, 8)
                    )
                    
                    st.pyplot(fig)
                    
                    # Stats
                    st.markdown("### 📊 Period Statistics")
                    s1, s2, s3, s4 = st.columns(4)
                    with s1:
                        st.metric("Open", f"${data['Open'].iloc[0]:.2f}")
                    with s2:
                        st.metric("Close", f"${data['Close'].iloc[-1]:.2f}")
                    with s3:
                        st.metric("High", f"${data['High'].max():.2f}")
                    with s4:
                        st.metric("Low", f"${data['Low'].min():.2f}")
                    
                else:
                    st.error("No data available for this ticker/date range")
                    
            except Exception as e:
                st.error(f"Error generating chart: {str(e)}")

# ============================================================
# BACKTESTING PAGE
# ============================================================
elif page == "📉 Backtesting":
    st.markdown("### 📉 Strategy Backtesting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Ticker", value="AAPL", key="backtest_ticker").upper()
        strategy = st.selectbox("Strategy", ["SMA Crossover"])
        start_date = st.date_input("Start Date", datetime(2024, 1, 1), key="bt_start")
    
    with col2:
        initial_cash = st.number_input("Initial Cash ($)", value=100000, step=10000)
        position_size = st.number_input("Position Size (shares)", value=100, step=10)
        end_date = st.date_input("End Date", datetime(2024, 6, 30), key="bt_end")
    
    # Strategy parameters
    with st.expander("⚙️ Strategy Parameters"):
        fast_sma = st.slider("Fast SMA Period", 5, 50, 10)
        slow_sma = st.slider("Slow SMA Period", 20, 200, 30)
    
    if st.button("🚀 Run Backtest", use_container_width=True):
        if start_date >= end_date:
            st.error("Start date must be before end date")
        else:
            with st.spinner("Running backtest... This may take a moment."):
                try:
                    from finrobot.functional.quantitative import BackTraderUtils
                    
                    result = BackTraderUtils.back_test(
                        ticker_symbol=ticker,
                        start_date=start_date.strftime("%Y-%m-%d"),
                        end_date=end_date.strftime("%Y-%m-%d"),
                        strategy="SMA_CrossOver",
                        strategy_params=f'{{"fast": {fast_sma}, "slow": {slow_sma}}}',
                        sizer=position_size,
                        cash=float(initial_cash),
                    )
                    
                    st.success("✅ Backtest Complete!")
                    
                    # Parse results (simplified display)
                    st.markdown("### 📊 Results")
                    st.code(result, language="python")
                    
                except Exception as e:
                    st.error(f"Backtest error: {str(e)}")

# ============================================================
# REPORTS PAGE
# ============================================================
elif page == "📄 Reports":
    st.markdown("### 📄 Generate Research Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Company Ticker", value="AAPL", key="report_ticker").upper()
    
    with col2:
        report_type = st.selectbox("Report Type", [
            "Quick Summary",
            "Full Research Report",
        ])
    
    if st.button("📝 Generate Report", use_container_width=True):
        with st.spinner(f"Generating {report_type} for {ticker}..."):
            try:
                from finrobot.data_source import YFinanceUtils
                
                info = YFinanceUtils.get_stock_info(ticker)
                
                if not info or not info.get('longName'):
                    st.error(f"Could not find data for {ticker}")
                else:
                    price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                    mcap = info.get('marketCap', 0)
                    mcap_str = f"${mcap/1e12:.2f}T" if mcap >= 1e12 else f"${mcap/1e9:.2f}B"
                    
                    # Generate report
                    report = f"""# {info.get('longName', ticker)} ({ticker})
## Equity Research Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")} | **Analyst:** FinRobot AI

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| Current Price | **${price:.2f}** |
| Market Cap | {mcap_str} |
| PE Ratio (TTM) | {info.get('trailingPE', 'N/A'):.1f if isinstance(info.get('trailingPE'), (int, float)) else 'N/A'} |
| Forward PE | {info.get('forwardPE', 'N/A'):.1f if isinstance(info.get('forwardPE'), (int, float)) else 'N/A'} |
| PEG Ratio | {info.get('pegRatio', 'N/A'):.2f if isinstance(info.get('pegRatio'), (int, float)) else 'N/A'} |
| Dividend Yield | {(info.get('dividendYield', 0) or 0)*100:.2f}% |
| 52-Week High | ${info.get('fiftyTwoWeekHigh', 0):.2f} |
| 52-Week Low | ${info.get('fiftyTwoWeekLow', 0):.2f} |
| Beta | {info.get('beta', 'N/A'):.2f if isinstance(info.get('beta'), (int, float)) else 'N/A'} |
| Avg Volume | {info.get('averageVolume', 0):,.0f} |

---

## 📝 Company Overview

**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}

{info.get('longBusinessSummary', 'No description available.')}

---

## 💡 Investment Highlights

Based on current metrics:
- **Valuation:** {"Reasonable" if info.get('trailingPE', 100) < 25 else "Premium"} PE of {info.get('trailingPE', 0):.1f}x
- **Market Position:** {mcap_str} market cap indicates {"large-cap" if mcap >= 10e9 else "mid-cap" if mcap >= 2e9 else "small-cap"} status
- **Income:** {"Dividend-paying" if (info.get('dividendYield', 0) or 0) > 0 else "Growth-focused (no dividend)"}

---

*This report was generated by FinRobot AI for informational purposes only. Not financial advice.*
"""
                    
                    st.markdown(report)
                    
                    # Download buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📥 Download as Markdown",
                            data=report,
                            file_name=f"{ticker}_report_{datetime.now().strftime('%Y%m%d')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            label="📄 Download as Text",
                            data=report,
                            file_name=f"{ticker}_report_{datetime.now().strftime('%Y%m%d')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 <strong>FinRobot AI</strong> | Powered by AutoGen & OpenAI</p>
    <p style="font-size: 0.8rem;">Built for CapGlobal | Data from YFinance, Finnhub, SEC</p>
</div>
""", unsafe_allow_html=True)
