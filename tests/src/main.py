from kybra import ic, query, update

# Import and expose all the test functions
from tests import test_functions, test_vars


@query
def greet() -> str:
    """Basic test function"""
    return "Hello from the logging test canister!"


@update
def run_test(function_name: str) -> int:
    ic.print(f"Running test_{function_name}...")
    return test_functions.run_test(function_name)


@update
def run_var_test() -> int:
    ic.print("Running variable storage tests...")
    return test_vars.run_all_tests()
