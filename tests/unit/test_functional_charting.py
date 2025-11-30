"""
Unit tests for charting functional modules
Tests MplFinanceUtils and ReportChartUtils
"""
import pytest
import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from finrobot.functional.charting import MplFinanceUtils, ReportChartUtils
from tests.utils.test_helpers import TestHelpers


class TestChartingUtils:
    """Comprehensive tests for charting utilities"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.test_ticker = 'AAPL'
        self.helpers = TestHelpers()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_plot_stock_price_chart_real_data(self):
        """Test plot_stock_price_chart with real data"""
        save_path = os.path.join(self.temp_dir, 'test_chart.png')
        
        result = MplFinanceUtils.plot_stock_price_chart(
            self.test_ticker,
            '2024-01-01',
            '2024-12-31',
            save_path,
            type='candle'
        )
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            MplFinanceUtils.plot_stock_price_chart,
            self.test_ticker, '2024-01-01', '2024-12-31', save_path
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify file was created
        assert os.path.exists(save_path), "Chart file should be created"
        assert os.path.getsize(save_path) > 0, "Chart file should not be empty"
    
    def test_get_share_performance_real_data(self):
        """Test get_share_performance with real data"""
        save_path = os.path.join(self.temp_dir, 'performance.png')
        filing_date = '2024-06-30'
        
        result = ReportChartUtils.get_share_performance(
            self.test_ticker, filing_date, save_path
        )
        
        # Check for silent failure
        is_silent, msg = self.helpers.detect_silent_failure(
            ReportChartUtils.get_share_performance,
            self.test_ticker, filing_date, save_path
        )
        assert not is_silent, f"Silent failure detected: {msg}"
        
        # Verify file was created
        assert os.path.exists(save_path), "Performance chart should be created"
    
    def test_no_silent_fallbacks(self):
        """Test that methods don't use silent fallbacks"""
        import inspect
        source_file = inspect.getfile(MplFinanceUtils.plot_stock_price_chart)
        
        with open(source_file, 'r') as f:
            code = f.read()
        
        issues = self.helpers.check_silent_fallback(code)
        assert len(issues) == 0, f"Silent fallback patterns found: {issues}"

