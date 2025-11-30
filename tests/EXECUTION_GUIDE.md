# Test Execution Guide

## 🚀 Quick Start

### 1. Install Test Dependencies
```bash
pip install -r tests/requirements.txt
```

### 2. Run Quick Validation
```bash
python tests/quick_validate.py
```
This runs essential checks in seconds.

### 3. Run Full Test Suite
```bash
# All tests with coverage
python tests/test_runner.py --type all --verbose --coverage

# Or use bash script
./tests/run_all_tests.sh
```

## 📋 Test Execution Options

### By Test Type
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# UI tests
pytest tests/ui/ -v

# API tests
pytest tests/api/ -v
```

### With Specific Options
```bash
# With coverage report
pytest tests/unit/ --cov=finrobot --cov-report=html

# In parallel (faster)
pytest tests/unit/ -n auto

# With timeout
pytest tests/unit/ --timeout=300

# Specific test file
pytest tests/unit/test_data_source_yfinance.py -v

# Specific test function
pytest tests/unit/test_data_source_yfinance.py::TestYFinanceUtils::test_get_stock_info_real_api -v
```

## 🔍 Code Quality Checks

### Check for Mock Data
```bash
python tests/test_runner.py --check-mock
```

### Check for Silent Failures
```bash
python tests/test_runner.py --check-silent
```

### Both Checks
```bash
python tests/test_runner.py --check-mock --check-silent
```

## 🌐 API Testing with curl

### Test API Endpoints
```bash
# Set API base URL
export API_BASE_URL=http://localhost:8000

# Run curl tests
./tests/api/test_curl_endpoints.sh
```

### Manual curl Tests
```bash
# Health check
curl http://localhost:8000/health

# Stock analysis
curl -X POST http://localhost:8000/api/stock/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "analysis_type": "comprehensive"}'
```

## 📊 View Test Results

### HTML Report
```bash
open tests/report.html
```

### Coverage Report
```bash
open htmlcov/index.html
```

### Terminal Output
Test results are displayed in real-time during execution.

## ✅ Pre-Deployment Checklist

Before deploying, run:

```bash
# 1. Quick validation
python tests/quick_validate.py

# 2. All unit tests
pytest tests/unit/ -v --cov

# 3. Integration tests
pytest tests/integration/ -v

# 4. Code quality checks
python tests/test_runner.py --check-mock --check-silent

# 5. Full test suite
python tests/test_runner.py --type all --coverage
```

## 🐛 Debugging Failed Tests

### Run with Verbose Output
```bash
pytest tests/unit/test_data_source_yfinance.py -vv -s
```

### Run Single Test
```bash
pytest tests/unit/test_data_source_yfinance.py::TestYFinanceUtils::test_get_stock_info_real_api -vv
```

### Check Test Logs
```bash
# View HTML report
open tests/report.html

# Check coverage
open htmlcov/index.html
```

## 🔧 Environment Setup

### Required Environment Variables
```bash
export OPENAI_API_KEY="your-key"
export FINNHUB_API_KEY="your-key"
export SEC_API_KEY="your-key"
export FMP_API_KEY="your-key"
```

### Optional: Load from Config
Tests will automatically load from:
- `OAI_CONFIG_LIST` (for OpenAI keys)
- `config_api_keys` (for other keys)

## 📈 CI/CD Integration

Tests run automatically in GitHub Actions on:
- Push to master/main
- Pull requests
- Weekly schedule

See `.github/workflows/tests.yml` for details.

## 🎯 Test Coverage Goals

- **Unit Tests**: > 90% coverage
- **Integration Tests**: All critical workflows
- **UI Tests**: All pages and components
- **API Tests**: All endpoints (if applicable)

## 📝 Notes

- Tests use **real API calls** (not mocked)
- Tests verify **no mock/synthetic data**
- Tests detect **silent failures**
- All results are **visible and reviewable**

---

For more details, see `TESTING_GUIDE.md` and `tests/README.md`

