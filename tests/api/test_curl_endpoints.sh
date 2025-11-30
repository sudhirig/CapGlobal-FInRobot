#!/bin/bash
# Curl-based API endpoint tests
# Tests all API endpoints using curl commands

set -e

BASE_URL="${API_BASE_URL:-http://localhost:8000}"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "API Endpoint Tests (curl)"
echo "=========================================="
echo ""

# Test health endpoint
echo -e "${YELLOW}Testing /health endpoint...${NC}"
if curl -f -s "${BASE_URL}/health" > /dev/null; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    curl -s "${BASE_URL}/health" | jq '.' || echo "Response: $(curl -s ${BASE_URL}/health)"
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "Note: API server may not be running"
fi

echo ""

# Test stock analysis endpoint
echo -e "${YELLOW}Testing /api/stock/analyze endpoint...${NC}"
response=$(curl -s -X POST "${BASE_URL}/api/stock/analyze" \
    -H "Content-Type: application/json" \
    -d '{"ticker": "AAPL", "analysis_type": "comprehensive"}')

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Stock analysis endpoint responded${NC}"
    echo "$response" | jq '.' || echo "$response"
else
    echo -e "${YELLOW}⚠️  Stock analysis endpoint not available${NC}"
fi

echo ""

# Test backtest endpoint
echo -e "${YELLOW}Testing /api/stock/backtest endpoint...${NC}"
response=$(curl -s -X POST "${BASE_URL}/api/stock/backtest" \
    -H "Content-Type: application/json" \
    -d '{
        "ticker": "AAPL",
        "strategy": "SMA Crossover",
        "start_date": "2024-01-01",
        "end_date": "2024-06-30"
    }')

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backtest endpoint responded${NC}"
    echo "$response" | jq '.' || echo "$response"
else
    echo -e "${YELLOW}⚠️  Backtest endpoint not available${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "API Tests Complete"
echo "==========================================${NC}"

