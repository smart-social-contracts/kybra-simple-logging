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
TEST_IDS=("basic_logging" "named_loggers" "level_filtering" "global_level" "disable_enable")
VAR_TEST_TYPES=("save_load" "complex_objects" "nonexistent" "list_vars" "overwrite" "all")
SELECTED_VAR_TESTS=()
SELECTED_TESTS=()

# Help function
show_help() {
  echo "Usage: $0 [options] [test_ids] [var_tests]"
  echo
  echo "Options:"
  echo "  -h, --help     Show this help message"
  echo "  -v, --verbose  Show verbose output (including commands being run)"
  echo
  echo "Available logging tests:"
  for test in "${TEST_IDS[@]}"; do
    echo "  - $test"
  done
  echo
  echo "Available variable storage tests:"
  for test in "${VAR_TEST_TYPES[@]}"; do
    echo "  - var:$test"
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
      # Check if this is a var test (prefixed with var:)
      if [[ $1 == var:* ]]; then
        var_test=${1#var:}
        SELECTED_VAR_TESTS+=("$var_test")
      else
        SELECTED_TESTS+=("$1")
      fi
      shift
      ;;
  esac
done

# If no tests specified, run all tests
if [ ${#SELECTED_TESTS[@]} -eq 0 ] && [ ${#SELECTED_VAR_TESTS[@]} -eq 0 ]; then
  SELECTED_TESTS=("${TEST_IDS[@]}")
  SELECTED_VAR_TESTS=("all")
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

# If any var tests were specified, run them
if [ ${#SELECTED_VAR_TESTS[@]} -gt 0 ]; then
  echo
  echo -e "${BLUE}=== Running Variable Storage Tests ===${NC}"
  
  for VAR_TEST in "${SELECTED_VAR_TESTS[@]}"; do
    if [[ ! " ${VAR_TEST_TYPES[*]} " =~ " ${VAR_TEST} " ]]; then
      echo -e "${YELLOW}Warning: Unknown variable test '${VAR_TEST}', skipping${NC}"
      continue
    fi
    
    start_time=$(date +%s.%N)
    
    if [ "$VAR_TEST" = "all" ]; then
      echo -e "${BLUE}Running all variable tests...${NC}"
      # Run all variable tests
      PYTHONPATH=".:../.." python tests/test_vars.py
    else
      echo -e "${BLUE}Testing variable storage: ${VAR_TEST}...${NC}"
      # Run the specified test
      PYTHONPATH=".:../.." python tests/test_vars.py test_${VAR_TEST}
    fi
    
    VAR_TEST_RESULT=$?
    
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc)
    
    if [ $VAR_TEST_RESULT -eq 0 ]; then
      echo -e "${GREEN}✓ Variable test ${VAR_TEST} passed (${duration}s)${NC}"
      pass_count=$((pass_count + 1))
    else
      echo -e "${RED}✗ Variable test ${VAR_TEST} failed with exit code ${VAR_TEST_RESULT} (${duration}s)${NC}"
      fail_count=$((fail_count + 1))
      exit_code=1
    fi
  done
fi

# Print summary
echo
echo -e "${BLUE}=== Test Summary ===${NC}"
echo -e "Total regular tests: ${total_tests}"
if [ ${#SELECTED_VAR_TESTS[@]} -gt 0 ]; then
  echo -e "Variable storage tests: ${#SELECTED_VAR_TESTS[@]}"
fi
echo -e "${GREEN}Passed: ${pass_count}${NC}"
if [ $fail_count -gt 0 ]; then
  echo -e "${RED}Failed: ${fail_count}${NC}"
else
  echo -e "Failed: 0"
fi

exit $exit_code
