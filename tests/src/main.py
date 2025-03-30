from kybra import ic, query

# Import and expose all the test functions
from tests.test_example_1 import (
    test_basic_logging,
    test_named_loggers,
    test_level_filtering,
    test_global_level,
    test_disable_enable,
    run as run_all_tests
)

@query
def greet() -> str:
    """Basic test function"""
    return "Hello from the logging test canister!"

@query
def run_tests() -> str:
    """Run all logging tests"""
    return run_all_tests()
