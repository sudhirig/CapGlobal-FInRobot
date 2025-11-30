"""
Unit tests for SECUtils data source module
Tests all methods, detects mock data, silent failures, and validates real API responses
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from finrobot.data_source.sec_utils import SECUtils
from tests.utils.test_helpers import TestHelpers


class TestSECUtils:
    """Comprehensive tests for SECUtils"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_keys):
        """Setup for each test"""
        self.test_ticker = 'AAPL'
        self.test_fyear = '2023'
        self.helpers = TestHelpers()
        
        # Check if API key is available
        if 'SEC_API_KEY' not in api_keys:
            pytest.skip("SEC_API_KEY not available")
    
    def test_get_10k_metadata_real_api(self):
        """Test get_10k_metadata with real API"""
        start_date = '2023-01-01'
        end_date = '2023-12-31'
        
        result = SECUtils.get_10k_metadata(self.test_ticker, start_date, end_date)
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            SECUtils.get_10k_metadata, self.test_ticker, start_date, end_date
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify not mock data
        if result:
            assert not self.helpers.is_mock_data(result), "Result contains mock data"
    
    def test_get_10k_section_real_api(self):
        """Test get_10k_section - verify real SEC filing data"""
        result = SECUtils.get_10k_section(self.test_ticker, self.test_fyear, '1')
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            SECUtils.get_10k_section, self.test_ticker, self.test_fyear, '1'
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify structure
        if result:
            assert isinstance(result, str), "Result should be string"
            assert len(result) > 100, "Result should have substantial content"
            assert not self.helpers.is_mock_data(result), "Result contains mock data"
    
    def test_no_silent_fallbacks(self):
        """Test that methods don't use silent fallbacks"""
        import inspect
        source_file = inspect.getfile(SECUtils.get_10k_metadata)
        
        with open(source_file, 'r') as f:
            code = f.read()
        
        issues = self.helpers.check_silent_fallback(code)
        assert len(issues) == 0, f"Silent fallback patterns found: {issues}"

