#!/usr/bin/env python3
"""
FinRobot Complete Feature Demonstration
Tests and demonstrates all available features
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

def print_header(text, char="="):
    width = 70
    print(f"\n{char * width}")
    print(f"  {text}")
    print(f"{char * width}\n")

def print_section(text):
    print(f"\n{'─' * 50}")
    print(f"  📌 {text}")
    print(f"{'─' * 50}")

def main():
    from finrobot.utils import register_keys_from_json, get_current_date
    register_keys_from_json("config_api_keys")
    
    print_header("🚀 FINROBOT COMPLETE FEATURE DEMONSTRATION", "🤖")
    print(f"Date: {get_current_date()}")
    
    results = {}
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 1: Data Sources
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 1: Data Source Integrations")
    
    # 1.1 YFinance
    print_section("1.1 YFinance - Stock Data")
    try:
        from finrobot.data_source import YFinanceUtils
        
        # Stock data
        data = YFinanceUtils.get_stock_data("AAPL", "2025-11-01", "2025-11-15")
        print(f"✅ Stock Data: Retrieved {len(data)} days for AAPL")
        print(f"   Latest close: ${data['Close'].iloc[-1]:.2f}")
        
        # Company info
        info = YFinanceUtils.get_stock_info("AAPL")
        print(f"✅ Company Info: {info.get('shortName')} - Market Cap: ${info.get('marketCap', 0)/1e12:.2f}T")
        
        # Income statement
        income = YFinanceUtils.get_income_stmt("AAPL")
        print(f"✅ Income Statement: {income.shape[0]} line items, {income.shape[1]} periods")
        
        # Balance sheet
        balance = YFinanceUtils.get_balance_sheet("AAPL")
        print(f"✅ Balance Sheet: {balance.shape[0]} line items")
        
        # Cash flow
        cashflow = YFinanceUtils.get_cash_flow("AAPL")
        print(f"✅ Cash Flow: {cashflow.shape[0]} line items")
        
        # Analyst recommendations
        rec, votes = YFinanceUtils.get_analyst_recommendations("AAPL")
        print(f"✅ Analyst Recommendation: {rec} ({votes} votes)")
        
        results["YFinance"] = "✅ PASS"
    except Exception as e:
        print(f"❌ YFinance Error: {e}")
        results["YFinance"] = "❌ FAIL"
    
    # 1.2 Finnhub
    print_section("1.2 Finnhub - Company Data & News")
    try:
        from finrobot.data_source import FinnHubUtils
        
        # Company profile
        profile = FinnHubUtils.get_company_profile("NVDA")
        print(f"✅ Company Profile: Retrieved for NVDA")
        print(f"   Preview: {profile[:100]}...")
        
        # Company news
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        news = FinnHubUtils.get_company_news("NVDA", start_date, end_date, max_news_num=5)
        print(f"✅ Company News: Retrieved {len(news)} articles")
        if len(news) > 0:
            print(f"   Latest: {news['headline'].iloc[0][:60]}...")
        
        # Basic financials
        financials = FinnHubUtils.get_basic_financials("NVDA")
        print(f"✅ Basic Financials: Retrieved metrics")
        
        results["Finnhub"] = "✅ PASS"
    except Exception as e:
        print(f"❌ Finnhub Error: {e}")
        results["Finnhub"] = "❌ FAIL"
    
    # 1.3 SEC-API
    print_section("1.3 SEC-API - 10-K Filings")
    try:
        from finrobot.data_source import SECUtils
        
        # Get 10-K metadata
        metadata = SECUtils.get_10k_metadata("AAPL", "2024-01-01", "2024-12-31")
        if metadata:
            print(f"✅ 10-K Metadata: Found filing from {metadata.get('filedAt', 'N/A')[:10]}")
        
        # Get 10-K section
        section1 = SECUtils.get_10k_section("MSFT", "2023", "1")
        print(f"✅ 10-K Section 1 (Business): Retrieved {len(section1)} characters")
        print(f"   Preview: {section1[:150]}...")
        
        section1a = SECUtils.get_10k_section("MSFT", "2023", "1A")
        print(f"✅ 10-K Section 1A (Risk Factors): Retrieved {len(section1a)} characters")
        
        results["SEC-API"] = "✅ PASS"
    except Exception as e:
        print(f"❌ SEC-API Error: {e}")
        results["SEC-API"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 2: Charting Utilities
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 2: Charting & Visualization")
    
    print_section("2.1 Stock Price Charts")
    try:
        from finrobot.functional.charting import MplFinanceUtils, ReportChartUtils
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        
        os.makedirs("demo_output", exist_ok=True)
        
        # Candlestick chart
        result = MplFinanceUtils.plot_stock_price_chart(
            "AAPL", "2025-10-01", "2025-11-15",
            save_path="demo_output/aapl_candle.png",
            type="candle",
            style="yahoo"
        )
        print(f"✅ Candlestick Chart: {result}")
        
        # Share performance vs S&P 500
        result = ReportChartUtils.get_share_performance(
            "GOOGL", "2025-11-15", "demo_output"
        )
        print(f"✅ Share Performance Chart: {result}")
        
        # PE/EPS chart
        result = ReportChartUtils.get_pe_eps_performance(
            "GOOGL", "2025-11-15", years=4, save_path="demo_output"
        )
        print(f"✅ PE/EPS Performance Chart: {result}")
        
        results["Charting"] = "✅ PASS"
    except Exception as e:
        print(f"❌ Charting Error: {e}")
        results["Charting"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 3: Financial Analysis Utilities
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 3: Financial Analysis Tools")
    
    print_section("3.1 Report Analysis Utilities")
    try:
        from finrobot.functional.analyzer import ReportAnalysisUtils
        
        # Get key data
        key_data = ReportAnalysisUtils.get_key_data("AAPL", "2024-10-31")
        print(f"✅ Key Financial Data:")
        for key, value in key_data.items():
            print(f"   {key}: {value}")
        
        results["Analysis Utils"] = "✅ PASS"
    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        results["Analysis Utils"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 4: PDF Report Generation
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 4: PDF Report Generation")
    
    print_section("4.1 Equity Research Report Builder")
    try:
        from reportlab.lib import colors, pagesizes
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_JUSTIFY
        
        pdf_path = "demo_output/GOOGL_Demo_Report.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=pagesizes.A4)
        styles = getSampleStyleSheet()
        
        content = []
        content.append(Paragraph("Alphabet Inc. (GOOGL) - Equity Research", styles['Title']))
        content.append(Paragraph("FinRobot AI-Generated Report", styles['Normal']))
        content.append(Spacer(1, 20))
        
        # Add key metrics
        info = YFinanceUtils.get_stock_info("GOOGL")
        data = [
            ["Metric", "Value"],
            ["Market Cap", f"${info.get('marketCap', 0)/1e12:.2f}T"],
            ["Current Price", f"${info.get('currentPrice', 0):.2f}"],
            ["PE Ratio", f"{info.get('trailingPE', 0):.1f}"],
            ["52-Week High", f"${info.get('fiftyTwoWeekHigh', 0):.2f}"],
            ["52-Week Low", f"${info.get('fiftyTwoWeekLow', 0):.2f}"],
        ]
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        content.append(table)
        content.append(Spacer(1, 20))
        
        body_style = ParagraphStyle('Body', parent=styles['Normal'], alignment=TA_JUSTIFY)
        content.append(Paragraph("<b>Company Overview</b>", styles['Heading2']))
        content.append(Paragraph("""Alphabet Inc. is a multinational technology conglomerate 
        headquartered in Mountain View, California. The company is the parent of Google, 
        one of the world's most valuable brands. Alphabet's business spans search, 
        advertising, cloud computing, and emerging technologies including AI, 
        autonomous vehicles (Waymo), and life sciences (Verily).""", body_style))
        
        doc.build(content)
        print(f"✅ PDF Report Generated: {pdf_path}")
        print(f"   Size: {os.path.getsize(pdf_path)/1024:.1f} KB")
        
        results["PDF Generation"] = "✅ PASS"
    except Exception as e:
        print(f"❌ PDF Generation Error: {e}")
        results["PDF Generation"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 5: Backtesting with BackTrader
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 5: Backtesting Engine")
    
    print_section("5.1 SMA Crossover Strategy Backtest")
    try:
        from finrobot.functional.quantitative import BackTraderUtils
        import matplotlib
        matplotlib.use('Agg')
        
        result = BackTraderUtils.back_test(
            ticker_symbol="AAPL",
            start_date="2024-01-01",
            end_date="2024-06-30",
            strategy="SMA_CrossOver",
            strategy_params='{"fast": 10, "slow": 30}',
            sizer=100,
            cash=100000.0,
            save_fig="demo_output/backtest_result.png"
        )
        print(f"✅ Backtest Complete:")
        # Parse key results
        lines = result.split('\n')
        for line in lines[:10]:
            if line.strip():
                print(f"   {line.strip()}")
        
        results["Backtesting"] = "✅ PASS"
    except Exception as e:
        print(f"❌ Backtesting Error: {e}")
        results["Backtesting"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 6: AI Agents
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 6: AI Agent Workflows")
    
    print_section("6.1 Single Agent - Market Analyst")
    try:
        import autogen
        from finrobot.agents.workflow import SingleAssistant
        
        llm_config = {
            "config_list": autogen.config_list_from_json("OAI_CONFIG_LIST"),
            "timeout": 120,
            "temperature": 0,
        }
        
        assistant = SingleAssistant(
            "Market_Analyst",
            llm_config,
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
        )
        
        print("✅ Market Analyst Agent: Created successfully")
        print("   Tools available:")
        print("   - get_company_profile (Finnhub)")
        print("   - get_company_news (Finnhub)")
        print("   - get_basic_financials (Finnhub)")
        print("   - get_stock_data (YFinance)")
        
        results["AI Agents"] = "✅ PASS"
    except Exception as e:
        print(f"❌ AI Agents Error: {e}")
        results["AI Agents"] = "❌ FAIL"
    
    print_section("6.2 Multi-Agent Team Structure")
    try:
        from finrobot.agents.workflow import MultiAssistantWithLeader
        
        group_config = {
            "leader": {
                "title": "Portfolio Manager",
                "responsibilities": ["Coordinate analysis", "Make final decisions"],
            },
            "agents": [
                {"title": "Sentiment Analyst", "responsibilities": ["Analyze news sentiment"]},
                {"title": "Technical Analyst", "responsibilities": ["Analyze price patterns"]},
                {"title": "Fundamental Analyst", "responsibilities": ["Analyze financials"]},
            ],
        }
        
        team = MultiAssistantWithLeader(group_config, llm_config=llm_config)
        print("✅ Multi-Agent Team: Created successfully")
        print(f"   Leader: Portfolio Manager")
        print(f"   Team Members: {len(group_config['agents'])} analysts")
        
        results["Multi-Agent"] = "✅ PASS"
    except Exception as e:
        print(f"❌ Multi-Agent Error: {e}")
        results["Multi-Agent"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 7: RAG (Retrieval Augmented Generation)
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 7: RAG for Document Q&A")
    
    print_section("7.1 RAG Function Setup")
    try:
        from finrobot.functional.rag import get_rag_function
        
        retrieve_config = {
            "task": "qa",
            "docs_path": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm",
            "chunk_token_size": 1000,
            "collection_name": "demo_collection",
            "get_or_create": True,
        }
        
        rag_func, rag_assistant = get_rag_function(
            retrieve_config, 
            description="Retrieve content from Apple's 10-K for Q&A"
        )
        print("✅ RAG Function: Created successfully")
        print(f"   Document: Apple 10-K FY2024")
        print(f"   Chunk size: 1000 tokens")
        
        results["RAG"] = "✅ PASS"
    except Exception as e:
        print(f"❌ RAG Error: {e}")
        results["RAG"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # FEATURE 8: Text & Coding Utilities
    # ═══════════════════════════════════════════════════════════════
    print_header("FEATURE 8: Utility Functions")
    
    print_section("8.1 Text Utilities")
    try:
        from finrobot.functional.text import TextUtils
        
        sample_text = "This is a sample text for testing the length check functionality."
        result = TextUtils.check_text_length(sample_text, min_length=5, max_length=100)
        print(f"✅ Text Length Check: {result}")
        
        results["Text Utils"] = "✅ PASS"
    except Exception as e:
        print(f"❌ Text Utils Error: {e}")
        results["Text Utils"] = "❌ FAIL"
    
    print_section("8.2 Coding Utilities")
    try:
        from finrobot.functional.coding import CodingUtils
        
        # Create a test file
        os.makedirs("demo_output/code_test", exist_ok=True)
        CodingUtils.create_file_with_code(
            "../demo_output/code_test/test.py",
            "# Test file\nprint('Hello from FinRobot!')"
        )
        print("✅ File Creation: demo_output/code_test/test.py created")
        
        # List directory
        files = CodingUtils.list_dir("../demo_output/code_test")
        print(f"✅ Directory Listing: {files}")
        
        results["Coding Utils"] = "✅ PASS"
    except Exception as e:
        print(f"❌ Coding Utils Error: {e}")
        results["Coding Utils"] = "❌ FAIL"
    
    # ═══════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════
    print_header("📊 FEATURE TEST SUMMARY", "═")
    
    passed = sum(1 for v in results.values() if "PASS" in v)
    total = len(results)
    
    print(f"\n{'Feature':<25} {'Status':<15}")
    print("-" * 40)
    for feature, status in results.items():
        print(f"{feature:<25} {status:<15}")
    
    print("-" * 40)
    print(f"\n🎯 Results: {passed}/{total} features working")
    
    if passed == total:
        print("\n🎉 ALL FEATURES OPERATIONAL!")
    else:
        print(f"\n⚠️  {total - passed} feature(s) need attention")
    
    # List generated files
    print_header("📁 Generated Demo Files")
    if os.path.exists("demo_output"):
        for root, dirs, files in os.walk("demo_output"):
            for f in files:
                filepath = os.path.join(root, f)
                size = os.path.getsize(filepath) / 1024
                print(f"   📄 {filepath} ({size:.1f} KB)")
    
    print("\n" + "🤖" * 35)
    print("  FinRobot Feature Demo Complete!")
    print("🤖" * 35 + "\n")

if __name__ == "__main__":
    main()

