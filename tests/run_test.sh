#!/bin/bash
set -e

# Colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
VERBOSE=0
TEST_IDS=("basic_logging" "named_loggers" "level_filtering" "global_level" "disable_enable" "debug_vars")
SELECTED_TESTS=()

# Help function
show_help() {
  echo "Usage: $0 [options] [test_ids]"
  echo
  echo "Options:"
  echo "  -h, --help     Show this help message"
  echo "  -v, --verbose  Show verbose output (including commands being run)"
  echo
  echo "Available tests:"
  for test in "${TEST_IDS[@]}"; do
    echo "  - $test"
  done
  echo
  echo "If no test_ids are provided, all tests will be run."
  exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      show_help
      ;;
    -v|--verbose)
      VERBOSE=1
      shift
      ;;
    *)
      SELECTED_TESTS+=("$1")
      shift
      ;;
  esac
done

# If no tests specified, run all tests
if [ ${#SELECTED_TESTS[@]} -eq 0 ]; then
  SELECTED_TESTS=("${TEST_IDS[@]}")
fi

# Set verbosity
if [ $VERBOSE -eq 1 ]; then
  set -x
fi

echo -e "${BLUE}=== Running tests ===${NC}"

cd src

exit_code=0
pass_count=0
fail_count=0
total_tests=${#SELECTED_TESTS[@]}

# Run tests
for TEST_ID in "${SELECTED_TESTS[@]}"; do
  if [[ ! " ${TEST_IDS[*]} " =~ " ${TEST_ID} " ]]; then
    echo -e "${YELLOW}Warning: Unknown test '${TEST_ID}', skipping${NC}"
    continue
  fi

  echo -e "${BLUE}Testing ${TEST_ID}...${NC}"
  start_time=$(date +%s.%N)
  
  # Run the test function
  PYTHONPATH=".:../.." python tests/test_functions.py test ${TEST_ID}
  
  # Run the assertion function
  PYTHONPATH=".:../.." python tests/test_functions.py assert ${TEST_ID}
  TEST_RESULT=$?
  
  end_time=$(date +%s.%N)
  duration=$(echo "$end_time - $start_time" | bc)
  
  if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Test ${TEST_ID} passed (${duration}s)${NC}"
    pass_count=$((pass_count + 1))
  else
    echo -e "${RED}✗ Test ${TEST_ID} failed with exit code ${TEST_RESULT} (${duration}s)${NC}"
    fail_count=$((fail_count + 1))
    exit_code=1
  fi
done

# Print summary
echo
echo -e "${BLUE}=== Test Summary ===${NC}"
echo -e "Total tests: ${total_tests}"
echo -e "${GREEN}Passed: ${pass_count}${NC}"
if [ $fail_count -gt 0 ]; then
  echo -e "${RED}Failed: ${fail_count}${NC}"
else
  echo -e "Failed: 0"
fi

exit $exit_code
