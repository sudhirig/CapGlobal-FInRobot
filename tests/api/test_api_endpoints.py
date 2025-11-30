"""
API endpoint tests using curl/httpx
Tests all API endpoints if they exist
"""
import pytest
import httpx
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.utils.test_helpers import TestHelpers


class TestAPIEndpoints:
    """Test API endpoints if they exist"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.base_url = os.environ.get('API_BASE_URL', 'http://localhost:8000')
        self.helpers = TestHelpers()
        self.client = httpx.Client(base_url=self.base_url, timeout=30.0)
    
    def test_api_health_check(self):
        """Test API health check endpoint"""
        try:
            response = self.client.get('/health')
            assert response.status_code == 200, f"Health check failed: {response.status_code}"
            
            # Validate response
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                is_valid, msg = self.helpers.validate_api_response(data)
                assert is_valid, f"Invalid API response: {msg}"
        except httpx.ConnectError:
            pytest.skip("API server not running")
    
    def test_stock_analysis_endpoint(self):
        """Test stock analysis API endpoint if it exists"""
        try:
            response = self.client.post('/api/stock/analyze', json={
                'ticker': 'AAPL',
                'analysis_type': 'comprehensive'
            })
            
            # Should return 200 or 404 (if endpoint doesn't exist)
            assert response.status_code in [200, 404], \
                f"Unexpected status code: {response.status_code}"
            
            if response.status_code == 200:
                data = response.json()
                is_valid, msg = self.helpers.validate_api_response(
                    data, expected_keys=['ticker', 'analysis']
                )
                assert is_valid, f"Invalid API response: {msg}"
                
                # Verify no mock data
                assert not self.helpers.is_mock_data(data), "Response contains mock data"
        except httpx.ConnectError:
            pytest.skip("API server not running")

