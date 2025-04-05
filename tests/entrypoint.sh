#!/bin/bash
set -e
set -x

# Start dfx in the background
echo "Starting dfx..."
dfx start --background --clean > src/log.txt 2>&1

# Deploy the test canister
echo "Deploying test canister..."
dfx deploy

# Define a list of test identifiers
TEST_IDS=( 'basic_logging' 'named_loggers' 'level_filtering' 'global_level' 'disable_enable' )

# Loop through each test identifier
for TEST_ID in "${TEST_IDS[@]}"; do
  echo "Testing test_${TEST_ID} module..."
  dfx canister call test run_test ${TEST_ID}
  sleep 2
  
  (cd src && PYTHONPATH=. python tests/test_functions.py assert ${TEST_ID})
  TEST_RESULT=$?
  
  if [ "$TEST_RESULT" != '0' ]; then
    echo "Error: test_${TEST_ID}.run() function returned unexpected result: $TEST_RESULT"
    dfx stop
    exit 1
  else
    echo "test_${TEST_ID}.run() function test passed!"
  fi

done

# Run variable tests
echo "Testing variable storage module..."
TEST_RESULT=$(dfx canister call test run_var_test)
if [ "$TEST_RESULT" != '(0 : int)' ]; then
  echo "Error: run_var_test test returned unexpected result: $TEST_RESULT"
  dfx stop
  exit 1
else
  echo "run_var_test test passed!"
fi

# Run memory logging tests
echo "Testing memory logging module..."
TEST_RESULT=$(dfx canister call test run_memory_logs_test)
if [ "$TEST_RESULT" != '(0 : int)' ]; then
  echo "Error: run_memory_logs_test returned unexpected result: $TEST_RESULT"
  dfx stop
  exit 1
else
  echo "run_memory_logs_test test passed!"
fi

echo "Stopping dfx..."
dfx stop

# Clean up log files
echo "Cleaning up log files..."
rm -f src/log.txt
rm -f log.txt

echo "All done!"