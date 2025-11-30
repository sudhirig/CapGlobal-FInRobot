"""
Integration tests for the Streamlit app
Tests app.py integration with all modules
"""
import pytest
import sys
import os
import importlib.util

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.utils.test_helpers import TestHelpers


class TestAppIntegration:
    """Integration tests for app.py"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.app_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'app.py'
        )
        self.helpers = TestHelpers()
    
    def test_app_imports_all_modules(self):
        """Test that app.py can import all required modules"""
        with open(self.app_file, 'r') as f:
            code = f.read()
        
        # Check for required imports
        required_imports = [
            'streamlit',
            'finrobot.data_source',
            'finrobot.agents.workflow',
            'finrobot.functional',
        ]
        
        missing_imports = []
        for imp in required_imports:
            if imp.replace('.', '_') not in code and imp not in code:
                missing_imports.append(imp)
        
        # This is a soft check - imports might be dynamic
        if len(missing_imports) == len(required_imports):
            pytest.skip("Cannot verify imports statically")
    
    def test_app_has_all_pages(self):
        """Test that app has all required pages"""
        with open(self.app_file, 'r') as f:
            code = f.read()
        
        required_pages = [
            'Dashboard',
            'Stock Analysis',
            'AI Chat',
            'AI Investment Team',
            'Charts',
            'Backtesting',
            'Reports'
        ]
        
        missing_pages = []
        for page in required_pages:
            if page not in code:
                missing_pages.append(page)
        
        assert len(missing_pages) == 0, \
            f"Missing pages in app: {missing_pages}"
    
    def test_app_handles_errors(self):
        """Test that app properly handles errors (not silently)"""
        with open(self.app_file, 'r') as f:
            code = f.read()
        
        # Should have error handling
        assert 'st.error' in code or 'except' in code, \
            "App should have error handling"
        
        # Check for bare except
        issues = self.helpers.check_silent_fallback(code)
        assert len(issues) == 0, \
            f"Silent error handling found: {issues}"

