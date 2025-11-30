"""
Test Helper Utilities
Provides common functions for testing across all test modules
"""
import os
import sys
import json
import inspect
from typing import Any, Dict, List, Optional
from unittest.mock import Mock, patch, MagicMock
import warnings

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestHelpers:
    """Common test utilities"""
    
    # Known mock/synthetic data patterns
    MOCK_PATTERNS = [
        'mock', 'fake', 'dummy', 'test_data', 'sample', 'example',
        'placeholder', 'synthetic', 'generated', 'random',
        'faker', 'factory_boy', 'mixer'
    ]
    
    # Known fallback patterns
    FALLBACK_PATTERNS = [
        'fallback', 'default', 'backup', 'else:', 'except:', 'pass',
        'return None', 'return {}', 'return []', 'return ""'
    ]
    
    @staticmethod
    def is_mock_data(value: Any) -> bool:
        """Detect if data is mock/synthetic"""
        if value is None:
            return False
        
        value_str = str(value).lower()
        
        # Check for mock patterns
        for pattern in TestHelpers.MOCK_PATTERNS:
            if pattern in value_str:
                return True
        
        # Check for obviously fake data
        if isinstance(value, str):
            if value in ['test', 'mock', 'fake', 'dummy', 'sample', 'example']:
                return True
            # Check for UUID-like patterns that might be generated
            if len(value) == 36 and value.count('-') == 4:  # UUID format
                # This might be real, but flag for review
                pass
        
        return False
    
    @staticmethod
    def detect_silent_failure(func, *args, **kwargs):
        """Detect if a function fails silently"""
        try:
            result = func(*args, **kwargs)
            
            # Check if result is a fallback value
            if result is None:
                return True, "Function returned None (possible silent failure)"
            if result == {}:
                return True, "Function returned empty dict (possible silent failure)"
            if result == []:
                return True, "Function returned empty list (possible silent failure)"
            if result == "":
                return True, "Function returned empty string (possible silent failure)"
            
            return False, None
        except Exception as e:
            # If exception is caught and not re-raised, it's a silent failure
            return True, f"Exception caught but not handled: {str(e)}"
    
    @staticmethod
    def check_for_mock_imports(file_path: str) -> List[str]:
        """Check if file imports mock/synthetic data libraries"""
        mock_imports = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check for faker imports
            if 'from faker' in content or 'import faker' in content:
                mock_imports.append('faker')
            
            # Check for factory_boy
            if 'from factory' in content or 'import factory' in content:
                mock_imports.append('factory_boy')
            
            # Check for mixer
            if 'from mixer' in content or 'import mixer' in content:
                mock_imports.append('mixer')
                
        except Exception as e:
            warnings.warn(f"Could not check file {file_path}: {e}")
        
        return mock_imports
    
    @staticmethod
    def validate_api_response(response: Any, expected_keys: List[str] = None) -> tuple[bool, str]:
        """Validate API response structure"""
        if response is None:
            return False, "Response is None"
        
        if isinstance(response, dict):
            if expected_keys:
                missing = [key for key in expected_keys if key not in response]
                if missing:
                    return False, f"Missing keys in response: {missing}"
            
            # Check for error indicators
            if 'error' in response:
                return False, f"Response contains error: {response.get('error')}"
            
            if 'status' in response and response['status'] == 'error':
                return False, f"Response status is error: {response.get('message', 'Unknown error')}"
        
        return True, "Response is valid"
    
    @staticmethod
    def check_api_key_valid(key: str) -> bool:
        """Check if API key looks valid (not placeholder)"""
        if not key or len(key) < 10:
            return False
        
        invalid_patterns = ['your_', 'placeholder', 'example', 'test', 'mock', 'fake']
        key_lower = key.lower()
        
        for pattern in invalid_patterns:
            if pattern in key_lower:
                return False
        
        return True
    
    @staticmethod
    def get_test_config() -> Dict[str, Any]:
        """Get test configuration"""
        return {
            'test_ticker': 'AAPL',  # Use real ticker for testing
            'test_date_start': '2024-01-01',
            'test_date_end': '2024-12-31',
            'timeout': 30,  # seconds
            'retry_count': 3
        }
    
    @staticmethod
    def check_silent_fallback(code: str) -> List[str]:
        """Check code for silent fallback patterns"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Check for bare except
            if line_stripped.startswith('except:') or line_stripped.startswith('except Exception:'):
                if 'pass' in line or 'return' not in line:
                    issues.append(f"Line {i}: Bare except with no error handling")
            
            # Check for silent None returns
            if 'return None' in line_stripped:
                # Check if there's error handling before
                if i > 1 and 'except' in lines[i-2]:
                    issues.append(f"Line {i}: Silent None return after exception")
            
            # Check for empty dict/list returns
            if 'return {}' in line_stripped or 'return []' in line_stripped:
                if i > 1 and ('except' in lines[i-2] or 'if not' in lines[i-2]):
                    issues.append(f"Line {i}: Silent empty return after condition")
        
        return issues

