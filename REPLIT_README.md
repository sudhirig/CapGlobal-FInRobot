# FinRobot on Replit 🚀

## 📋 Project Overview

**FinRobot** is an AI-powered financial analysis platform that uses Large Language Models (LLMs) to provide comprehensive stock analysis, market insights, and investment recommendations. This Replit deployment includes:

- **Multi-Agent AI System**: Specialized agents for market analysis, fundamental analysis, and technical analysis
- **Streamlit Web Interface**: Modern, interactive dashboard for financial analysis
- **Real-time Data Integration**: YFinance, Finnhub, SEC-API, and more
- **PDF Report Generation**: Automated equity research reports
- **Backtesting Capabilities**: Test trading strategies on historical data
- **Chart Generation**: Technical analysis charts and visualizations

---

## 🏗️ Architecture

### Tech Stack
- **Language**: Python 3.11
- **Framework**: Microsoft AutoGen (Multi-Agent System)
- **LLM**: OpenAI GPT-4
- **Frontend**: Streamlit
- **Data Sources**: YFinance, Finnhub, SEC-API, FMP, Reddit

### Agent System
- **Market Analyst Agent**: News analysis, market sentiment
- **Fundamental Analyst Agent**: Financial statements, valuation metrics
- **Technical Analyst Agent**: Price patterns, technical indicators
- **CIO (Chief Investment Officer)**: Final recommendations, consensus building

---

## 🚀 Quick Start

### 1. Install Dependencies

The dependencies will be installed automatically when you run the project. If you need to install manually:

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

**Option A: Using Replit Secrets (Recommended)**
1. Click on the "Secrets" tab in Replit
2. Add the following secrets:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `FINNHUB_API_KEY` - Your Finnhub API key
   - `FMP_API_KEY` - Your Financial Modeling Prep API key (optional)
   - `SEC_API_KEY` - Your SEC-API key
   - `REDDIT_CLIENT_ID` - Reddit API client ID (optional)
   - `REDDIT_CLIENT_SECRET` - Reddit API client secret (optional)

**Option B: Using Environment Variables**
Edit `.replit` file and add your keys in the `[env]` section (not recommended for production)

**Option C: Using Config Files**
1. Copy `config_api_keys.example` to `config_api_keys`
2. Copy `OAI_CONFIG_LIST.example` to `OAI_CONFIG_LIST`
3. Fill in your API keys

### 3. Run the Application

Click the **"Run"** button in Replit, or run manually:

```bash
streamlit run app.py --server.port=5000 --server.address=0.0.0.0 --server.headless=true
```

The app will be available at the URL provided by Replit (usually shown in the console).

---

## 📱 Features

### 1. Dashboard
- Market overview
- Quick actions
- Platform statistics

### 2. Stock Analysis
- Real-time stock data
- Financial metrics
- Company information
- News and sentiment

### 3. AI Chat
- Natural language queries
- Stock information retrieval
- Investment advice
- Powered by GPT-4

### 4. AI Investment Team
- Multi-agent analysis
- Market Analyst insights
- Fundamental Analyst findings
- Technical Analyst indicators
- CIO consensus recommendations

### 5. Charts
- Candlestick charts
- Technical indicators
- Performance charts
- Customizable timeframes

### 6. Backtesting
- Strategy testing
- Historical performance
- Risk metrics
- Performance visualization

### 7. Reports
- PDF equity research reports
- Comprehensive analysis
- Financial statements
- Investment recommendations

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | ✅ Yes |
| `FINNHUB_API_KEY` | Finnhub API key for market data | ✅ Yes |
| `FMP_API_KEY` | Financial Modeling Prep API key | ⚠️ Optional |
| `SEC_API_KEY` | SEC-API key for filings | ✅ Yes |
| `REDDIT_CLIENT_ID` | Reddit API client ID | ⚠️ Optional |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | ⚠️ Optional |

### File Structure

```
FinRobot/
├── app.py                    # Streamlit web interface
├── main.py                   # Entry point for Replit
├── finrobot/                 # Core FinRobot package
│   ├── agents/              # AI agents (AutoGen)
│   ├── data_source/         # Data source integrations
│   ├── functional/          # Analysis functions
│   └── toolkits.py          # Agent tools
├── config_api_keys          # API keys config (create from example)
├── OAI_CONFIG_LIST          # OpenAI config (create from example)
├── requirements.txt         # Python dependencies
├── .replit                  # Replit configuration
└── replit.nix              # Nix package configuration
```

---

## 🎯 Usage Examples

### Stock Analysis
1. Navigate to "📊 Stock Analysis"
2. Enter a ticker symbol (e.g., AAPL, MSFT, NVDA)
3. View comprehensive analysis

### AI Investment Team
1. Navigate to "🧠 AI Investment Team"
2. Enter ticker and analysis depth
3. Get multi-agent consensus recommendation

### Generate Report
1. Navigate to "📄 Report"
2. Enter ticker and year
3. Download PDF report

---

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "API key not found"
**Solution**: 
1. Check Replit Secrets are set correctly
2. Verify `config_api_keys` file exists and has correct format
3. Check `OAI_CONFIG_LIST` file exists

### Issue: "Port already in use"
**Solution**: The app uses port 5000. If it's busy, change it in `.replit` file:
```
run = "streamlit run app.py --server.port=5001 ..."
```

### Issue: "Streamlit not starting"
**Solution**: 
1. Check Python version: `python --version` (should be 3.11+)
2. Verify Streamlit is installed: `pip install streamlit`
3. Check logs in Replit console

---

## 📚 Documentation

- **Main README**: See `README.md` for full project documentation
- **Implementation Guide**: See `IMPLEMENTATION_GUIDE.md` for setup details
- **CGMF Integration**: See `SERVICE_ORIENTED_INTEGRATION.md` for integration plans

---

## 🔒 Security Notes

- **Never commit API keys** to version control
- Use Replit Secrets for sensitive data
- The `config_api_keys` and `OAI_CONFIG_LIST` files are in `.gitignore`
- Always use HTTPS in production

---

## 🚢 Deployment

### Replit Deployment
1. Click "Deploy" button in Replit
2. Configure deployment settings
3. Set environment variables in Replit Secrets
4. Deploy!

### Custom Domain
1. Go to Replit Settings
2. Configure custom domain
3. Update CORS settings if needed

---

## 📊 Performance

- **Response Time**: 2-5 seconds for stock analysis
- **AI Team Analysis**: 5-15 seconds (multi-agent)
- **Report Generation**: 10-30 seconds (PDF creation)
- **Concurrent Users**: Supports multiple simultaneous users

---

## 🛠️ Development

### Running Tests
```bash
python scripts/test_setup.py
```

### Quick Start Script
```bash
python scripts/quick_start.py
```

### Adding New Features
1. Create feature branch
2. Implement changes
3. Test locally
4. Push to GitHub

---

## 📝 License

See `LICENSE` file for details.

---

## 🤝 Contributing

Contributions welcome! Please read the main `README.md` for contribution guidelines.

---

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Discord**: Join the FinRobot Discord community
- **Documentation**: Check the main README and docs folder

---

## 🎉 What's Next?

- ✅ Multi-agent investment team analysis
- ✅ Real-time stock data integration
- ✅ PDF report generation
- ✅ Backtesting capabilities
- 🔄 CGMF integration (in progress)
- 🔄 Enhanced UI/UX improvements

---

**Built with ❤️ using FinRobot, AutoGen, and Streamlit**

*Last Updated: November 2025*

