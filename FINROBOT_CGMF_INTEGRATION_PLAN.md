# FinRobot → CGMF Integration Plan
## Merging FinRobot into CGMF's Hierarchical Multi-Agent System with LangGraph

## Executive Summary

**Goal**: Integrate FinRobot's stock analysis capabilities into CGMF's sophisticated 9-agent hierarchical system, creating a unified AI-powered financial intelligence platform that handles both **mutual funds** (CGMF) and **stocks** (FinRobot).

**Key Benefits**:
- ✅ Unified platform for all investment types
- ✅ Leverage CGMF's proven LangGraph orchestration
- ✅ Maintain FinRobot's powerful stock analysis tools
- ✅ Create new specialized agents for stock analysis
- ✅ Single frontend for both mutual funds and stocks

---

## Current State Analysis

### CGMF System (Target Platform)
- **Framework**: LangGraph (TypeScript/Node.js)
- **LLM**: Anthropic Claude (Sonnet 4)
- **Agents**: 9 specialized agents in hierarchical structure
- **Focus**: Indian Mutual Funds (16,766 funds)
- **Frontend**: React + TypeScript
- **Database**: PostgreSQL + pgvector
- **Architecture**: Production-ready, 90.6% score

### FinRobot System (To Be Integrated)
- **Framework**: Microsoft AutoGen (Python)
- **LLM**: OpenAI GPT-4
- **Agents**: Multi-agent workflows (SingleAssistant, MultiAssistantWithLeader)
- **Focus**: Global Stocks (US markets)
- **Frontend**: Streamlit (Python)
- **Data Sources**: YFinance, Finnhub, SEC-API, FMP, Reddit
- **Tools**: Stock analysis, PDF reports, backtesting, charts

---

## Integration Strategy

### Phase 1: Architecture Design ✅

#### 1.1 New Agent Structure

Add **3 new specialized agents** to CGMF's 9-agent system:

```
CGMF Hierarchical System (Current: 9 agents)
├── AI Investment Advisor (Main Controller)
├── AI Fund Assistant V2 (MF Database)
├── User Profile Agent
├── Investment Advisor Agent
├── ELIVATE Market Agent
├── Mutual Fund Agent
├── Risk Management Agent
├── Tax Optimization Agent
└── Performance Analytics Agent

NEW AGENTS (FinRobot Integration):
├── Stock Market Analyst Agent ⭐ NEW
│   ├── Market Analyst (from FinRobot)
│   ├── Fundamental Analyst (from FinRobot)
│   └── Technical Analyst (from FinRobot)
├── Stock Research Agent ⭐ NEW
│   ├── SEC Filing Analysis
│   ├── Company Research
│   └── Industry Analysis
└── Portfolio Intelligence Agent ⭐ ENHANCED
    ├── Stock Portfolio Analysis
    ├── MF Portfolio Analysis
    └── Unified Portfolio View
```

#### 1.2 LangGraph Workflow Design

```typescript
// New Stock Analysis Graph
const StockAnalysisGraph = {
  nodes: {
    'intent_classifier': classifyStockIntent,
    'market_analyst': analyzeMarketSentiment,      // FinRobot: Market Analyst
    'fundamental_analyst': analyzeFundamentals,    // FinRobot: Fundamental Analyst
    'technical_analyst': analyzeTechnical,          // FinRobot: Technical Analyst
    'sec_researcher': analyzeSECFilings,           // FinRobot: SEC Analysis
    'report_generator': generateStockReport,         // FinRobot: PDF Reports
    'portfolio_optimizer': optimizePortfolio,       // Unified: Stocks + MF
    'risk_assessor': assessPortfolioRisk,           // CGMF: Risk Management
    'response_formatter': formatResponse
  },
  edges: {
    conditional: [
      { from: 'intent_classifier', to: ['market_analyst', 'fundamental_analyst', 'technical_analyst', 'sec_researcher'] },
      { from: 'fundamental_analyst', to: ['portfolio_optimizer', 'risk_assessor'] }
    ],
    parallel: [
      ['market_analyst', 'fundamental_analyst', 'technical_analyst'] // Run simultaneously
    ]
  }
}
```

---

## Phase 2: Technical Implementation

### 2.1 Convert FinRobot Tools to LangGraph Tools

**Current FinRobot Tools** (Python/AutoGen):
```python
# finrobot/toolkits.py
- YFinanceUtils: get_stock_info, get_historical_data
- FinnHubUtils: get_company_news, get_company_profile
- SECUtils: get_filings, extract_financials
- FMPUtils: get_financial_metrics
- ReportLabUtils: build_annual_report
- BackTraderUtils: back_test
```

**Converted to LangGraph Tools** (TypeScript):
```typescript
// server/agents/finrobot-tools.ts
import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";

// Stock Info Tool
export const stockInfoTool = new DynamicStructuredTool({
  name: "get_stock_info",
  description: "Get comprehensive stock information (price, metrics, company data)",
  schema: z.object({
    ticker: z.string().describe("Stock ticker symbol (e.g., AAPL, MSFT)"),
  }),
  func: async ({ ticker }) => {
    // Call Python microservice or Node.js implementation
    return await yfinanceService.getStockInfo(ticker);
  }
});

// SEC Filing Analysis Tool
export const secFilingTool = new DynamicStructuredTool({
  name: "analyze_sec_filing",
  description: "Analyze SEC filings (10-K, 10-Q) for financial insights",
  schema: z.object({
    ticker: z.string(),
    filingType: z.enum(["10-K", "10-Q", "8-K"]).optional(),
    year: z.number().optional(),
  }),
  func: async ({ ticker, filingType, year }) => {
    return await secService.analyzeFiling(ticker, filingType, year);
  }
});

// Backtesting Tool
export const backtestTool = new DynamicStructuredTool({
  name: "backtest_strategy",
  description: "Backtest trading strategies using historical data",
  schema: z.object({
    ticker: z.string(),
    strategy: z.string(),
    startDate: z.string(),
    endDate: z.string(),
  }),
  func: async ({ ticker, strategy, startDate, endDate }) => {
    return await backtestService.runBacktest(ticker, strategy, startDate, endDate);
  }
});
```

### 2.2 Create Stock Market Analyst Agent

```typescript
// server/agents/stock-market-analyst-agent.ts
import { StateGraph, Annotation } from "@langchain/langgraph";
import { ChatAnthropic } from "@langchain/anthropic";
import { stockInfoTool, secFilingTool, backtestTool } from './finrobot-tools';

const StockAnalystState = Annotation.Root({
  messages: Annotation<BaseMessage[]>(),
  ticker: Annotation<string>(),
  analysisType: Annotation<'market' | 'fundamental' | 'technical' | 'comprehensive'>(),
  marketData: Annotation<any>(),
  fundamentalData: Annotation<any>(),
  technicalData: Annotation<any>(),
  recommendations: Annotation<any[]>(),
});

export class StockMarketAnalystAgent {
  private graph: StateGraph;
  private model: ChatAnthropic;
  
  constructor() {
    this.model = new ChatAnthropic({
      model: "claude-sonnet-4-20250514",
      temperature: 0.7
    });
    
    // Create LangGraph workflow
    this.graph = new StateGraph(StockAnalystState)
      .addNode("classify_intent", this.classifyIntent.bind(this))
      .addNode("market_analysis", this.analyzeMarket.bind(this))
      .addNode("fundamental_analysis", this.analyzeFundamentals.bind(this))
      .addNode("technical_analysis", this.analyzeTechnical.bind(this))
      .addNode("generate_recommendations", this.generateRecommendations.bind(this))
      .addConditionalEdges("classify_intent", this.routeByIntent.bind(this))
      .addEdge("market_analysis", "generate_recommendations")
      .addEdge("fundamental_analysis", "generate_recommendations")
      .addEdge("technical_analysis", "generate_recommendations")
      .compile();
  }
  
  async analyzeMarket(state: StockAnalystStateType) {
    // Use FinRobot's Market Analyst logic
    const news = await finnhubService.getCompanyNews(state.ticker);
    const sentiment = await analyzeSentiment(news);
    return { marketData: { news, sentiment } };
  }
  
  async analyzeFundamentals(state: StockAnalystStateType) {
    // Use FinRobot's Fundamental Analyst logic
    const info = await stockInfoTool.func({ ticker: state.ticker });
    const financials = await secFilingTool.func({ ticker: state.ticker, filingType: "10-K" });
    return { fundamentalData: { info, financials } };
  }
  
  async analyzeTechnical(state: StockAnalystStateType) {
    // Use FinRobot's Technical Analyst logic
    const historical = await yfinanceService.getHistoricalData(state.ticker);
    const indicators = await calculateTechnicalIndicators(historical);
    return { technicalData: { historical, indicators } };
  }
}
```

### 2.3 Integration with CGMF's AI Investment Advisor

```typescript
// server/services/ai-advisory-agent.ts (Enhanced)
export class AIAdvisoryAgent {
  // ... existing code ...
  
  async routeQuery(query: string, userId: string) {
    const intent = await this.analyzeIntent(query);
    
    // NEW: Route to stock analysis agents
    if (intent.type === 'stock_analysis' || intent.type === 'equity_research') {
      return await this.routeToStockAgents(query, userId, intent);
    }
    
    // Existing: Route to MF agents
    if (intent.type === 'mutual_fund' || intent.type === 'mf_analysis') {
      return await this.routeToMFAgents(query, userId, intent);
    }
    
    // NEW: Unified portfolio queries
    if (intent.type === 'portfolio' || intent.type === 'unified_portfolio') {
      return await this.routeToPortfolioAgent(query, userId, intent);
    }
    
    // Default routing
    return await this.defaultRoute(query, userId);
  }
  
  private async routeToStockAgents(query: string, userId: string, intent: any) {
    const stockAnalyst = new StockMarketAnalystAgent();
    const context = await this.getSharedContext(userId);
    
    return await stockAnalyst.invoke({
      messages: [new HumanMessage(query)],
      ticker: intent.ticker,
      analysisType: intent.analysisType,
      ...context
    });
  }
}
```

---

## Phase 3: Data Source Integration

### 3.1 Python Microservice Approach (Recommended)

Since FinRobot is Python-based, create a **Python microservice** that CGMF can call:

```python
# finrobot-service/main.py (FastAPI)
from fastapi import FastAPI
from finrobot.data_source import YFinanceUtils, FinnHubUtils, SECUtils
from finrobot.functional import ReportLabUtils, BackTraderUtils

app = FastAPI()

@app.post("/api/stock/info")
async def get_stock_info(ticker: str):
    return YFinanceUtils.get_stock_info(ticker)

@app.post("/api/stock/analyze")
async def analyze_stock(ticker: str, analysis_type: str):
    # Run multi-agent analysis
    from finrobot.agents.workflow import MultiAssistantWithLeader
    # ... analysis logic
    return results

@app.post("/api/stock/backtest")
async def backtest(ticker: str, strategy: str, start: str, end: str):
    return BackTraderUtils.back_test(ticker, strategy, start, end)
```

**CGMF calls this service**:
```typescript
// server/services/finrobot-service.ts
import axios from 'axios';

const FINROBOT_SERVICE_URL = process.env.FINROBOT_SERVICE_URL || 'http://localhost:8000';

export class FinRobotService {
  async getStockInfo(ticker: string) {
    const response = await axios.post(`${FINROBOT_SERVICE_URL}/api/stock/info`, { ticker });
    return response.data;
  }
  
  async analyzeStock(ticker: string, analysisType: string) {
    const response = await axios.post(`${FINROBOT_SERVICE_URL}/api/stock/analyze`, {
      ticker,
      analysis_type: analysisType
    });
    return response.data;
  }
}
```

### 3.2 Alternative: Direct Node.js Implementation

Port FinRobot's Python code to TypeScript/Node.js:
- Use `yfinance` equivalent: `yahoo-finance2` (npm)
- Use `finnhub-python` equivalent: `finnhub` (npm)
- Use `sec-api` equivalent: `sec-api` (npm)
- Port backtesting logic to Node.js

**Pros**: Faster, no microservice overhead  
**Cons**: More work, need to port all Python code

---

## Phase 4: Unified Frontend

### 4.1 Extend CGMF React Frontend

Add stock analysis pages to CGMF's React app:

```typescript
// client/src/pages/StockAnalysis.tsx
export function StockAnalysis() {
  return (
    <div>
      <h1>Stock Analysis</h1>
      <StockSearch />
      <StockCharts />
      <StockReports />
      <Backtesting />
    </div>
  );
}

// client/src/pages/UnifiedPortfolio.tsx
export function UnifiedPortfolio() {
  return (
    <div>
      <h1>Unified Portfolio</h1>
      <StockHoldings />
      <MutualFundHoldings />
      <CombinedAnalysis />
      <RiskMetrics />
    </div>
  );
}
```

### 4.2 Migrate Streamlit Features

Convert FinRobot's Streamlit features to React:
- ✅ Stock Analysis → React component
- ✅ Charts → Recharts/Chart.js
- ✅ Backtesting → React + Chart visualization
- ✅ PDF Reports → React PDF viewer
- ✅ AI Chat → CGMF's existing chat system

---

## Phase 5: Migration Timeline

### Week 1: Foundation
- [ ] Set up Python microservice for FinRobot
- [ ] Create LangGraph tools for stock analysis
- [ ] Design Stock Market Analyst Agent structure
- [ ] Test data source connectivity

### Week 2: Agent Development
- [ ] Implement Stock Market Analyst Agent
- [ ] Implement Stock Research Agent
- [ ] Integrate with AI Investment Advisor
- [ ] Add routing logic for stock queries

### Week 3: Frontend Integration
- [ ] Add stock analysis pages to React app
- [ ] Migrate chart visualizations
- [ ] Integrate backtesting UI
- [ ] Add unified portfolio view

### Week 4: Testing & Optimization
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Error handling
- [ ] Documentation

---

## Technical Challenges & Solutions

### Challenge 1: Python ↔ TypeScript Communication
**Solution**: FastAPI microservice with REST/GraphQL API

### Challenge 2: Different LLM Providers
**Solution**: 
- Use Claude for CGMF agents (existing)
- Use GPT-4 for stock analysis (via microservice)
- Or standardize on one LLM

### Challenge 3: Data Source APIs
**Solution**: 
- YFinance, Finnhub, SEC-API work from both Python and Node.js
- Create unified API layer

### Challenge 4: State Management
**Solution**: 
- LangGraph checkpointing for conversation state
- Shared context service (already exists in CGMF)

---

## Expected Benefits

### For Users
- ✅ Single platform for all investments (stocks + mutual funds)
- ✅ Unified portfolio view
- ✅ Consistent AI experience
- ✅ Better insights from combined analysis

### For System
- ✅ Leverage CGMF's proven architecture
- ✅ Reuse LangGraph orchestration
- ✅ Maintain FinRobot's powerful tools
- ✅ Scalable, production-ready system

---

## Success Metrics

1. **Technical**:
   - Stock analysis response time < 5s
   - 99% uptime
   - Successful agent routing > 95%

2. **Business**:
   - Unified queries handled correctly
   - User satisfaction > 90%
   - Feature adoption > 70%

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Set up development environment** (Python microservice + CGMF)
3. **Create proof-of-concept** (one stock agent integrated)
4. **Iterate and expand** based on feedback

---

**Status**: 📋 Planning Phase  
**Last Updated**: 2025-11-30  
**Version**: 1.0

