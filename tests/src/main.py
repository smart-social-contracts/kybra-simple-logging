from kybra import ic, query, update

# Import and expose all the test functions
from tests import (
    test_example_1
)

@query
def greet() -> str:
    """Basic test function"""
    return "Hello from the logging test canister!"

@update
def run_test(module_name: str) -> int:
    ic.print(f"Running test_{module_name}...")
    return globals()[f"test_{module_name}"].run()
