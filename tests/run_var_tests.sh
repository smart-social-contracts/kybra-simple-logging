#!/bin/bash
set -e

# Colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Running Variable Storage Tests ===${NC}"

cd src

# Run all variable storage tests
echo -e "${BLUE}Running all variable storage tests...${NC}"
start_time=$(date +%s.%N)

PYTHONPATH=".:../.." python tests/test_vars.py
TEST_RESULT=$?

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)

if [ $TEST_RESULT -eq 0 ]; then
  echo -e "${GREEN}✓ Variable storage tests passed (${duration}s)${NC}"
  exit 0
else
  echo -e "${RED}✗ Variable storage tests failed with exit code ${TEST_RESULT} (${duration}s)${NC}"
  exit 1
fi
