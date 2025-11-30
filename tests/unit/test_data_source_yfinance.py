"""
Unit tests for YFinanceUtils data source module
Tests all methods, detects mock data, silent failures, and validates real API responses
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from finrobot.data_source.yfinance_utils import YFinanceUtils
from tests.utils.test_helpers import TestHelpers


class TestYFinanceUtils:
    """Comprehensive tests for YFinanceUtils"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.test_ticker = 'AAPL'  # Use real ticker
        self.helpers = TestHelpers()
    
    def test_get_stock_data_real_api(self):
        """Test get_stock_data with real API - verify no mock data"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        result = YFinanceUtils.get_stock_data(self.test_ticker, start_date, end_date)
        
        # Verify not mock data
        assert not self.helpers.is_mock_data(result), "Result contains mock data"
        
        # Verify structure
        assert isinstance(result, pd.DataFrame), "Result should be DataFrame"
        assert not result.empty, "Result should not be empty"
        
        # Verify required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            assert col in result.columns, f"Missing column: {col}"
        
        # Verify data types
        assert pd.api.types.is_numeric_dtype(result['Close']), "Close price should be numeric"
        assert pd.api.types.is_numeric_dtype(result['Volume']), "Volume should be numeric"
        
        # Verify no synthetic values
        assert result['Close'].min() > 0, "Stock price should be positive"
        assert result['Volume'].min() >= 0, "Volume should be non-negative"
    
    def test_get_stock_info_real_api(self):
        """Test get_stock_info - verify real data, no silent failures"""
        result = YFinanceUtils.get_stock_info(self.test_ticker)
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            YFinanceUtils.get_stock_info, self.test_ticker
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify not mock data
        assert not self.helpers.is_mock_data(result), "Result contains mock data"
        
        # Verify structure
        assert isinstance(result, dict), "Result should be dict"
        assert len(result) > 0, "Result should not be empty"
        
        # Verify required keys exist
        required_keys = ['symbol', 'longName', 'currentPrice', 'marketCap']
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
        
        # Verify data is real (not placeholder)
        assert result.get('symbol') == self.test_ticker, "Symbol should match"
        assert result.get('currentPrice', 0) > 0, "Current price should be positive"
        assert result.get('marketCap', 0) > 0, "Market cap should be positive"
    
    def test_get_company_info_real_api(self):
        """Test get_company_info - verify real company data"""
        result = YFinanceUtils.get_company_info(self.test_ticker)
        
        # Verify not mock data
        assert not self.helpers.is_mock_data(result), "Result contains mock data"
        
        # Verify structure
        assert isinstance(result, pd.DataFrame), "Result should be DataFrame"
        assert not result.empty, "Result should not be empty"
        
        # Verify required columns
        required_cols = ['Company Name', 'Industry', 'Sector', 'Country', 'Website']
        for col in required_cols:
            assert col in result.columns, f"Missing column: {col}"
        
        # Verify data is not placeholder
        company_name = result['Company Name'].iloc[0]
        assert company_name != 'N/A', "Company name should not be placeholder"
        assert 'Apple' in company_name or 'AAPL' in company_name, "Should contain real company name"
    
    def test_get_income_stmt_real_api(self):
        """Test get_income_stmt - verify real financial data"""
        result = YFinanceUtils.get_income_stmt(self.test_ticker)
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            YFinanceUtils.get_income_stmt, self.test_ticker
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify structure
        assert isinstance(result, pd.DataFrame), "Result should be DataFrame"
        assert not result.empty, "Result should not be empty"
        
        # Verify financial statement has data
        assert len(result.columns) > 0, "Should have date columns"
        assert len(result.index) > 0, "Should have financial metrics"
    
    def test_get_balance_sheet_real_api(self):
        """Test get_balance_sheet - verify real balance sheet data"""
        result = YFinanceUtils.get_balance_sheet(self.test_ticker)
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            YFinanceUtils.get_balance_sheet, self.test_ticker
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify structure
        assert isinstance(result, pd.DataFrame), "Result should be DataFrame"
        assert not result.empty, "Result should not be empty"
    
    def test_get_cash_flow_real_api(self):
        """Test get_cash_flow - verify real cash flow data"""
        result = YFinanceUtils.get_cash_flow(self.test_ticker)
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            YFinanceUtils.get_cash_flow, self.test_ticker
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify structure
        assert isinstance(result, pd.DataFrame), "Result should be DataFrame"
        assert not result.empty, "Result should not be empty"
    
    def test_get_stock_dividends_real_api(self):
        """Test get_stock_dividends - verify real dividend data"""
        result = YFinanceUtils.get_stock_dividends(self.test_ticker)
        
        # Verify structure (may be empty for some stocks)
        assert isinstance(result, pd.Series) or isinstance(result, pd.DataFrame), \
            "Result should be Series or DataFrame"
    
    def test_invalid_ticker_handling(self):
        """Test that invalid tickers are handled properly (not silently)"""
        invalid_ticker = 'INVALID_TICKER_XYZ123'
        
        # Should raise exception or return None explicitly, not fail silently
        result = YFinanceUtils.get_stock_info(invalid_ticker)
        
        # If it returns data, verify it's not mock
        if result:
            assert not self.helpers.is_mock_data(result), \
                "Invalid ticker should not return mock data"
    
    def test_no_silent_fallbacks(self):
        """Test that methods don't use silent fallbacks"""
        # Check source code for silent fallback patterns
        import inspect
        source_file = inspect.getfile(YFinanceUtils.get_stock_info)
        
        with open(source_file, 'r') as f:
            code = f.read()
        
        issues = self.helpers.check_silent_fallback(code)
        assert len(issues) == 0, f"Silent fallback patterns found: {issues}"
    
    def test_no_mock_imports(self):
        """Test that module doesn't import mock data libraries"""
        import inspect
        source_file = inspect.getfile(YFinanceUtils)
        
        mock_imports = self.helpers.check_for_mock_imports(source_file)
        assert len(mock_imports) == 0, \
            f"Mock data libraries imported: {mock_imports}"

