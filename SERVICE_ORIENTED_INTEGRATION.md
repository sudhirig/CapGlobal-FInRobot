# Service-Oriented Integration: CGMF ↔ FinRobot
## Keep Both Frameworks Intact - Minimal Refactoring

## 🎯 Core Principle

**Both systems stay independent** - they communicate via **REST APIs** as services.

```
┌─────────────────────────────────────────────────────────────┐
│                    CGMF System (Base)                        │
│  TypeScript + LangGraph + 9 Agents                          │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Hierarchical Agent Controller                      │    │
│  │  - AI Investment Advisor (Main)                     │    │
│  │  - AI Fund Assistant V2                             │    │
│  │  - User Profile Agent                               │    │
│  │  - Risk Management Agent                            │    │
│  │  - Tax Optimization Agent                           │    │
│  │  - Performance Analytics Agent                      │    │
│  │  - ELIVATE Market Agent                             │    │
│  │  - Investment Advisor Agent                         │    │
│  │  - Mutual Fund Agent                                │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  NEW: FinRobot Service Client                       │    │
│  │  (HTTP calls to FinRobot API)                       │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          ↕ HTTP/REST API
┌─────────────────────────────────────────────────────────────┐
│                  FinRobot System (Service)                   │
│  Python + AutoGen + Multi-Agent                             │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FastAPI REST Service                                │    │
│  │  - /api/stock/analyze                                │    │
│  │  - /api/stock/info                                   │    │
│  │  - /api/stock/backtest                               │    │
│  │  - /api/stock/report                                 │    │
│  │  - /api/agents/multi-team                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FinRobot Agents (Unchanged)                        │    │
│  │  - Market Analyst                                   │    │
│  │  - Fundamental Analyst                              │    │
│  │  - Technical Analyst                                │    │
│  │  - CIO (Leader)                                     │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Implementation Plan

### Step 1: Expose FinRobot as REST API (FastAPI)

**File**: `finrobot-service/main.py` (NEW - minimal code)

```python
# finrobot-service/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import sys

# Add FinRobot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from finrobot.agents.workflow import MultiAssistantWithLeader, SingleAssistant
from finrobot.data_source import YFinanceUtils, FinnHubUtils, SECUtils
from finrobot.functional import ReportLabUtils, BackTraderUtils
import autogen

app = FastAPI(title="FinRobot API Service")

# CORS for CGMF to call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class StockAnalysisRequest(BaseModel):
    ticker: str
    analysis_type: Optional[str] = "comprehensive"  # market, fundamental, technical, comprehensive
    depth: Optional[str] = "standard"  # quick, standard, deep

class BacktestRequest(BaseModel):
    ticker: str
    strategy: str
    start_date: str
    end_date: str

class MultiAgentRequest(BaseModel):
    ticker: str
    query: str
    depth: Optional[str] = "standard"

# Initialize FinRobot agents (lazy loading)
_finrobot_agents = None

def get_finrobot_agents():
    global _finrobot_agents
    if _finrobot_agents is None:
        # Load API keys from environment
        llm_config = {
            "config_list": [{
                "model": "gpt-4o",
                "api_key": os.environ.get("OPENAI_API_KEY"),
            }],
            "timeout": 120,
            "temperature": 0.7,
        }
        _finrobot_agents = MultiAssistantWithLeader(
            group_config={
                "leader": {
                    "title": "Chief Investment Officer",
                    "responsibilities": ["Final recommendations", "Consensus building"]
                },
                "agents": [
                    {"title": "Market Analyst", "responsibilities": ["News analysis", "Market sentiment"]},
                    {"title": "Fundamental Analyst", "responsibilities": ["Financial statements", "Valuation"]},
                    {"title": "Technical Analyst", "responsibilities": ["Price patterns", "Technical indicators"]},
                ]
            },
            llm_config=llm_config
        )
    return _finrobot_agents

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "finrobot"}

@app.post("/api/stock/info")
async def get_stock_info(request: StockAnalysisRequest):
    """Get basic stock information"""
    try:
        info = YFinanceUtils.get_stock_info(request.ticker)
        return {"success": True, "data": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stock/analyze")
async def analyze_stock(request: StockAnalysisRequest):
    """Run comprehensive stock analysis using FinRobot agents"""
    try:
        agents = get_finrobot_agents()
        
        query = f"Analyze {request.ticker} with {request.analysis_type} analysis at {request.depth} depth"
        
        # Run analysis (this uses AutoGen internally - no changes needed!)
        agents.chat(query)
        
        # Get results from conversation
        messages = agents.user_proxy.chat_messages[agents.agents[0].name]
        result = messages[-1].get("content", "") if messages else "Analysis completed"
        
        return {
            "success": True,
            "ticker": request.ticker,
            "analysis_type": request.analysis_type,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stock/multi-agent")
async def multi_agent_analysis(request: MultiAgentRequest):
    """Run multi-agent investment team analysis"""
    try:
        agents = get_finrobot_agents()
        
        query = f"For {request.ticker}: {request.query}"
        
        # Use existing MultiAssistantWithLeader - no changes!
        agents.chat(query)
        
        # Extract results
        messages = agents.user_proxy.chat_messages
        results = {}
        for agent_name, msgs in messages.items():
            if msgs:
                results[agent_name] = msgs[-1].get("content", "")
        
        return {
            "success": True,
            "ticker": request.ticker,
            "query": request.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stock/backtest")
async def backtest_strategy(request: BacktestRequest):
    """Run backtesting"""
    try:
        result = BackTraderUtils.back_test(
            request.ticker,
            request.strategy,
            request.start_date,
            request.end_date
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stock/report")
async def generate_report(request: StockAnalysisRequest):
    """Generate PDF report"""
    try:
        # Use existing ReportLabUtils - no changes!
        report_path = ReportLabUtils.build_annual_report(
            ticker=request.ticker,
            year=2024  # or get from request
        )
        return {"success": True, "report_path": report_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**That's it!** FinRobot stays 100% unchanged - just wrapped in FastAPI.

---

### Step 2: Create FinRobot Service Client in CGMF

**File**: `server/services/finrobot-service.ts` (NEW - minimal code)

```typescript
// server/services/finrobot-service.ts
import axios, { AxiosInstance } from 'axios';

const FINROBOT_SERVICE_URL = process.env.FINROBOT_SERVICE_URL || 'http://localhost:8000';

export interface StockAnalysisRequest {
  ticker: string;
  analysis_type?: 'market' | 'fundamental' | 'technical' | 'comprehensive';
  depth?: 'quick' | 'standard' | 'deep';
}

export interface StockInfo {
  longName: string;
  currentPrice: number;
  marketCap: number;
  peRatio: number;
  // ... other fields
}

export class FinRobotService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: FINROBOT_SERVICE_URL,
      timeout: 120000, // 2 minutes for complex analysis
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async getStockInfo(ticker: string): Promise<StockInfo> {
    const response = await this.client.post('/api/stock/info', { ticker });
    return response.data.data;
  }

  async analyzeStock(request: StockAnalysisRequest): Promise<any> {
    const response = await this.client.post('/api/stock/analyze', request);
    return response.data;
  }

  async multiAgentAnalysis(ticker: string, query: string, depth: string = 'standard'): Promise<any> {
    const response = await this.client.post('/api/stock/multi-agent', {
      ticker,
      query,
      depth,
    });
    return response.data;
  }

  async backtest(ticker: string, strategy: string, startDate: string, endDate: string): Promise<any> {
    const response = await this.client.post('/api/stock/backtest', {
      ticker,
      strategy,
      start_date: startDate,
      end_date: endDate,
    });
    return response.data;
  }

  async generateReport(ticker: string, analysisType: string = 'comprehensive'): Promise<string> {
    const response = await this.client.post('/api/stock/report', {
      ticker,
      analysis_type: analysisType,
    });
    return response.data.report_path;
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.client.get('/health');
      return response.data.status === 'healthy';
    } catch {
      return false;
    }
  }
}

export const finrobotService = new FinRobotService();
```

---

### Step 3: Create LangGraph Tools for FinRobot Services

**File**: `server/agents/finrobot-tools.ts` (NEW)

```typescript
// server/agents/finrobot-tools.ts
import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";
import { finrobotService } from '../services/finrobot-service';

// Stock Info Tool
export const stockInfoTool = new DynamicStructuredTool({
  name: "get_stock_info",
  description: "Get comprehensive stock information including price, market cap, PE ratio, and company details. Use this for any stock ticker query.",
  schema: z.object({
    ticker: z.string().describe("Stock ticker symbol (e.g., AAPL, MSFT, NVDA)"),
  }),
  func: async ({ ticker }) => {
    const info = await finrobotService.getStockInfo(ticker);
    return JSON.stringify(info, null, 2);
  }
});

// Stock Analysis Tool
export const stockAnalysisTool = new DynamicStructuredTool({
  name: "analyze_stock",
  description: "Run comprehensive stock analysis using AI agents. Returns detailed analysis including market sentiment, fundamentals, and technical indicators.",
  schema: z.object({
    ticker: z.string(),
    analysis_type: z.enum(["market", "fundamental", "technical", "comprehensive"]).optional(),
    depth: z.enum(["quick", "standard", "deep"]).optional(),
  }),
  func: async ({ ticker, analysis_type = "comprehensive", depth = "standard" }) => {
    const result = await finrobotService.analyzeStock({ ticker, analysis_type, depth });
    return result.result || JSON.stringify(result, null, 2);
  }
});

// Multi-Agent Investment Team Tool
export const multiAgentAnalysisTool = new DynamicStructuredTool({
  name: "multi_agent_stock_analysis",
  description: "Get investment team consensus analysis from multiple specialized AI agents (Market Analyst, Fundamental Analyst, Technical Analyst, CIO). Best for comprehensive investment decisions.",
  schema: z.object({
    ticker: z.string(),
    query: z.string().describe("Specific question or analysis request"),
    depth: z.enum(["quick", "standard", "deep"]).optional(),
  }),
  func: async ({ ticker, query, depth = "standard" }) => {
    const result = await finrobotService.multiAgentAnalysis(ticker, query, depth);
    return JSON.stringify(result.results, null, 2);
  }
});

// Backtesting Tool
export const backtestTool = new DynamicStructuredTool({
  name: "backtest_trading_strategy",
  description: "Backtest trading strategies on historical stock data. Returns performance metrics and charts.",
  schema: z.object({
    ticker: z.string(),
    strategy: z.string().describe("Trading strategy name or description"),
    start_date: z.string().describe("Start date (YYYY-MM-DD)"),
    end_date: z.string().describe("End date (YYYY-MM-DD)"),
  }),
  func: async ({ ticker, strategy, start_date, end_date }) => {
    const result = await finrobotService.backtest(ticker, strategy, start_date, end_date);
    return JSON.stringify(result, null, 2);
  }
});

// Export all tools
export const finrobotTools = [
  stockInfoTool,
  stockAnalysisTool,
  multiAgentAnalysisTool,
  backtestTool,
];
```

---

### Step 4: Add Stock Analysis Agent to CGMF Hierarchy

**File**: `server/agents/stock-analysis-agent.ts` (NEW)

```typescript
// server/agents/stock-analysis-agent.ts
import { StateGraph, Annotation, END } from "@langchain/langgraph";
import { BaseMessage, HumanMessage } from "@langchain/core/messages";
import { ChatAnthropic } from "@langchain/anthropic";
import { finrobotTools } from './finrobot-tools';
import { ToolNode } from "@langchain/langgraph/prebuilt";

const StockAnalysisState = Annotation.Root({
  messages: Annotation<BaseMessage[]>({
    reducer: (x, y) => x.concat(y),
    default: () => []
  }),
  ticker: Annotation<string>(),
  analysisType: Annotation<string>(),
  results: Annotation<any>(),
});

type StockAnalysisStateType = typeof StockAnalysisState.State;

export class StockAnalysisAgent {
  private graph: any;
  private model: ChatAnthropic;
  private tools: any[];

  constructor() {
    this.model = new ChatAnthropic({
      model: "claude-sonnet-4-20250514",
      temperature: 0.7,
    });

    // Bind tools to model
    this.tools = finrobotTools;
    const toolNode = new ToolNode(this.tools);
    const boundModel = this.model.bindTools(this.tools);

    // Create LangGraph workflow
    this.graph = new StateGraph(StockAnalysisState)
      .addNode("agent", this.callAgent.bind(this))
      .addNode("tools", toolNode.invoke.bind(toolNode))
      .addEdge("agent", "tools")
      .addConditionalEdges("tools", this.shouldContinue.bind(this))
      .setEntryPoint("agent")
      .compile();
  }

  async callAgent(state: StockAnalysisStateType) {
    const boundModel = this.model.bindTools(this.tools);
    const response = await boundModel.invoke(state.messages);
    return { messages: [response] };
  }

  shouldContinue(state: StockAnalysisStateType) {
    const lastMessage = state.messages[state.messages.length - 1];
    if (lastMessage.tool_calls && lastMessage.tool_calls.length > 0) {
      return "tools";
    }
    return END;
  }

  async analyze(ticker: string, query: string): Promise<string> {
    const result = await this.graph.invoke({
      messages: [new HumanMessage(`Analyze ${ticker}: ${query}`)],
      ticker,
      analysisType: "comprehensive",
      results: {},
    });

    const lastMessage = result.messages[result.messages.length - 1];
    return lastMessage.content;
  }
}
```

---

### Step 5: Register New Agent in Hierarchical Controller

**File**: `server/services/hierarchical-agent-controller.ts` (MINOR UPDATE)

```typescript
// Add to AgentType enum
export enum AgentType {
  // ... existing agents ...
  STOCK_ANALYSIS = 'stock_analysis',  // NEW
}

// Add to initializeAgentRegistry()
private initializeAgentRegistry() {
  // ... existing registrations ...
  
  // NEW: Stock Analysis Agent
  this.registerAgent({
    type: AgentType.STOCK_ANALYSIS,
    name: 'Stock Analysis Agent',
    description: 'Analyzes stocks using FinRobot AI agents (Market, Fundamental, Technical analysis)',
    accessLevel: AccessLevel.CONTROLLED,  // Via AI Investment Advisor
    capabilities: [
      'stock_analysis',
      'market_sentiment',
      'fundamental_analysis',
      'technical_analysis',
      'backtesting',
      'investment_recommendations'
    ],
    dependencies: []
  });
}

// Add routing logic in routeQuery()
async routeQuery(...) {
  // ... existing routing ...
  
  // NEW: Route stock queries to Stock Analysis Agent
  if (intent.includes('stock') || intent.includes('equity') || 
      /[A-Z]{1,5}/.test(query)) {  // Detects ticker symbols
    return await this.routeToStockAgent(query, sessionId, context);
  }
}
```

---

## 🎯 What Changes?

### FinRobot (Python/AutoGen)
- ✅ **ZERO changes** to existing code
- ✅ Add `finrobot-service/main.py` (FastAPI wrapper - ~200 lines)
- ✅ Keep all agents, tools, workflows **exactly as-is**

### CGMF (TypeScript/LangGraph)
- ✅ Add `server/services/finrobot-service.ts` (~100 lines)
- ✅ Add `server/agents/finrobot-tools.ts` (~80 lines)
- ✅ Add `server/agents/stock-analysis-agent.ts` (~100 lines)
- ✅ Update `hierarchical-agent-controller.ts` (~20 lines)

**Total new code: ~500 lines**  
**Refactoring: ZERO**

---

## 🚀 Deployment

### Option 1: Same Server (Recommended for Development)
```bash
# Terminal 1: Start FinRobot service
cd /path/to/finrobot
python -m uvicorn finrobot-service.main:app --port 8000

# Terminal 2: Start CGMF
cd /path/to/cgmf
npm run dev
```

### Option 2: Separate Services (Production)
- FinRobot: Deploy FastAPI service (Docker/Cloud)
- CGMF: Set `FINROBOT_SERVICE_URL` environment variable

---

## ✅ Benefits

1. **No Refactoring**: Both systems stay intact
2. **Independent Updates**: Update FinRobot or CGMF separately
3. **Language Agnostic**: Python ↔ TypeScript via HTTP
4. **Scalable**: Can deploy services separately
5. **Testable**: Test each service independently
6. **Maintainable**: Clear service boundaries

---

## 📊 Architecture Flow

```
User Query: "Analyze AAPL stock"
    ↓
CGMF: AI Investment Advisor (LangGraph)
    ↓
CGMF: Stock Analysis Agent (LangGraph)
    ↓
CGMF: Calls stockAnalysisTool (LangGraph Tool)
    ↓
HTTP POST → FinRobot Service (FastAPI)
    ↓
FinRobot: MultiAssistantWithLeader (AutoGen)
    ↓
FinRobot: Market Analyst + Fundamental + Technical (AutoGen)
    ↓
FinRobot: Returns results
    ↓
HTTP Response → CGMF
    ↓
CGMF: Formats response (LangGraph)
    ↓
User: Gets unified response
```

---

## 🎉 Result

**Both frameworks work together seamlessly** with minimal code changes!

- CGMF's LangGraph orchestrates everything
- FinRobot's AutoGen agents do the stock analysis
- They communicate via REST API
- **No major refactoring needed!**

---

**Status**: Ready to implement  
**Estimated Time**: 1-2 days  
**Risk**: Low (both systems stay independent)

