"""
Tests to detect common issues: mock data, silent failures, fallbacks
Runs across entire codebase
"""
import pytest
import os
import sys
import inspect
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.utils.test_helpers import TestHelpers


class TestCodebaseIssues:
    """Tests to detect issues across entire codebase"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.helpers = TestHelpers()
        self.project_root = Path(__file__).parent.parent.parent
        self.finrobot_dir = self.project_root / 'finrobot'
    
    def test_no_mock_data_imports(self):
        """Test that no modules import mock data libraries"""
        issues = []
        
        for root, dirs, files in os.walk(self.finrobot_dir):
            # Skip test files and cache
            if 'test' in root or '__pycache__' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    mock_imports = self.helpers.check_for_mock_imports(file_path)
                    if mock_imports:
                        issues.append(f"{file_path}: {mock_imports}")
        
        assert len(issues) == 0, \
            f"Mock data libraries found in codebase:\n" + "\n".join(issues)
    
    def test_no_silent_failures(self):
        """Test that codebase doesn't have silent failure patterns"""
        issues = []
        
        for root, dirs, files in os.walk(self.finrobot_dir):
            if 'test' in root or '__pycache__' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        code = f.read()
                        file_issues = self.helpers.check_silent_fallback(code)
                        if file_issues:
                            issues.extend([f"{file_path}: {issue}" for issue in file_issues])
        
        # Report first 20 issues
        if issues:
            error_msg = "Silent failure patterns found:\n" + "\n".join(issues[:20])
            if len(issues) > 20:
                error_msg += f"\n... and {len(issues) - 20} more issues"
            pytest.fail(error_msg)
    
    def test_no_random_data_generation(self):
        """Test that random is not used for data generation"""
        issues = []
        
        for root, dirs, files in os.walk(self.finrobot_dir):
            if 'test' in root or '__pycache__' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            # Check for random usage with data-related variables
                            if 'random' in line.lower():
                                lower_line = line.lower()
                                # Check if random is used for actual data (not just selection)
                                data_keywords = ['price', 'value', 'data', 'amount', 'quantity', 
                                                'revenue', 'profit', 'loss', 'return']
                                if any(keyword in lower_line for keyword in data_keywords):
                                    # Check if it's actually generating data (not just selecting)
                                    if 'random.' in lower_line and ('uniform' in lower_line or 
                                                                    'randint' in lower_line or
                                                                    'choice' in lower_line):
                                        issues.append(f"{file_path}:{i} - {line.strip()}")
        
        if issues:
            error_msg = "Random data generation found:\n" + "\n".join(issues[:10])
            pytest.fail(error_msg)
    
    def test_api_keys_not_hardcoded(self):
        """Test that API keys are not hardcoded"""
        issues = []
        
        for root, dirs, files in os.walk(self.finrobot_dir):
            if 'test' in root or '__pycache__' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        # Check for hardcoded API keys (long strings starting with sk-)
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if 'sk-' in line and len(line) > 50:
                                # Might be a hardcoded key
                                if '=' in line or ':' in line:
                                    issues.append(f"{file_path}:{i} - Possible hardcoded API key")
        
        if issues:
            error_msg = "Possible hardcoded API keys found:\n" + "\n".join(issues[:10])
            pytest.fail(error_msg)
    
    def test_all_modules_importable(self):
        """Test that all modules can be imported without errors"""
        import importlib
        
        modules_to_test = [
            'finrobot.data_source.yfinance_utils',
            'finrobot.data_source.finnhub_utils',
            'finrobot.data_source.sec_utils',
            'finrobot.functional.analyzer',
            'finrobot.functional.charting',
            'finrobot.functional.quantitative',
            'finrobot.agents.workflow',
            'finrobot.agents.agent_library',
        ]
        
        failed_imports = []
        for module_name in modules_to_test:
            try:
                importlib.import_module(module_name)
            except Exception as e:
                failed_imports.append(f"{module_name}: {str(e)}")
        
        assert len(failed_imports) == 0, \
            f"Failed to import modules:\n" + "\n".join(failed_imports)

