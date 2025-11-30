# FinRobot Implementation Guide

## 📋 Complete Implementation Checklist

---

## 🔴 PHASE 1: Environment Setup (Day 1)

### Step 1.1: Python Environment

```bash
# Create and activate virtual environment
conda create --name finrobot python=3.10
conda activate finrobot

# OR using venv
python -m venv finrobot_env
source finrobot_env/bin/activate  # macOS/Linux
```

### Step 1.2: Install Dependencies

```bash
cd /Users/Gautam/CapGlobal-FInRobot

# Install the package in development mode
pip install -e .

# If issues, install requirements directly
pip install -r requirements.txt
```

### Step 1.3: API Keys Required

| API | Where to Get | Priority |
|-----|--------------|----------|
| **OpenAI** | https://platform.openai.com/api-keys | 🔴 Critical |
| **Finnhub** | https://finnhub.io/register | 🔴 Critical |
| **FMP** | https://site.financialmodelingprep.com/developer/docs | 🟡 Important |
| **SEC-API** | https://sec-api.io | 🟡 Important |
| **Reddit** | https://www.reddit.com/prefs/apps | 🟢 Optional |

### Step 1.4: Configure API Keys

1. **OpenAI Config** - Edit `OAI_CONFIG_LIST`:
```json
[
    {
        "model": "gpt-4-0125-preview",
        "api_key": "sk-YOUR_ACTUAL_KEY_HERE"
    }
]
```

2. **Other APIs** - Edit `config_api_keys`:
```json
{
    "FINNHUB_API_KEY": "your_actual_finnhub_key",
    "FMP_API_KEY": "your_actual_fmp_key",
    "SEC_API_KEY": "your_actual_sec_key",
    "SEC_API_ORGANIZATION": "YourCompanyName",
    "SEC_API_EMAIL": "your@email.com"
}
```

---

## 🟡 PHASE 2: Validation Tests (Day 2)

### Test 2.1: Data Source Connectivity

```python
# test_connections.py
import os
import sys
sys.path.insert(0, '/Users/Gautam/CapGlobal-FInRobot')

from finrobot.utils import register_keys_from_json
from finrobot.data_source import FinnHubUtils, YFinanceUtils, FMPUtils

# Load API keys
register_keys_from_json('config_api_keys')

# Test YFinance (no API key needed)
print("=" * 50)
print("Testing YFinance...")
stock_data = YFinanceUtils.get_stock_data("AAPL", "2024-01-01", "2024-01-15")
print(stock_data.head())
print("✅ YFinance working!")

# Test Finnhub
print("=" * 50)
print("Testing Finnhub...")
profile = FinnHubUtils.get_company_profile("AAPL")
print(profile[:200] + "...")
print("✅ Finnhub working!")

# Test FMP
print("=" * 50)
print("Testing FMP...")
report = FMPUtils.get_sec_report("AAPL", "2023")
print(report)
print("✅ FMP working!")
```

### Test 2.2: OpenAI Connection

```python
import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={"model": ["gpt-4-0125-preview"]}
)

print(f"Found {len(config_list)} model configurations")
print("✅ OpenAI config loaded!")
```

---

## 🟢 PHASE 3: Use Case 1 - Market Forecaster (Day 3-4)

### The Simplest Agent - Stock Prediction

```python
# market_forecaster.py
import autogen
from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.agents.workflow import SingleAssistant

# Configuration
llm_config = {
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-0125-preview"]},
    ),
    "timeout": 120,
    "temperature": 0,
}

# Load API keys
register_keys_from_json("config_api_keys")

# Create Market Analyst Agent
company = "NVDA"  # Change to any stock ticker

assistant = SingleAssistant(
    "Market_Analyst",
    llm_config,
    human_input_mode="NEVER",  # or "ALWAYS" for interactive
)

# Run analysis
assistant.chat(
    f"""Use all the tools provided to retrieve information available for {company} 
    upon {get_current_date()}. 
    
    Analyze the positive developments and potential concerns of {company} 
    with 2-4 most important factors respectively and keep them concise. 
    Most factors should be inferred from company related news.
    
    Then make a rough prediction (e.g. up/down by 2-3%) of the {company} 
    stock price movement for next week. 
    
    Provide a summary analysis to support your prediction."""
)
```

### What This Does:
1. Fetches company profile from Finnhub
2. Gets recent news articles
3. Retrieves basic financials
4. Gets stock price data from YFinance
5. LLM analyzes all data and makes prediction

---

## 🔵 PHASE 4: Use Case 2 - Equity Research Report (Day 5-7)

### Generate Professional PDF Reports

```python
# equity_report.py
import os
import autogen
from textwrap import dedent
from finrobot.utils import register_keys_from_json
from finrobot.agents.workflow import SingleAssistantShadow

# Configuration
llm_config = {
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-0125-preview"]},
    ),
    "timeout": 120,
    "temperature": 0.5,
}

register_keys_from_json("config_api_keys")

# Create output directory
work_dir = "report"
os.makedirs(work_dir, exist_ok=True)

# Create Expert Investor Agent (with shadow for nested instructions)
assistant = SingleAssistantShadow(
    "Expert_Investor",
    llm_config,
    max_consecutive_auto_reply=None,
    human_input_mode="TERMINATE",
)

# Run report generation
company = "Microsoft"
fyear = "2023"

message = dedent(f"""
    With the tools you've been provided, write an annual report based on 
    {company}'s {fyear} 10-K report, format it into a PDF.
    
    Pay attention to the following:
    - Explicitly explain your working plan before you kick off.
    - Use tools one by one for clarity, especially when asking for instructions. 
    - All your file operations should be done in "{work_dir}". 
    - Display any image in the chat once generated.
    - All the paragraphs should combine between 400 and 450 words.
""")

assistant.chat(message, use_cache=True, max_turns=50, summary_method="last_msg")
```

### Report Includes:
- Business Overview
- Market Position
- Operating Results (Income, Balance, Cash Flow analysis)
- Financial Metrics Table
- Risk Assessment
- Competitor Analysis
- Stock Performance Charts
- PE & EPS Charts

---

## 🟣 PHASE 5: Use Case 3 - RAG Q&A on SEC Filings (Day 8-9)

### Ask Questions About Annual Reports

```python
# rag_qa.py
import autogen
from finrobot.utils import register_keys_from_json
from finrobot.agents.workflow import SingleAssistantRAG

llm_config = {
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-0125-preview"]},
    ),
    "timeout": 120,
    "temperature": 0,
}

register_keys_from_json("config_api_keys")

# RAG configuration - point to SEC filing
retrieve_config = {
    "task": "qa",
    "docs_path": "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm",
    "chunk_token_size": 1000,
    "collection_name": "apple_10k_2023",
    "get_or_create": True,
}

# Create RAG-enabled agent
rag_assistant = SingleAssistantRAG(
    "Financial_Analyst",
    llm_config=llm_config,
    retrieve_config=retrieve_config,
    rag_description="Retrieve content from Apple's 2023 10-K SEC filing for Q&A",
    human_input_mode="NEVER",
)

# Ask questions about the filing
questions = [
    "What are Apple's main risk factors mentioned in the 10-K?",
    "What was Apple's revenue growth compared to previous year?",
    "What are the key segments of Apple's business?",
]

for q in questions:
    print(f"\n{'='*60}\nQuestion: {q}\n{'='*60}")
    rag_assistant.chat(q)
    rag_assistant.reset()
```

---

## ⚫ PHASE 6: Multi-Agent Investment Team (Day 10+)

### Full Investment Analysis Team

```python
# investment_team.py
import autogen
from finrobot.agents.workflow import MultiAssistantWithLeader
from finrobot.data_source import FinnHubUtils, YFinanceUtils, FMPUtils, RedditUtils

llm_config = {
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-0125-preview"]},
    ),
    "cache_seed": 42,
    "temperature": 0,
}

# Define the investment team structure
group_config = {
    "leader": {
        "title": "Chief Investment Officer",
        "responsibilities": [
            "Oversee the entire investment analysis process",
            "Integrate insights from all analyst groups",
            "Make final investment recommendation",
        ],
    },
    "agents": [
        {
            "title": "Market Sentiment Analyst",
            "responsibilities": [
                "Track and interpret market trends and news",
                "Analyze social media sentiment",
            ],
            "toolkits": [
                FinnHubUtils.get_company_news,
                RedditUtils.get_reddit_posts,
            ],
        },
        {
            "title": "Fundamental Analyst",
            "responsibilities": [
                "Analyze financial statements",
                "Calculate key financial metrics",
            ],
            "toolkits": [
                YFinanceUtils.get_income_stmt,
                YFinanceUtils.get_balance_sheet,
                FMPUtils.get_financial_metrics,
            ],
        },
        {
            "title": "Technical Analyst",
            "responsibilities": [
                "Analyze stock price patterns",
                "Identify support/resistance levels",
            ],
            "toolkits": [
                YFinanceUtils.get_stock_data,
            ],
        },
    ],
}

# Create the multi-agent team
investment_team = MultiAssistantWithLeader(
    group_config,
    llm_config=llm_config,
)

# Run investment analysis
task = """
Analyze NVDA (NVIDIA) for potential investment:
1. Gather recent market sentiment from news and social media
2. Analyze the latest financial statements
3. Review recent stock price movements
4. Provide a comprehensive investment recommendation with target price
"""

investment_team.chat(message=task, use_cache=True)
```

---

## 📊 Cost Estimation

| Use Case | Tokens/Run | Cost/Run (GPT-4) |
|----------|------------|------------------|
| Market Forecaster | ~5,000 | ~$0.15 |
| Equity Report | ~50,000 | ~$1.50 |
| RAG Q&A (per question) | ~3,000 | ~$0.09 |
| Multi-Agent Team | ~100,000 | ~$3.00 |

---

## 🛠️ Directory Structure After Setup

```
CapGlobal-FInRobot/
├── config_api_keys          # Your API keys (DO NOT COMMIT)
├── OAI_CONFIG_LIST          # OpenAI config (DO NOT COMMIT)
├── .gitignore               # Should ignore above files
├── report/                  # Generated reports go here
├── coding/                  # Agent-generated code executes here
├── finrobot/               # Core package
└── tutorials_beginner/     # Jupyter notebooks to learn
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "FINNHUB_API_KEY not set"
```python
# Solution: Make sure you call this BEFORE using FinnHubUtils
from finrobot.utils import register_keys_from_json
register_keys_from_json("config_api_keys")
```

### Issue 2: "Rate limit exceeded"
```python
# Solution: Add delays between API calls
import time
time.sleep(1)  # 1 second delay
```

### Issue 3: "SEC section extraction fails"
```python
# Solution: SEC-API requires paid subscription for section extraction
# Alternative: Use FMPUtils.get_sec_report() for basic info
```

### Issue 4: "Docker not found"
```python
# Solution: Set use_docker=False in code_execution_config
code_execution_config={
    "work_dir": "coding",
    "use_docker": False,  # Disable Docker
}
```

---

## 🎯 Quick Start Command

After setting up API keys:

```bash
cd /Users/Gautam/CapGlobal-FInRobot
conda activate finrobot
python -c "
from finrobot.utils import register_keys_from_json
from finrobot.data_source import YFinanceUtils
print('Testing YFinance...')
data = YFinanceUtils.get_stock_data('AAPL', '2024-01-01', '2024-01-05')
print(data)
print('✅ Setup complete!')
"
```

