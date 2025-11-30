"""
Unit tests for ReportAnalysisUtils functional module
Tests all analysis methods, detects mock data, silent failures
"""
import pytest
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from finrobot.functional.analyzer import ReportAnalysisUtils
from tests.utils.test_helpers import TestHelpers


class TestReportAnalysisUtils:
    """Comprehensive tests for ReportAnalysisUtils"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.test_ticker = 'AAPL'
        self.test_fyear = '2023'
        self.helpers = TestHelpers()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_analyze_income_stmt_real_data(self):
        """Test analyze_income_stmt with real data"""
        save_path = os.path.join(self.temp_dir, 'income_test.txt')
        
        result = ReportAnalysisUtils.analyze_income_stmt(
            self.test_ticker, self.test_fyear, save_path
        )
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            ReportAnalysisUtils.analyze_income_stmt,
            self.test_ticker, self.test_fyear, save_path
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify file was created
        assert os.path.exists(save_path), "Analysis file should be created"
        
        # Verify file has content
        with open(save_path, 'r') as f:
            content = f.read()
            assert len(content) > 0, "Analysis should have content"
            assert not self.helpers.is_mock_data(content), "Content contains mock data"
    
    def test_analyze_balance_sheet_real_data(self):
        """Test analyze_balance_sheet with real data"""
        save_path = os.path.join(self.temp_dir, 'balance_test.txt')
        
        result = ReportAnalysisUtils.analyze_balance_sheet(
            self.test_ticker, self.test_fyear, save_path
        )
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            ReportAnalysisUtils.analyze_balance_sheet,
            self.test_ticker, self.test_fyear, save_path
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify file was created
        assert os.path.exists(save_path), "Analysis file should be created"
    
    def test_no_silent_fallbacks(self):
        """Test that methods don't use silent fallbacks"""
        import inspect
        source_file = inspect.getfile(ReportAnalysisUtils.analyze_income_stmt)
        
        with open(source_file, 'r') as f:
            code = f.read()
        
        issues = self.helpers.check_silent_fallback(code)
        assert len(issues) == 0, f"Silent fallback patterns found: {issues}"

