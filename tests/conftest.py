"""
Pytest configuration and fixtures
"""
import os
import sys
import pytest
import warnings
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Suppress warnings during tests
warnings.filterwarnings("ignore")


@pytest.fixture(scope="session")
def test_config():
    """Test configuration fixture"""
    return {
        'test_ticker': 'AAPL',
        'test_date_start': '2024-01-01',
        'test_date_end': '2024-12-31',
        'timeout': 30,
    }


@pytest.fixture(scope="session")
def api_keys():
    """API keys fixture - checks for real keys"""
    keys = {}
    
    # Check environment variables
    openai_key = os.environ.get('OPENAI_API_KEY', '')
    finnhub_key = os.environ.get('FINNHUB_API_KEY', '')
    sec_key = os.environ.get('SEC_API_KEY', '')
    fmp_key = os.environ.get('FMP_API_KEY', '')
    
    # Validate keys are not placeholders
    from tests.utils.test_helpers import TestHelpers
    
    if TestHelpers.check_api_key_valid(openai_key):
        keys['OPENAI_API_KEY'] = openai_key
    else:
        pytest.skip("OPENAI_API_KEY not set or invalid")
    
    if TestHelpers.check_api_key_valid(finnhub_key):
        keys['FINNHUB_API_KEY'] = finnhub_key
    else:
        warnings.warn("FINNHUB_API_KEY not set - some tests may be skipped")
    
    if TestHelpers.check_api_key_valid(sec_key):
        keys['SEC_API_KEY'] = sec_key
    
    if TestHelpers.check_api_key_valid(fmp_key):
        keys['FMP_API_KEY'] = fmp_key
    
    return keys


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment before each test"""
    # Store original env
    original_env = os.environ.copy()
    yield
    # Restore original env
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_api_response():
    """Mock API response fixture"""
    def _create_response(status_code=200, data=None, error=None):
        response = Mock()
        response.status_code = status_code
        if error:
            response.json.return_value = {'error': error}
            response.raise_for_status.side_effect = Exception(error)
        else:
            response.json.return_value = data or {}
        return response
    return _create_response

