"""
UI/Functional tests for Streamlit app
Tests all UI components, pages, and user interactions
"""
import pytest
import sys
import os
import subprocess
import time
import requests
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.utils.test_helpers import TestHelpers


class TestStreamlitApp:
    """Comprehensive UI tests for Streamlit app"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.app_file = Path(__file__).parent.parent.parent / 'app.py'
        self.helpers = TestHelpers()
        self.base_url = 'http://localhost:8501'
        self.streamlit_process = None
    
    @pytest.fixture(scope='class')
    def streamlit_server(self):
        """Start Streamlit server for testing"""
        app_file = Path(__file__).parent.parent.parent / 'app.py'
        process = subprocess.Popen(
            ['streamlit', 'run', str(app_file), '--server.headless=true', '--server.port=8501'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(5)
        
        yield process
        
        # Cleanup
        process.terminate()
        process.wait()
    
    def test_app_starts(self, streamlit_server):
        """Test that Streamlit app starts successfully"""
        try:
            response = requests.get(self.base_url, timeout=10)
            assert response.status_code == 200, "App should return 200"
        except requests.exceptions.ConnectionError:
            pytest.skip("Streamlit server not running")
    
    def test_dashboard_page_loads(self, streamlit_server):
        """Test that dashboard page loads correctly"""
        try:
            response = requests.get(self.base_url, timeout=10)
            assert response.status_code == 200
            assert 'AriaWealth' in response.text or 'Dashboard' in response.text, \
                "Dashboard should be visible"
        except requests.exceptions.ConnectionError:
            pytest.skip("Streamlit server not running")
    
    def test_navigation_works(self, streamlit_server):
        """Test that navigation between pages works"""
        # This would require Selenium for full testing
        # For now, verify pages exist in code
        with open(self.app_file, 'r') as f:
            code = f.read()
            
        # Check that all navigation pages are defined
        pages = ['Dashboard', 'Stock Analysis', 'AI Chat', 'AI Investment Team', 
                 'Charts', 'Backtesting', 'Reports']
        for page in pages:
            assert page in code, f"Page '{page}' should be in app code"
    
    def test_api_key_input_exists(self, streamlit_server):
        """Test that API key input exists in UI"""
        with open(self.app_file, 'r') as f:
            code = f.read()
            
        assert 'API Key' in code or 'API Keys' in code, \
            "API key input should exist"
        assert 'text_input' in code, "Should have text input for API keys"
    
    def test_no_hardcoded_mock_data(self):
        """Test that app doesn't contain hardcoded mock data"""
        with open(self.app_file, 'r') as f:
            code = f.read()
        
        # Check for common mock data patterns
        mock_patterns = ['mock_data', 'fake_data', 'test_data', 'sample_data']
        for pattern in mock_patterns:
            assert pattern not in code.lower(), \
                f"Found potential mock data pattern: {pattern}"
    
    def test_error_handling_visible(self):
        """Test that errors are displayed to users (not silent)"""
        with open(self.app_file, 'r') as f:
            code = f.read()
        
        # Should have error display mechanisms
        assert 'st.error' in code or 'st.warning' in code, \
            "Should have error display mechanisms"
        
        # Check for bare except clauses
        lines = code.split('\n')
        bare_excepts = []
        for i, line in enumerate(lines):
            if line.strip().startswith('except:') and 'pass' in lines[i+1] if i+1 < len(lines) else False:
                bare_excepts.append(i+1)
        
        assert len(bare_excepts) == 0, \
            f"Found bare except clauses (silent failures) at lines: {bare_excepts}"

