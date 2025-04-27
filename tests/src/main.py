from kybra import ic, query, update

# Import and expose all the test functions
from tests import test_functions, test_memory_logs, test_vars


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


@update
def run_memory_logs_test() -> int:
    ic.print("Running memory logging tests...")
    return test_memory_logs.run_tests()


# ##### Import Kybra and the internal function #####

from kybra import Opt, Record, Vec, nat, query  # noqa: E402

from kybra_simple_logging import get_canister_logs as _get_canister_logs  # noqa: E402


# Define the PublicLogEntry class directly in the test canister
class PublicLogEntry(Record):
    timestamp: nat
    level: str
    logger_name: str
    message: str
    id: nat


@query
def get_canister_logs(
    from_entry: Opt[nat] = None,
    max_entries: Opt[nat] = None,
    min_level: Opt[str] = None,
    logger_name: Opt[str] = None,
) -> Vec[PublicLogEntry]:
    """
    Re-export the get_canister_logs query function from the library
    This makes it accessible as a query method on the test canister
    """
    logs = _get_canister_logs(
        from_entry=from_entry,
        max_entries=max_entries,
        min_level=min_level,
        logger_name=logger_name,
    )

    # Convert the logs to our local PublicLogEntry type
    return [
        PublicLogEntry(
            timestamp=log["timestamp"],
            level=log["level"],
            logger_name=log["logger_name"],
            message=log["message"],
            id=log["id"],
        )
        for log in logs
    ]
