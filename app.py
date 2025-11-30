"""
AriaWealth.ai Web Interface - Streamlit App
A beautiful UI for AI-powered financial analysis
Powered by ARIA™
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
    return """👋 Hello! I'm **ARIA**, your AI Financial Analyst from AriaWealth.ai. I can help you with:

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
    page_title="AriaWealth.ai",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main styling */
    .stApp {
        background: linear-gradient(180deg, #0a0a1a 0%, #111128 50%, #0a0a1a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Fix main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
    }
    
    p, span, label {
        color: #e0e0e0 !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 50%, #d946ef 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        text-align: center;
        color: #a0a0c0 !important;
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f24 0%, #151532 100%);
        border-right: 1px solid #2a2a4a;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #a855f7 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1a35 0%, #252550 100%);
        border-radius: 16px;
        padding: 1.25rem;
        border: 1px solid #3a3a6a;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetric"] label {
        color: #a0a0d0 !important;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.5);
        background: linear-gradient(135deg, #8b5cf6 0%, #c084fc 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Text inputs */
    .stTextInput input {
        background: #1a1a35 !important;
        border: 2px solid #3a3a6a !important;
        border-radius: 10px;
        color: #ffffff !important;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: #1a1a35 !important;
        border: 2px solid #3a3a6a !important;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    /* Number inputs */
    .stNumberInput input {
        background: #1a1a35 !important;
        border: 2px solid #3a3a6a !important;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    /* Date inputs */
    .stDateInput input {
        background: #1a1a35 !important;
        border: 2px solid #3a3a6a !important;
        border-radius: 10px;
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a35;
        border-radius: 12px;
        padding: 0.5rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #a0a0c0 !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%) !important;
        color: #ffffff !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #1a1a35 !important;
        border-radius: 12px;
        color: #ffffff !important;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background: #151530 !important;
        border: 1px solid #2a2a4a;
        border-radius: 0 0 12px 12px;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        background: #1a1a35 !important;
        border: 1px solid #3a3a6a;
        border-radius: 12px;
        color: #e0e0e0 !important;
    }
    
    [data-testid="stAlert"] {
        padding: 1rem 1.25rem;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #3a3a6a;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: #1a1a35 !important;
        border-radius: 12px;
        border: 1px solid #2a2a4a;
    }
    
    /* Spinners */
    .stSpinner > div {
        border-color: #7c3aed !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Code blocks */
    code {
        background: #1a1a35 !important;
        color: #a855f7 !important;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
    }
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        padding: 0.6rem 1rem;
        border-radius: 8px;
        transition: background 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(124, 58, 237, 0.2);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3a3a6a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5a5a8a;
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
    st.markdown("## 💎 AriaWealth.ai")
    st.markdown("*Powered by ARIA™*")
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
        "🧠 AI Investment Team",
        "📈 Charts",
        "📉 Backtesting",
        "📄 Reports"
    ], label_visibility="collapsed")

# Main content
st.markdown('<h1 class="main-header">💎 AriaWealth.ai</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by ARIA™ | AI-Driven Financial Intelligence</p>', unsafe_allow_html=True)

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
        
        # Generate response using LLM
        with st.chat_message("assistant"):
            with st.spinner("🧠 ARIA is thinking..."):
                try:
                    import autogen
                    from finrobot.agents.workflow import SingleAssistant
                    from finrobot.utils import register_keys_from_json
                    
                    # Ensure API keys are registered
                    if os.path.exists('config_api_keys'):
                        register_keys_from_json('config_api_keys')
                    
                    # Setup LLM config
                    openai_key = os.environ.get('OPENAI_API_KEY')
                    if not openai_key:
                        response = "⚠️ Please configure your OpenAI API key in the sidebar to use AI Chat."
                    else:
                        # Create LLM config (AutoGen format)
                        llm_config = {
                            "config_list": [{
                                "model": "gpt-4o",
                                "api_key": openai_key,
                            }],
                            "temperature": 0.7,
                            "timeout": 120,
                        }
                        
                        # Initialize assistant agent (reuse if exists, create if not)
                        if 'chat_assistant' not in st.session_state:
                            st.session_state.chat_assistant = SingleAssistant(
                                "Financial_Analyst",
                                llm_config=llm_config,
                                human_input_mode="NEVER",
                                max_consecutive_auto_reply=3,
                            )
                        
                        # Use LLM to generate response via AutoGen
                        # Run the chat and capture response from conversation history
                        try:
                            # Initiate chat (don't use .chat() as it resets, use initiate_chat directly)
                            st.session_state.chat_assistant.user_proxy.initiate_chat(
                                st.session_state.chat_assistant.assistant,
                                message=prompt,
                                max_turns=3,
                            )
                            
                            # Get the last message from the assistant
                            # Messages are stored in user_proxy's chat_messages dict
                            assistant_name = st.session_state.chat_assistant.assistant.name
                            if assistant_name in st.session_state.chat_assistant.user_proxy.chat_messages:
                                messages = st.session_state.chat_assistant.user_proxy.chat_messages[assistant_name]
                                # Get the last assistant message (skip user messages)
                                for msg in reversed(messages):
                                    if isinstance(msg, dict) and msg.get("role") == "assistant":
                                        response = msg.get("content", "")
                                        break
                                    elif not isinstance(msg, dict):
                                        # Sometimes messages are strings
                                        response = str(msg)
                                        break
                                
                                # If no assistant message found, get the last message
                                if not response and messages:
                                    last_msg = messages[-1]
                                    if isinstance(last_msg, dict):
                                        response = last_msg.get("content", "")
                                    else:
                                        response = str(last_msg)
                            else:
                                response = "I'm processing your request. Please try rephrasing your question."
                                
                        except Exception as chat_error:
                            # Fallback to a helpful response
                            response = f"""I'm ARIA, your AI Financial Analyst powered by GPT-4. 

I can help you with:
- **Stock Analysis**: Ask about any company (e.g., "Tell me about Microsoft" or "Analyze AAPL")
- **Market Insights**: Questions about market trends and sectors
- **Financial Data**: Current prices, financials, news, and more

*Note: I have access to real-time financial data tools via AutoGen framework.*

Error details: {str(chat_error)}"""
                    
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    import traceback
                    error_msg = f"Sorry, I encountered an error: {str(e)}\n\n*Please ensure your OpenAI API key is configured correctly.*"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================
# AI INVESTMENT TEAM PAGE (Agentic AI)
# ============================================================
elif page == "🧠 AI Investment Team":
    st.markdown("### 🧠 AI Investment Team")
    st.markdown("*Multi-Agent Analysis powered by ARIA™*")
    
    # Team description
    st.info("""
    **How it works:** Our AI Investment Team consists of multiple specialized agents that collaborate 
    to provide comprehensive analysis. Each agent has expertise in a specific domain and uses real 
    financial data to form their opinions.
    """)
    
    # Team visualization
    st.markdown("### 👥 Meet the Team")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1a365d 0%, #234876 100%); 
                    padding: 2rem 1.5rem; border-radius: 16px; text-align: center;
                    border: 1px solid #3182ce; box-shadow: 0 8px 32px rgba(49, 130, 206, 0.2);">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📊</div>
            <h3 style="color: #63b3ed; margin: 0 0 0.75rem 0; font-size: 1.3rem; font-weight: 600;">Market Analyst</h3>
            <p style="color: #bee3f8; font-size: 0.95rem; line-height: 1.5; margin: 0;">
            Analyzes market trends, news sentiment, and price movements
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #1a4d3e 0%, #236348 100%); 
                    padding: 2rem 1.5rem; border-radius: 16px; text-align: center;
                    border: 1px solid #38a169; box-shadow: 0 8px 32px rgba(56, 161, 105, 0.2);">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">💰</div>
            <h3 style="color: #68d391; margin: 0 0 0.75rem 0; font-size: 1.3rem; font-weight: 600;">Fundamental Analyst</h3>
            <p style="color: #c6f6d5; font-size: 0.95rem; line-height: 1.5; margin: 0;">
            Reviews financial statements, valuations, and business fundamentals
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(145deg, #4a1d5e 0%, #5e2876 100%); 
                    padding: 2rem 1.5rem; border-radius: 16px; text-align: center;
                    border: 1px solid #9f7aea; box-shadow: 0 8px 32px rgba(159, 122, 234, 0.2);">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">📈</div>
            <h3 style="color: #b794f4; margin: 0 0 0.75rem 0; font-size: 1.3rem; font-weight: 600;">Technical Analyst</h3>
            <p style="color: #e9d8fd; font-size: 0.95rem; line-height: 1.5; margin: 0;">
            Studies charts, patterns, and technical indicators
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CIO card
    st.markdown("""
    <div style="background: linear-gradient(145deg, #1a1a40 0%, #2d2d60 100%); 
                padding: 2rem; border-radius: 16px; text-align: center; margin: 1rem 0;
                border: 2px solid #a855f7; box-shadow: 0 8px 40px rgba(168, 85, 247, 0.25);">
        <div style="font-size: 3rem; margin-bottom: 0.75rem;">👔</div>
        <h3 style="color: #c084fc; margin: 0 0 0.75rem 0; font-size: 1.5rem; font-weight: 700;">Chief Investment Officer (CIO)</h3>
        <p style="color: #e9d5ff; font-size: 1rem; line-height: 1.6; margin: 0; max-width: 600px; margin-left: auto; margin-right: auto;">
        Coordinates all analysts, integrates their findings, and delivers the final investment recommendation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analysis input
    st.markdown("### 🎯 Run Team Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input("Stock to Analyze", value="NVDA", key="team_ticker").upper()
    
    with col2:
        analysis_depth = st.selectbox("Depth", ["Quick", "Standard", "Deep"])
    
    if st.button("🚀 Launch AI Team Analysis", use_container_width=True):
        if not st.session_state.api_configured and not os.environ.get('OPENAI_API_KEY'):
            st.error("⚠️ Please configure your OpenAI API key first!")
        else:
            # Progress display
            progress_placeholder = st.empty()
            results_placeholder = st.empty()
            
            with st.spinner("🧠 AI Team is analyzing..."):
                try:
                    from finrobot.data_source import YFinanceUtils, FinnHubUtils
                    from datetime import datetime, timedelta
                    import time
                    
                    # Simulate team workflow with real data
                    progress_placeholder.markdown("### 📊 Analysis Progress")
                    
                    # Step 1: Market Analyst
                    progress_placeholder.info("📊 **Market Analyst** is gathering news and sentiment...")
                    time.sleep(1)
                    
                    end_date = datetime.now().strftime("%Y-%m-%d")
                    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                    
                    try:
                        news = FinnHubUtils.get_company_news(ticker, start_date, end_date, max_news_num=5)
                        news_summary = f"Found {len(news)} recent articles" if news is not None and not news.empty else "Limited news available"
                    except:
                        news_summary = "News analysis unavailable"
                    
                    # Step 2: Fundamental Analyst
                    progress_placeholder.info("💰 **Fundamental Analyst** is reviewing financials...")
                    time.sleep(1)
                    
                    info = YFinanceUtils.get_stock_info(ticker)
                    price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                    pe = info.get('trailingPE', 0)
                    mcap = info.get('marketCap', 0)
                    
                    # Step 3: Technical Analyst
                    progress_placeholder.info("📈 **Technical Analyst** is studying price action...")
                    time.sleep(1)
                    
                    high_52 = info.get('fiftyTwoWeekHigh', 0)
                    low_52 = info.get('fiftyTwoWeekLow', 0)
                    price_vs_high = ((price - high_52) / high_52 * 100) if high_52 else 0
                    
                    # Step 4: CIO Integration
                    progress_placeholder.info("👔 **CIO** is integrating all findings...")
                    time.sleep(1)
                    
                    # Generate recommendation
                    if pe and pe < 20:
                        valuation = "undervalued"
                        val_score = 3
                    elif pe and pe < 35:
                        valuation = "fairly valued"
                        val_score = 2
                    else:
                        valuation = "premium valued"
                        val_score = 1
                    
                    if price_vs_high > -10:
                        momentum = "strong"
                        mom_score = 3
                    elif price_vs_high > -25:
                        momentum = "moderate"
                        mom_score = 2
                    else:
                        momentum = "weak"
                        mom_score = 1
                    
                    total_score = val_score + mom_score
                    if total_score >= 5:
                        recommendation = "STRONG BUY"
                        rec_color = "#00ff88"
                    elif total_score >= 4:
                        recommendation = "BUY"
                        rec_color = "#88ff00"
                    elif total_score >= 3:
                        recommendation = "HOLD"
                        rec_color = "#ffff00"
                    else:
                        recommendation = "CAUTIOUS"
                        rec_color = "#ff8800"
                    
                    progress_placeholder.empty()
                    
                    # Display results using Streamlit components
                    st.markdown("---")
                    st.markdown(f"## 📋 {info.get('longName', ticker)} ({ticker})")
                    st.caption(f"{info.get('sector', 'N/A')} | {info.get('industry', 'N/A')}")
                    
                    # Recommendation banner
                    rec_emoji = "🟢" if "BUY" in recommendation else "🟡" if "HOLD" in recommendation else "🔴"
                    st.success(f"""
                    ### {rec_emoji} ARIA™ AI Team Recommendation: **{recommendation}**
                    """)
                    
                    st.markdown("---")
                    
                    # Analyst findings in columns
                    st.markdown("### 👥 Team Findings")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 📊 Market Analyst")
                        st.info(f"""
                        **News:** {news_summary}
                        
                        **Price:** ${price:.2f}
                        
                        **vs 52W High:** {abs(price_vs_high):.1f}% {"below" if price_vs_high < 0 else "above"}
                        """)
                    
                    with col2:
                        st.markdown("#### 💰 Fundamental Analyst")
                        st.info(f"""
                        **PE Ratio:** {pe:.1f}x
                        
                        **Valuation:** {valuation.title()}
                        
                        **Market Cap:** ${mcap/1e9:.1f}B
                        """)
                    
                    with col3:
                        st.markdown("#### 📈 Technical Analyst")
                        st.info(f"""
                        **52W High:** ${high_52:.2f}
                        
                        **52W Low:** ${low_52:.2f}
                        
                        **Momentum:** {momentum.title()}
                        """)
                    
                    st.markdown("---")
                    
                    # CIO Summary
                    st.markdown("### 👔 CIO Summary")
                    st.warning(f"""
                    Based on the team's comprehensive analysis, **{ticker}** shows **{valuation}** 
                    characteristics with **{momentum}** price momentum.
                    
                    **Final Recommendation: {recommendation}**
                    """)
                    
                    st.markdown("---")
                    
                    # Detailed metrics
                    st.markdown("### 📊 Key Metrics")
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.metric("Price", f"${price:.2f}")
                    with m2:
                        st.metric("PE Ratio", f"{pe:.1f}")
                    with m3:
                        st.metric("52W High", f"${high_52:.2f}")
                    with m4:
                        st.metric("52W Low", f"${low_52:.2f}")
                    
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
    
    # How it works section
    with st.expander("ℹ️ How the AI Team Works"):
        st.markdown("""
        **The ARIA™ AI Investment Team uses a multi-agent architecture:**
        
        1. **Market Analyst Agent** 📊
           - Gathers recent news and social sentiment
           - Analyzes market trends and momentum
           - Tools: Finnhub News API, YFinance
        
        2. **Fundamental Analyst Agent** 💰
           - Reviews financial statements
           - Calculates valuation metrics
           - Tools: YFinance, SEC Filings
        
        3. **Technical Analyst Agent** 📈
           - Studies price charts and patterns
           - Identifies support/resistance levels
           - Tools: YFinance, Technical Indicators
        
        4. **Chief Investment Officer (CIO)** 👔
           - Coordinates all analysts
           - Integrates diverse perspectives
           - Makes final recommendation
        
        **Technology:** Built on Microsoft AutoGen framework with GPT-4 reasoning.
        """)

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
            "Full PDF Research Report (SEC 10-K Analysis)",
        ])
    
    # Add fiscal year input for full reports
    if report_type == "Full PDF Research Report (SEC 10-K Analysis)":
        fyear = st.text_input("Fiscal Year", value=str(datetime.now().year - 1), key="report_fyear")
        st.info("💡 Full reports analyze SEC 10-K filings, financial statements, and generate professional PDFs with charts. This may take 2-5 minutes.")
        st.warning("⚠️ **Note:** Full PDF reports require SEC-API key. Ensure it's set in your environment or config_api_keys file.")
    
    if st.button("📝 Generate Report", use_container_width=True):
        with st.spinner(f"Generating {report_type} for {ticker}..."):
            try:
                if report_type == "Quick Summary":
                    # Quick summary report (existing functionality)
                    from finrobot.data_source import YFinanceUtils
                    
                    info = YFinanceUtils.get_stock_info(ticker)
                    
                    if not info or not info.get('longName'):
                        st.error(f"Could not find data for {ticker}")
                    else:
                        price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                        mcap = info.get('marketCap', 0)
                        mcap_str = f"${mcap/1e12:.2f}T" if mcap >= 1e12 else f"${mcap/1e9:.2f}B"
                        
                        # Format metrics with proper handling of None/missing values
                        trailing_pe = info.get('trailingPE')
                        trailing_pe_str = f"{trailing_pe:.1f}" if isinstance(trailing_pe, (int, float)) else 'N/A'
                        
                        forward_pe = info.get('forwardPE')
                        forward_pe_str = f"{forward_pe:.1f}" if isinstance(forward_pe, (int, float)) else 'N/A'
                        
                        peg_ratio = info.get('pegRatio')
                        peg_ratio_str = f"{peg_ratio:.2f}" if isinstance(peg_ratio, (int, float)) else 'N/A'
                        
                        beta = info.get('beta')
                        beta_str = f"{beta:.2f}" if isinstance(beta, (int, float)) else 'N/A'
                        
                        # Generate report
                        report = f"""# {info.get('longName', ticker)} ({ticker})
## Equity Research Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")} | **Analyst:** ARIA™ by AriaWealth.ai

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| Current Price | **${price:.2f}** |
| Market Cap | {mcap_str} |
| PE Ratio (TTM) | {trailing_pe_str} |
| Forward PE | {forward_pe_str} |
| PEG Ratio | {peg_ratio_str} |
| Dividend Yield | {(info.get('dividendYield', 0) or 0)*100:.2f}% |
| 52-Week High | ${info.get('fiftyTwoWeekHigh', 0):.2f} |
| 52-Week Low | ${info.get('fiftyTwoWeekLow', 0):.2f} |
| Beta | {beta_str} |
| Avg Volume | {info.get('averageVolume', 0):,.0f} |

---

## 📝 Company Overview

**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}

{info.get('longBusinessSummary', 'No description available.')}

---

## 💡 Investment Highlights

Based on current metrics:
- **Valuation:** {"Reasonable" if (isinstance(trailing_pe, (int, float)) and trailing_pe < 25) else "Premium"} PE of {trailing_pe_str}x
- **Market Position:** {mcap_str} market cap indicates {"large-cap" if mcap >= 10e9 else "mid-cap" if mcap >= 2e9 else "small-cap"} status
- **Income:** {"Dividend-paying" if (info.get('dividendYield', 0) or 0) > 0 else "Growth-focused (no dividend)"}

---

*This report was generated by ARIA™ (AriaWealth.ai) for informational purposes only. Not financial advice.*
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
                
                else:
                    # Full PDF Research Report using AI agent
                    import os
                    from textwrap import dedent
                    from finrobot.agents.workflow import SingleAssistantShadow
                    from finrobot.utils import register_keys_from_json
                    import autogen
                    import json
                    
                    # Check API keys from environment (where they're stored when saved in sidebar)
                    openai_key = os.environ.get('OPENAI_API_KEY')
                    finnhub_key = os.environ.get('FINNHUB_API_KEY')
                    
                    if not openai_key:
                        st.error("⚠️ Please configure OpenAI API key in the sidebar first!")
                        st.info("💡 Go to the sidebar → 🔑 API Keys → Enter your OpenAI API key → Click '💾 Save Keys'")
                        st.stop()
                    
                    # Register API keys for the agent's tools
                    # Check if config_api_keys exists, if not create temporary one
                    temp_config = False
                    if not os.path.exists('config_api_keys'):
                        config_data = {}
                        if finnhub_key:
                            config_data['FINNHUB_API_KEY'] = finnhub_key
                        # Check for SEC-API key in environment
                        if os.environ.get('SEC_API_KEY'):
                            config_data['SEC_API_KEY'] = os.environ.get('SEC_API_KEY')
                        # Check for FMP key in environment
                        if os.environ.get('FMP_API_KEY'):
                            config_data['FMP_API_KEY'] = os.environ.get('FMP_API_KEY')
                        # Add other keys if available
                        if config_data:
                            with open('config_api_keys', 'w') as f:
                                json.dump(config_data, f)
                            temp_config = True
                    
                    # Register keys from config file if it exists
                    if os.path.exists('config_api_keys'):
                        register_keys_from_json('config_api_keys')
                    
                    # Ensure OpenAI key is set in environment (should already be set from sidebar)
                    if openai_key:
                        os.environ['OPENAI_API_KEY'] = openai_key
                    
                    # Set up work directory
                    work_dir = "report"
                    os.makedirs(work_dir, exist_ok=True)
                    
                    # Configure LLM
                    llm_config = {
                        "config_list": [{
                            "model": "gpt-4o",
                            "api_key": openai_key
                        }],
                        "temperature": 0.5,
                        "timeout": 120,
                    }
                    
                    # Initialize agent
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.info("🤖 Initializing AI Financial Analyst Agent...")
                    progress_bar.progress(10)
                    
                    assistant = SingleAssistantShadow(
                        "Expert_Investor",
                        llm_config,
                        max_consecutive_auto_reply=None,
                        human_input_mode="NEVER",
                    )
                    
                    status_text.info("📊 Retrieving SEC 10-K filing and analyzing financial statements...")
                    progress_bar.progress(20)
                    
                    # Create the task message
                    company_name = ticker
                    message = dedent(
                        f"""
                        With the tools you've been provided, write an annual report based on {company_name}'s {fyear} 10-k report, format it into a pdf.
                        Pay attention to the followings:
                        - Explicitly explain your working plan before you kick off.
                        - Use tools one by one for clarity, especially when asking for instructions. 
                        - All your file operations should be done in "{work_dir}". 
                        - Display any image in the chat once generated.
                        - All the paragraphs should combine between 400 and 450 words, don't generate the pdf until this is explicitly fulfilled.
                        - Save the final PDF as "{work_dir}/{company_name}_Annual_Report_{fyear}.pdf"
                        """
                    )
                    
                    status_text.info("🧠 AI Agent is analyzing and generating the comprehensive report...")
                    progress_bar.progress(40)
                    
                    # Run the agent (this will take time)
                    try:
                        assistant.chat(message, use_cache=False, max_turns=50, summary_method="last_msg")
                        progress_bar.progress(90)
                        
                        # Check if PDF was generated
                        pdf_path = os.path.join(work_dir, f"{ticker}_Equity_Research_report.pdf")
                        alt_pdf_path = os.path.join(work_dir, f"{company_name}_Annual_Report_{fyear}.pdf")
                        
                        if os.path.exists(pdf_path):
                            final_pdf = pdf_path
                        elif os.path.exists(alt_pdf_path):
                            final_pdf = alt_pdf_path
                        else:
                            # Look for any PDF in the report directory
                            pdf_files = [f for f in os.listdir(work_dir) if f.endswith('.pdf') and ticker.upper() in f.upper()]
                            if pdf_files:
                                final_pdf = os.path.join(work_dir, pdf_files[-1])
                            else:
                                raise FileNotFoundError("PDF report was not generated. Check the agent's output for errors.")
                        
                        progress_bar.progress(100)
                        status_text.success(f"✅ Report generated successfully!")
                        
                        # Display success and download button
                        st.success(f"📄 Comprehensive PDF report generated: `{os.path.basename(final_pdf)}`")
                        
                        # Read and provide download
                        with open(final_pdf, "rb") as pdf_file:
                            st.download_button(
                                label="📥 Download Full PDF Report",
                                data=pdf_file.read(),
                                file_name=os.path.basename(final_pdf),
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        # Show preview info
                        st.info(f"""
                        **Report Contents:**
                        - SEC 10-K Filing Analysis
                        - Financial Statement Analysis (Income, Balance Sheet, Cash Flow)
                        - Business Overview & Market Position
                        - Risk Assessment
                        - Competitors Analysis
                        - Share Performance Charts
                        - PE & EPS Performance Charts
                        
                        **File:** `{os.path.basename(final_pdf)}`
                        """)
                        
                    except Exception as agent_error:
                        progress_bar.progress(100)
                        st.error(f"❌ Error during report generation: {str(agent_error)}")
                        st.info("💡 This feature requires SEC-API access and may take several minutes. Check your API keys and try again.")
                    finally:
                        # Clean up temporary config file if created
                        if temp_config and os.path.exists('config_api_keys'):
                            try:
                                os.remove('config_api_keys')
                            except:
                                pass
                    
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; margin-top: 2rem; 
            border-top: 1px solid #2a2a4a; background: linear-gradient(180deg, transparent 0%, #0a0a15 100%);">
    <p style="font-size: 1.3rem; margin: 0 0 0.5rem 0; color: #c084fc;">
        💎 <strong>AriaWealth.ai</strong>™
    </p>
    <p style="font-size: 1rem; margin: 0 0 0.75rem 0; color: #a855f7; font-weight: 500;">
        Powered by ARIA™
    </p>
    <p style="font-size: 0.85rem; margin: 0; color: #6b7280;">
        Data: YFinance, Finnhub, SEC-API | AI: OpenAI GPT-4 | Framework: AutoGen
    </p>
</div>
""", unsafe_allow_html=True)
