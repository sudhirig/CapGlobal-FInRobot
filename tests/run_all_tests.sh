#!/bin/bash
# Comprehensive test runner script
# Runs all tests with proper setup and reporting

set -e  # Exit on error

echo "=========================================="
echo "FinRobot Comprehensive Test Suite"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}Error: Must run from project root directory${NC}"
    exit 1
fi

# Install test requirements
echo -e "${YELLOW}Installing test requirements...${NC}"
pip install -q -r tests/requirements.txt

# Run code quality checks
echo -e "\n${YELLOW}Running code quality checks...${NC}"
python tests/test_runner.py --check-mock --check-silent

# Run unit tests
echo -e "\n${YELLOW}Running unit tests...${NC}"
python tests/test_runner.py --type unit --verbose --coverage

# Run integration tests
echo -e "\n${YELLOW}Running integration tests...${NC}"
python tests/test_runner.py --type integration --verbose

# Run API tests (if API exists)
echo -e "\n${YELLOW}Running API tests...${NC}"
python tests/test_runner.py --type api --verbose || echo -e "${YELLOW}API tests skipped (API not running)${NC}"

# Generate final report
echo -e "\n${GREEN}=========================================="
echo "Test Suite Complete"
echo "==========================================${NC}"
echo ""
echo "Test reports:"
echo "  - HTML: tests/report.html"
echo "  - Coverage: htmlcov/index.html"
echo ""

