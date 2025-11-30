"""
Unit tests for FinnHubUtils data source module
Tests all methods, detects mock data, silent failures, and validates real API responses
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from finrobot.data_source.finnhub_utils import FinnHubUtils
from tests.utils.test_helpers import TestHelpers


class TestFinnHubUtils:
    """Comprehensive tests for FinnHubUtils"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_keys):
        """Setup for each test"""
        self.test_ticker = 'AAPL'
        self.helpers = TestHelpers()
        
        # Check if API key is available
        if 'FINNHUB_API_KEY' not in api_keys:
            pytest.skip("FINNHUB_API_KEY not available")
    
    def test_get_company_profile_real_api(self):
        """Test get_company_profile with real API - verify no mock data"""
        result = FinnHubUtils.get_company_profile(self.test_ticker)
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            FinnHubUtils.get_company_profile, self.test_ticker
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify not mock data
        assert not self.helpers.is_mock_data(result), "Result contains mock data"
        
        # Verify structure
        assert isinstance(result, str), "Result should be string"
        assert len(result) > 0, "Result should not be empty"
        
        # Verify contains real company information
        assert self.test_ticker in result or 'Apple' in result, \
            "Should contain real company information"
        
        # Verify no placeholder text
        assert 'N/A' not in result or result.count('N/A') < 3, \
            "Should not have excessive placeholder values"
    
    def test_get_company_news_real_api(self):
        """Test get_company_news - verify real news data"""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        result = FinnHubUtils.get_company_news(
            self.test_ticker, start_date, end_date, max_news_num=5
        )
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            FinnHubUtils.get_company_news, self.test_ticker, start_date, end_date
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify structure
        assert isinstance(result, pd.DataFrame), "Result should be DataFrame"
        
        # If empty, that's okay (no news in period), but verify it's not mock
        if not result.empty:
            # Verify required columns
            required_cols = ['date', 'headline', 'summary']
            for col in required_cols:
                assert col in result.columns, f"Missing column: {col}"
            
            # Verify not mock data
            for idx, row in result.iterrows():
                assert not self.helpers.is_mock_data(row['headline']), \
                    f"Headline contains mock data: {row['headline']}"
    
    def test_get_basic_financials_real_api(self):
        """Test get_basic_financials - verify real financial data"""
        result = FinnHubUtils.get_basic_financials(self.test_ticker, 'quarterly')
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            FinnHubUtils.get_basic_financials, self.test_ticker, 'quarterly'
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify structure
        assert result is not None, "Result should not be None"
        
        # If dict, verify it has real data
        if isinstance(result, dict):
            assert len(result) > 0, "Result should not be empty"
            assert not self.helpers.is_mock_data(result), "Result contains mock data"
    
    def test_no_random_data_generation(self):
        """Test that module doesn't use random data generation"""
        import inspect
        source_file = inspect.getfile(FinnHubUtils)
        
        with open(source_file, 'r') as f:
            code = f.read()
        
        # Check for random usage (should only be for non-data purposes)
        if 'import random' in code or 'from random' in code:
            # Check if random is used for data generation
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if 'random' in line.lower() and ('data' in line.lower() or 'price' in line.lower() or 'value' in line.lower()):
                    pytest.fail(f"Random used for data generation at line {i+1}: {line.strip()}")
    
    def test_no_silent_fallbacks(self):
        """Test that methods don't use silent fallbacks"""
        import inspect
        source_file = inspect.getfile(FinnHubUtils.get_company_profile)
        
        with open(source_file, 'r') as f:
            code = f.read()
        
        issues = self.helpers.check_silent_fallback(code)
        assert len(issues) == 0, f"Silent fallback patterns found: {issues}"
    
    def test_api_key_validation(self):
        """Test that API key is validated before use"""
        import inspect
        source_file = inspect.getfile(FinnHubUtils)
        
        with open(source_file, 'r') as f:
            code = f.read()
        
        # Should check for API key before making calls
        assert 'FINNHUB_API_KEY' in code, "Should check for FINNHUB_API_KEY"
        assert 'os.environ.get' in code or 'os.environ[' in code, \
            "Should check environment variable"

