# FinRobot Comprehensive Test Suite

## Overview

This test suite provides comprehensive testing for the entire FinRobot application, including:

- **Unit Tests**: Individual module and component testing
- **Integration Tests**: End-to-end workflow testing
- **UI Tests**: Streamlit app component testing
- **API Tests**: Backend endpoint testing (if applicable)
- **Validation Tests**: Mock data detection, silent failure detection

## Test Structure

```
tests/
├── unit/              # Unit tests for individual modules
│   ├── test_data_source_*.py
│   ├── test_functional_*.py
│   └── test_agents_*.py
├── integration/       # Integration tests
│   └── test_end_to_end_workflows.py
├── ui/                # UI/Functional tests
│   └── test_streamlit_app.py
├── api/               # API endpoint tests
│   ├── test_api_endpoints.py
│   └── test_curl_endpoints.sh
├── utils/             # Test utilities
│   └── test_helpers.py
├── conftest.py        # Pytest configuration
├── test_runner.py     # Main test runner
└── run_all_tests.sh   # Bash test runner
```

## Running Tests

### Run All Tests
```bash
# Using Python
python tests/test_runner.py --type all --verbose --coverage

# Using bash script
./tests/run_all_tests.sh
```

### Run Specific Test Types
```bash
# Unit tests only
python tests/test_runner.py --type unit --verbose

# Integration tests
python tests/test_runner.py --type integration

# UI tests
python tests/test_runner.py --type ui

# API tests
python tests/test_runner.py --type api
```

### Run with Coverage
```bash
python tests/test_runner.py --type all --coverage
# View coverage report: htmlcov/index.html
```

### Run in Parallel
```bash
python tests/test_runner.py --type all --parallel
```

## Code Quality Checks

### Check for Mock Data
```bash
python tests/test_runner.py --check-mock
```

### Check for Silent Failures
```bash
python tests/test_runner.py --check-silent
```

## Test Requirements

Install test dependencies:
```bash
pip install -r tests/requirements.txt
```

## Test Coverage

Tests cover:
- ✅ All data source modules (YFinance, Finnhub, SEC, FMP, Reddit)
- ✅ All functional modules (analyzer, charting, quantitative, reportlab, RAG)
- ✅ Agent workflows and library
- ✅ End-to-end workflows
- ✅ UI components
- ✅ API endpoints (if applicable)
- ✅ Mock data detection
- ✅ Silent failure detection

## Test Validation

All tests verify:
1. **Real Data**: No mock/synthetic data is used
2. **No Silent Failures**: Errors are properly handled and reported
3. **Proper Structure**: Responses match expected formats
4. **API Validation**: All API responses are validated
5. **Connection Testing**: All connections are tested

## Continuous Integration

Tests are designed to run in CI/CD pipelines. See `.github/workflows/` for GitHub Actions configuration.

## Debugging Failed Tests

1. Check test output for specific error messages
2. Review HTML test report: `tests/report.html`
3. Check coverage report: `htmlcov/index.html`
4. Run individual test files for detailed debugging:
   ```bash
   pytest tests/unit/test_data_source_yfinance.py -v
   ```

## Adding New Tests

When adding new functionality:
1. Add unit tests in `tests/unit/`
2. Add integration tests in `tests/integration/`
3. Update test runner if needed
4. Ensure tests verify:
   - No mock data
   - No silent failures
   - Proper error handling
   - Real API responses

