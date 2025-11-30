#!/usr/bin/env python3
"""
FinRobot - AI Financial Analysis Platform
Entry point for Replit deployment
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check and install required packages"""
    required = [
        'streamlit',
        'pyautogen',
        'yfinance',
        'finnhub-python',
        'mplfinance',
        'reportlab',
        'pandas',
        'matplotlib',
    ]
    
    import subprocess
    for package in required:
        try:
            __import__(package.replace('-', '_').split('==')[0])
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])

def main():
    """Main entry point"""
    print("🤖 FinRobot - AI Financial Analysis Platform")
    print("=" * 50)
    
    # Check for Streamlit mode
    if '--streamlit' in sys.argv or os.environ.get('RUN_STREAMLIT'):
        import subprocess
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'app.py', 
            '--server.port=8501',
            '--server.address=0.0.0.0',
            '--server.headless=true'
        ])
    else:
        # Run quick demo
        run_demo()

def run_demo():
    """Run a quick demo of FinRobot capabilities"""
    print("\n📊 Running FinRobot Demo...\n")
    
    # Check API keys
    from finrobot.utils import register_keys_from_json
    
    # Try to load from environment variables first (Replit Secrets)
    if os.environ.get('OPENAI_API_KEY'):
        print("✅ API keys loaded from environment")
    elif os.path.exists('config_api_keys'):
        register_keys_from_json('config_api_keys')
        print("✅ API keys loaded from config file")
    else:
        print("⚠️  No API keys found. Set them in Replit Secrets!")
        print("   Required: OPENAI_API_KEY, FINNHUB_API_KEY")
        return
    
    # Demo: Get stock data
    print("\n📈 Fetching stock data...")
    from finrobot.data_source import YFinanceUtils
    
    stocks = ["AAPL", "MSFT", "GOOGL"]
    for ticker in stocks:
        try:
            info = YFinanceUtils.get_stock_info(ticker)
            price = info.get('currentPrice', 'N/A')
            mcap = info.get('marketCap', 0) / 1e12
            print(f"   {ticker}: ${price:.2f} | Market Cap: ${mcap:.2f}T")
        except Exception as e:
            print(f"   {ticker}: Error - {e}")
    
    print("\n✅ Demo complete!")
    print("\n💡 To run the web interface:")
    print("   python main.py --streamlit")
    print("   Or set RUN_STREAMLIT=1 in environment")

if __name__ == "__main__":
    check_dependencies()
    main()

