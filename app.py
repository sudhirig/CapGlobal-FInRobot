"""
FinRobot Web Interface - Streamlit App
A beautiful UI for AI-powered financial analysis
"""

import streamlit as st
import os
import sys
import pandas as pd
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page config
st.set_page_config(
    page_title="FinRobot AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono&display=swap');
    
    .main-header {
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #0f3460;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .stock-ticker {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        color: #00d9ff;
    }
    
    .price-up { color: #00ff88; }
    .price-down { color: #ff4757; }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
    }
    
    .sidebar .stSelectbox label {
        color: #a0a0a0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_configured' not in st.session_state:
    st.session_state.api_configured = False

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/AI4Finance-Foundation/FinRobot/main/figs/logo_white_background.jpg", width=200)
    st.markdown("---")
    
    st.markdown("### ⚙️ Configuration")
    
    # API Key configuration
    with st.expander("🔑 API Keys", expanded=not st.session_state.api_configured):
        openai_key = st.text_input("OpenAI API Key", type="password", 
                                    value=os.environ.get('OPENAI_API_KEY', ''))
        finnhub_key = st.text_input("Finnhub API Key", type="password",
                                     value=os.environ.get('FINNHUB_API_KEY', ''))
        
        if st.button("Save Keys"):
            if openai_key and finnhub_key:
                os.environ['OPENAI_API_KEY'] = openai_key
                os.environ['FINNHUB_API_KEY'] = finnhub_key
                st.session_state.api_configured = True
                st.success("✅ API keys configured!")
            else:
                st.error("Please provide both API keys")
    
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
    ])

# Main content
st.markdown('<h1 class="main-header">🤖 FinRobot AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #888;">AI-Powered Financial Analysis Platform</p>', unsafe_allow_html=True)

# Dashboard
if page == "🏠 Dashboard":
    st.markdown("### 📊 Market Overview")
    
    try:
        from finrobot.data_source import YFinanceUtils
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
        cols = [col1, col2, col3, col4, col5]
        
        for ticker, col in zip(tickers, cols):
            with col:
                try:
                    info = YFinanceUtils.get_stock_info(ticker)
                    price = info.get('currentPrice', 0)
                    change = info.get('regularMarketChangePercent', 0)
                    
                    delta_color = "normal" if change >= 0 else "inverse"
                    st.metric(
                        label=ticker,
                        value=f"${price:.2f}",
                        delta=f"{change:.2f}%",
                        delta_color=delta_color
                    )
                except Exception as e:
                    st.metric(label=ticker, value="N/A", delta="--")
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 🎯 Quick Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📈 **S&P 500**\nTrack major indices")
        with col2:
            st.success("🤖 **AI Agents**\n5 specialists ready")
        with col3:
            st.warning("📰 **News**\nReal-time updates")
            
    except ImportError:
        st.warning("Installing dependencies... Please refresh in a moment.")

# Stock Analysis
elif page == "📊 Stock Analysis":
    st.markdown("### 📊 Stock Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker", value="AAPL", max_chars=5).upper()
    
    with col2:
        analyze_btn = st.button("🔍 Analyze", use_container_width=True)
    
    if analyze_btn and ticker:
        with st.spinner(f"Analyzing {ticker}..."):
            try:
                from finrobot.data_source import YFinanceUtils, FinnHubUtils
                
                # Get data
                info = YFinanceUtils.get_stock_info(ticker)
                
                # Display metrics
                st.markdown(f"## {info.get('longName', ticker)}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Price", f"${info.get('currentPrice', 0):.2f}")
                with col2:
                    mcap = info.get('marketCap', 0) / 1e12
                    st.metric("Market Cap", f"${mcap:.2f}T")
                with col3:
                    st.metric("PE Ratio", f"{info.get('trailingPE', 0):.1f}")
                with col4:
                    st.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 0):.2f}")
                
                # Company info
                st.markdown("### 📝 About")
                st.write(info.get('longBusinessSummary', 'No description available.')[:500] + "...")
                
                # Financials
                st.markdown("### 💰 Financials")
                
                try:
                    income = YFinanceUtils.get_income_stmt(ticker)
                    if income is not None and not income.empty:
                        st.dataframe(income.head(10), use_container_width=True)
                except:
                    st.info("Financial data not available")
                
                # News
                st.markdown("### 📰 Latest News")
                try:
                    end_date = datetime.now().strftime("%Y-%m-%d")
                    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                    news = FinnHubUtils.get_company_news(ticker, start_date, end_date, max_news_num=5)
                    
                    for _, article in news.iterrows():
                        st.markdown(f"**{article['headline']}**")
                        st.caption(f"Source: {article.get('source', 'Unknown')}")
                        st.markdown("---")
                except:
                    st.info("News not available")
                    
            except Exception as e:
                st.error(f"Error analyzing {ticker}: {str(e)}")

# AI Chat
elif page == "🤖 AI Chat":
    st.markdown("### 🤖 Chat with AI Financial Analyst")
    
    if not st.session_state.api_configured and not os.environ.get('OPENAI_API_KEY'):
        st.warning("⚠️ Please configure your OpenAI API key in the sidebar first.")
    else:
        # Chat interface
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        if prompt := st.chat_input("Ask about stocks, markets, or investments..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Simple response for now
                        # In production, this would use the full agent
                        from finrobot.data_source import YFinanceUtils
                        
                        # Check if asking about a specific stock
                        import re
                        ticker_match = re.search(r'\b([A-Z]{1,5})\b', prompt.upper())
                        
                        if ticker_match and any(word in prompt.lower() for word in ['price', 'stock', 'analyze', 'tell me about']):
                            ticker = ticker_match.group(1)
                            try:
                                info = YFinanceUtils.get_stock_info(ticker)
                                response = f"""Here's what I found about **{ticker}**:

- **Company**: {info.get('longName', 'N/A')}
- **Current Price**: ${info.get('currentPrice', 0):.2f}
- **Market Cap**: ${info.get('marketCap', 0)/1e12:.2f}T
- **PE Ratio**: {info.get('trailingPE', 0):.1f}
- **52-Week Range**: ${info.get('fiftyTwoWeekLow', 0):.2f} - ${info.get('fiftyTwoWeekHigh', 0):.2f}

{info.get('longBusinessSummary', '')[:300]}..."""
                            except:
                                response = f"I couldn't find data for {ticker}. Please check the ticker symbol."
                        else:
                            response = """I'm your AI Financial Analyst! I can help you with:

📊 **Stock Analysis** - Ask about any stock (e.g., "Tell me about AAPL")
📈 **Market Data** - Get current prices and metrics
📰 **News** - Latest financial news
💡 **Investment Ideas** - General market insights

Try asking: "What's the price of NVDA?" or "Analyze MSFT for me" """
                        
                        st.write(response)
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Charts
elif page == "📈 Charts":
    st.markdown("### 📈 Stock Charts")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        ticker = st.text_input("Ticker Symbol", value="AAPL").upper()
    with col2:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=90))
    with col3:
        end_date = st.date_input("End Date", datetime.now())
    
    if st.button("📈 Generate Chart"):
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
                    # Handle multi-index columns from newer yfinance
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                    
                    # Create chart
                    fig, ax = plt.subplots(figsize=(12, 6))
                    mpf.plot(data, type='candle', style='yahoo', 
                             title=f'{ticker} Stock Price', 
                             ylabel='Price ($)',
                             volume=True,
                             ax=ax,
                             savefig='temp_chart.png')
                    
                    st.image('temp_chart.png')
                    
                    # Show data table
                    st.markdown("### 📊 Data")
                    st.dataframe(data.tail(10), use_container_width=True)
                else:
                    st.error("No data available for this ticker/date range")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Backtesting
elif page == "📉 Backtesting":
    st.markdown("### 📉 Strategy Backtesting")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Ticker", value="AAPL").upper()
        strategy = st.selectbox("Strategy", ["SMA Crossover", "RSI", "MACD"])
        start_date = st.date_input("Start", datetime(2024, 1, 1))
    
    with col2:
        initial_cash = st.number_input("Initial Cash ($)", value=100000, step=10000)
        position_size = st.number_input("Position Size", value=100, step=10)
        end_date = st.date_input("End", datetime(2024, 6, 30))
    
    if st.button("🚀 Run Backtest"):
        with st.spinner("Running backtest..."):
            try:
                from finrobot.functional.quantitative import BackTraderUtils
                
                result = BackTraderUtils.back_test(
                    ticker_symbol=ticker,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    strategy="SMA_CrossOver",
                    strategy_params='{"fast": 10, "slow": 30}',
                    sizer=position_size,
                    cash=float(initial_cash),
                )
                
                st.success("Backtest Complete!")
                st.code(result)
                
            except Exception as e:
                st.error(f"Backtest error: {str(e)}")

# Reports
elif page == "📄 Reports":
    st.markdown("### 📄 Generate Research Report")
    
    ticker = st.text_input("Company Ticker", value="AAPL").upper()
    
    report_type = st.selectbox("Report Type", [
        "Quick Summary",
        "Full Equity Research",
        "Technical Analysis",
        "Competitor Comparison"
    ])
    
    if st.button("📝 Generate Report"):
        with st.spinner(f"Generating {report_type} for {ticker}..."):
            try:
                from finrobot.data_source import YFinanceUtils
                
                info = YFinanceUtils.get_stock_info(ticker)
                
                # Generate report content
                report = f"""
# {info.get('longName', ticker)} ({ticker})
## Equity Research Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

### Key Metrics

| Metric | Value |
|--------|-------|
| Current Price | ${info.get('currentPrice', 0):.2f} |
| Market Cap | ${info.get('marketCap', 0)/1e12:.2f}T |
| PE Ratio | {info.get('trailingPE', 0):.1f} |
| Forward PE | {info.get('forwardPE', 0):.1f} |
| PEG Ratio | {info.get('pegRatio', 0):.2f} |
| Dividend Yield | {info.get('dividendYield', 0)*100:.2f}% |
| 52-Week High | ${info.get('fiftyTwoWeekHigh', 0):.2f} |
| 52-Week Low | ${info.get('fiftyTwoWeekLow', 0):.2f} |
| Beta | {info.get('beta', 0):.2f} |

---

### Business Description

{info.get('longBusinessSummary', 'No description available.')}

---

### Investment Thesis

Based on the current metrics, {ticker} shows:
- {'Strong' if info.get('trailingPE', 100) < 25 else 'Elevated'} valuation with PE of {info.get('trailingPE', 0):.1f}
- Market leadership position with ${info.get('marketCap', 0)/1e12:.2f}T market cap
- {'Attractive' if info.get('dividendYield', 0) > 0.02 else 'Low'} dividend yield

---

*Report generated by FinRobot AI*
"""
                
                st.markdown(report)
                
                # Download button
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"{ticker}_report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 FinRobot AI | Powered by AutoGen & OpenAI</p>
    <p style="font-size: 0.8rem;">Built for CapGlobal</p>
</div>
""", unsafe_allow_html=True)

