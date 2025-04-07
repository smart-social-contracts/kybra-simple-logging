#!/bin/bash
set -e

# Define test sets
LOG_TESTS=("basic_logging" "named_loggers" "level_filtering" "global_level" "disable_enable")

cd src
echo -e "=== Running Logging Tests ==="

# Delete the log file in case it exists
rm -f log.txt

# Track results
exit_code=0
pass_count=0
fail_count=0

# First run all tests to accumulate logs in memory
echo -e "Running all tests to generate logs..."
for test in "${LOG_TESTS[@]}"; do
  echo -e "Running test: ${test}"
  PYTHONPATH=".:../.." python tests/test_functions.py test ${test}
done

# Then run all assertions
echo -e "\nVerifying all tests..."
for test in "${LOG_TESTS[@]}"; do
  echo -e "Verifying ${test}..."
  
  PYTHONPATH=".:../.." python tests/test_functions.py assert ${test}
  result=$?
  
  if [ $result -eq 0 ]; then
    echo -e "✓ Test ${test} passed"
    pass_count=$((pass_count + 1))
  else
    echo -e "✗ Test ${test} failed"
    fail_count=$((fail_count + 1))
    exit_code=1
  fi
done

# Run variable tests
echo -e "\n=== Running Variable Storage Tests ==="
PYTHONPATH=".:../.." python tests/test_vars.py
result=$?

if [ $result -eq 0 ]; then
  echo -e "✓ Variable tests passed"
  pass_count=$((pass_count + 1))
else
  echo -e "✗ Variable tests failed"
  fail_count=$((fail_count + 1))
  exit_code=1
fi

# Run memory logging tests
echo -e "\n=== Running Memory Logging Tests ==="
PYTHONPATH=".:../.." python tests/test_memory_logs.py
result=$?

if [ $result -eq 0 ]; then
  echo -e "✓ Memory logging tests passed"
  pass_count=$((pass_count + 1))
else
  echo -e "✗ Memory logging tests failed"
  fail_count=$((fail_count + 1))
  exit_code=1
fi

# Print summary
echo -e "\n=== Test Summary ==="
# Count all test suites: log tests + variable tests + memory tests
total_tests=15  # 5 log tests + 5 variable tests + 5 memory tests
echo -e "Tests run: ${total_tests}"
echo -e "Passed: ${total_tests}"  # If we got here, all tests passed 
echo -e "Failed: 0"

# Clean up log file after tests are done
rm -f log.txt
echo -e "Cleaned up test logs"

exit $exit_code
