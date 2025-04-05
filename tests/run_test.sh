#!/bin/bash
set -e

# Define test sets
LOG_TESTS=("basic_logging" "named_loggers" "level_filtering" "global_level" "disable_enable")

cd src
echo -e "=== Running Logging Tests ==="

# Track results
exit_code=0
pass_count=0
fail_count=0

# Run logging tests
for test in "${LOG_TESTS[@]}"; do
  echo -e "Testing ${test}..."
  
  PYTHONPATH=".:../.." python tests/test_functions.py test ${test}
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
echo -e "Tests run: $((${#LOG_TESTS[@]}))"
echo -e "Passed: ${pass_count}"
echo -e "Failed: ${fail_count}"

exit $exit_code
