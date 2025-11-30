# FinRobot Comprehensive Testing Guide

## 🎯 Overview

This document describes the comprehensive testing strategy for FinRobot, ensuring all modules, components, APIs, and UI elements are thoroughly tested with **real data** and **no silent failures**.

## 📋 Test Categories

### 1. Unit Tests (`tests/unit/`)
Tests individual modules and components in isolation:
- **Data Source Tests**: YFinance, Finnhub, SEC, FMP, Reddit utilities
- **Functional Tests**: Analyzer, Charting, Quantitative, ReportLab, RAG
- **Agent Tests**: Workflow, Agent Library
- **Issue Detection**: Mock data, silent failures, fallbacks

### 2. Integration Tests (`tests/integration/`)
Tests end-to-end workflows:
- Stock analysis workflows
- Report generation workflows
- Multi-agent interactions
- App integration

### 3. UI Tests (`tests/ui/`)
Tests Streamlit app components:
- Page loading
- Navigation
- User interactions
- Error display
- Component rendering

### 4. API Tests (`tests/api/`)
Tests API endpoints (if applicable):
- Health checks
- Stock analysis endpoints
- Backtest endpoints
- Response validation

## 🚀 Quick Start

### Install Test Dependencies
```bash
pip install -r tests/requirements.txt
```

### Run All Tests
```bash
# Using Python test runner
python tests/test_runner.py --type all --verbose --coverage

# Using bash script
./tests/run_all_tests.sh
```

### Run Specific Test Types
```bash
# Unit tests only
python tests/test_runner.py --type unit

# Integration tests
python tests/test_runner.py --type integration

# UI tests
python tests/test_runner.py --type ui

# API tests
python tests/test_runner.py --type api
```

## 🔍 Code Quality Checks

### Check for Mock/Synthetic Data
```bash
python tests/test_runner.py --check-mock
```
This checks:
- No `faker` imports
- No `factory_boy` imports
- No `mixer` imports
- No hardcoded test data in production code

### Check for Silent Failures
```bash
python tests/test_runner.py --check-silent
```
This checks:
- No bare `except:` clauses
- No silent `return None` after exceptions
- No empty dict/list returns after conditions
- Proper error handling

## 📊 Test Coverage

### Current Coverage
- ✅ Data Source Modules: 100% of public methods
- ✅ Functional Modules: Core functions tested
- ✅ Agent Workflows: Initialization and basic workflows
- ✅ UI Components: Page structure and navigation
- ✅ Integration: End-to-end workflows

### Coverage Report
After running tests with `--coverage`:
```bash
# View HTML report
open htmlcov/index.html

# View terminal report
# (displayed during test run)
```

## 🧪 Test Execution Examples

### Example 1: Test YFinance Module
```bash
pytest tests/unit/test_data_source_yfinance.py -v
```

### Example 2: Test with Real API Keys
```bash
export OPENAI_API_KEY="your-key"
export FINNHUB_API_KEY="your-key"
pytest tests/unit/ -v
```

### Example 3: Test Specific Functionality
```bash
# Test stock data retrieval
pytest tests/unit/test_data_source_yfinance.py::TestYFinanceUtils::test_get_stock_data_real_api -v

# Test chart generation
pytest tests/unit/test_functional_charting.py::TestChartingUtils::test_plot_stock_price_chart_real_data -v
```

## 🔧 Test Configuration

### Environment Variables
Tests use these environment variables (set in CI/CD or locally):
- `OPENAI_API_KEY`: Required for agent tests
- `FINNHUB_API_KEY`: Required for Finnhub tests
- `SEC_API_KEY`: Required for SEC tests
- `FMP_API_KEY`: Optional for FMP tests

### Pytest Configuration
See `pytest.ini` for:
- Test discovery patterns
- Timeout settings
- Coverage configuration
- Markers

## 🐛 Debugging Failed Tests

### 1. Run with Verbose Output
```bash
pytest tests/unit/test_data_source_yfinance.py -vv
```

### 2. Run with Print Statements
```bash
pytest tests/unit/test_data_source_yfinance.py -s
```

### 3. Run Single Test
```bash
pytest tests/unit/test_data_source_yfinance.py::TestYFinanceUtils::test_get_stock_info_real_api -v
```

### 4. Check Test Reports
```bash
# HTML report
open tests/report.html

# Coverage report
open htmlcov/index.html
```

## ✅ Test Validation Checklist

Before marking tests as complete, verify:

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] UI tests verify components render
- [ ] No mock data detected
- [ ] No silent failures detected
- [ ] API responses validated
- [ ] Error handling verified
- [ ] Coverage > 80%
- [ ] All connections tested
- [ ] Real data used (not synthetic)

## 🔗 API Testing with curl

### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

### Test Stock Analysis
```bash
curl -X POST http://localhost:8000/api/stock/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "analysis_type": "comprehensive"}'
```

### Run All curl Tests
```bash
./tests/api/test_curl_endpoints.sh
```

## 📝 Adding New Tests

When adding new functionality:

1. **Create Unit Test**
   ```python
   # tests/unit/test_new_module.py
   def test_new_function_real_data():
       result = NewModule.new_function("real_input")
       assert not helpers.is_mock_data(result)
       assert result is not None
   ```

2. **Add Integration Test**
   ```python
   # tests/integration/test_new_workflow.py
   def test_new_workflow_end_to_end():
       # Test complete workflow
   ```

3. **Update Test Runner**
   - Tests are auto-discovered
   - No manual registration needed

## 🚨 Common Issues

### Issue: Tests Fail with "API Key Not Found"
**Solution**: Set environment variables or use `pytest --skip-missing-api-keys`

### Issue: Tests Timeout
**Solution**: Increase timeout in `pytest.ini` or use `--timeout=600`

### Issue: Mock Data Detected
**Solution**: Remove any `faker`, `factory_boy`, or `mixer` imports from production code

### Issue: Silent Failures Detected
**Solution**: Replace bare `except:` with proper error handling and logging

## 📈 Continuous Integration

Tests run automatically on:
- Push to master/main
- Pull requests
- Weekly schedule (Sundays)

See `.github/workflows/tests.yml` for CI configuration.

## 🎓 Best Practices

1. **Always Use Real Data**: Never use mock data in production code
2. **Explicit Error Handling**: Never use bare `except:` clauses
3. **Validate Responses**: Always validate API responses
4. **Test Edge Cases**: Test invalid inputs, missing data, etc.
5. **Document Tests**: Clear test names and docstrings
6. **Keep Tests Fast**: Unit tests should be < 1 second each
7. **Isolate Tests**: Tests should not depend on each other

## 📞 Support

For test-related issues:
1. Check test output for specific errors
2. Review test reports
3. Run tests individually to isolate issues
4. Check environment variables are set correctly

---

**Last Updated**: November 2025  
**Test Framework**: pytest  
**Coverage Tool**: pytest-cov

