"""
Integration tests for end-to-end workflows
Tests complete workflows from data retrieval to report generation
"""
import pytest
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from finrobot.data_source import YFinanceUtils, FinnHubUtils
from finrobot.functional.analyzer import ReportAnalysisUtils
from finrobot.functional.charting import ReportChartUtils
from tests.utils.test_helpers import TestHelpers


class TestEndToEndWorkflows:
    """End-to-end workflow tests"""
    
    @pytest.fixture(autouse=True)
    def setup(self, api_keys):
        """Setup for each test"""
        self.test_ticker = 'AAPL'
        self.test_fyear = '2023'
        self.helpers = TestHelpers()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_stock_analysis_workflow(self):
        """Test complete stock analysis workflow"""
        # Step 1: Get stock info
        stock_info = YFinanceUtils.get_stock_info(self.test_ticker)
        assert stock_info is not None, "Stock info should be retrieved"
        assert not self.helpers.is_mock_data(stock_info), "Stock info contains mock data"
        
        # Step 2: Get financial statements
        income_stmt = YFinanceUtils.get_income_stmt(self.test_ticker)
        assert income_stmt is not None, "Income statement should be retrieved"
        assert not income_stmt.empty, "Income statement should not be empty"
        
        balance_sheet = YFinanceUtils.get_balance_sheet(self.test_ticker)
        assert balance_sheet is not None, "Balance sheet should be retrieved"
        
        # Step 3: Analyze financials
        analysis_path = os.path.join(self.temp_dir, 'analysis.txt')
        result = ReportAnalysisUtils.analyze_income_stmt(
            self.test_ticker, self.test_fyear, analysis_path
        )
        assert os.path.exists(analysis_path), "Analysis should be saved"
    
    def test_report_generation_workflow(self):
        """Test complete report generation workflow"""
        # This would test the full PDF report generation
        # For now, test that all components work together
        pass  # Will be implemented with ReportLabUtils tests

