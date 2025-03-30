#!/bin/bash
set -e
set -x

echo "Running tests..."

cd src

exit_code=0

TEST_IDS=("basic_logging" "named_loggers" "level_filtering" "global_level" "disable_enable")


for TEST_ID in "${TEST_IDS[@]}"; do
  echo "Testing test_${TEST_ID} function..."
  
  PYTHONPATH=".:../.." python tests/test_functions.py test ${TEST_ID}
  PYTHONPATH=".:../.." python tests/test_functions.py assert ${TEST_ID}
  
  TEST_RESULT=$?
  if [ $TEST_RESULT -ne 0 ]; then
    exit_code=1
    echo "Test ${TEST_ID} failed with exit code ${TEST_RESULT}"
  fi
done

exit $exit_code
