#!/usr/bin/env python3
"""
FinRobot Quick Start - Market Forecaster Demo
This script demonstrates the simplest use case: predicting stock movement.
"""

import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

def main():
    print("=" * 60)
    print("  🚀 FinRobot Quick Start - Market Forecaster")
    print("=" * 60)
    
    # Get stock ticker from user or use default
    ticker = input("\nEnter stock ticker (default: NVDA): ").strip().upper() or "NVDA"
    
    print(f"\n📊 Analyzing {ticker}...")
    print("This will use GPT-4 to analyze company data and predict stock movement.\n")
    
    import autogen
    from finrobot.utils import get_current_date, register_keys_from_json
    from finrobot.agents.workflow import SingleAssistant
    
    # Load configuration
    llm_config = {
        "config_list": autogen.config_list_from_json(
            str(PROJECT_ROOT / "OAI_CONFIG_LIST"),
            filter_dict={"model": ["gpt-4-0125-preview", "gpt-4-turbo", "gpt-4o"]},
        ),
        "timeout": 120,
        "temperature": 0,
    }
    
    # Register API keys
    register_keys_from_json(str(PROJECT_ROOT / "config_api_keys"))
    
    # Create Market Analyst agent
    assistant = SingleAssistant(
        "Market_Analyst",
        llm_config,
        human_input_mode="NEVER",
    )
    
    # Run analysis
    today = get_current_date()
    assistant.chat(
        f"""Use all the tools provided to retrieve information available for {ticker} 
        upon {today}. 
        
        Analyze the positive developments and potential concerns of {ticker} 
        with 2-4 most important factors respectively and keep them concise. 
        Most factors should be inferred from company related news.
        
        Then make a rough prediction (e.g. up/down by 2-3%) of the {ticker} 
        stock price movement for next week. 
        
        Provide a summary analysis to support your prediction."""
    )
    
    print("\n" + "=" * 60)
    print("  ✅ Analysis Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

