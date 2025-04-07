import os
import sys

from kybra_simple_logging import (
    disable_logging,
    enable_logging,
    get_logger,
    get_logs,
    list_vars,
    load_var,
    logger,
    save_var,
    set_log_level,
)
from kybra_simple_logging._handler import _LOG_STORAGE

# Determine if we're in IC environment
IN_IC_ENVIRONMENT = False
try:
    from kybra import ic

    ic.print("")
    IN_IC_ENVIRONMENT = True
except:
    pass


def extract_between(text, start_tag, end_tag):
    try:
        start = text.index(start_tag) + len(start_tag)
        end = text.index(end_tag, start)
        return text[start:end]
    except ValueError:
        return None


FILEPATH = r"/tmp/log.txt"


def save_logs_to_file(filepath=FILEPATH):
    """Save all in-memory logs to a file for test purposes

    Appends current logs to existing logs in the file
    """
    logs = list(_LOG_STORAGE)
    ret = []
    # Add current logs
    for log in logs:
        ret.append(log.message)

    # Combine logs and save
    with open(filepath, "a") as f:
        f.write("\n".join(ret))


def load_logs_from_file(filepath=FILEPATH):
    with open(filepath, "r") as f:
        return f.read()


def custom_print(message: str):
    # Print to console
    if IN_IC_ENVIRONMENT:
        # In IC environment, we just use ic.print which will be captured by dfx
        ic.print(message)
    else:
        print(message)

    # If it's a start/end marker, also store it in the in-memory logs
    if message.startswith("START ") or message.startswith("END "):
        # Use the default logger to store the marker
        logger.info(message)


def test_basic_logging():
    custom_print("START basic_logging")
    logger.debug("[TEST-BASIC] Debug message")
    logger.info("[TEST-BASIC] Info message")
    logger.warning("[TEST-BASIC] Warning message")
    logger.error("[TEST-BASIC] Error message")
    logger.critical("[TEST-BASIC] Critical message")
    custom_print("END basic_logging")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_basic_logging():
    logs = load_logs_from_file()
    assert "[TEST-BASIC] Debug message" not in logs
    assert "[TEST-BASIC] Info message" in logs
    assert "[TEST-BASIC] Warning message" in logs
    assert "[TEST-BASIC] Error message" in logs
    assert "[TEST-BASIC] Critical message" in logs
    return 0


def test_basic_logging():
    custom_print("START basic_logging")
    logger.debug("[TEST-BASIC] Debug message")
    logger.info("[TEST-BASIC] Info message")
    logger.warning("[TEST-BASIC] Warning message")
    logger.error("[TEST-BASIC] Error message")
    logger.critical("[TEST-BASIC] Critical message")
    custom_print("END basic_logging")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_basic_logging():
    logs = load_logs_from_file()
    print("logs", logs)
    assert "[TEST-BASIC] Debug message" not in logs
    assert "[TEST-BASIC] Info message" in logs
    assert "[TEST-BASIC] Warning message" in logs
    assert "[TEST-BASIC] Error message" in logs
    assert "[TEST-BASIC] Critical message" in logs
    return 0


def test_named_loggers():
    """Test multiple named loggers"""
    custom_print("START named_loggers")
    auth_logger = get_logger("auth")
    db_logger = get_logger("db")

    auth_logger.info("[TEST-NAMED] Auth system message")
    db_logger.info("[TEST-NAMED] Database message")
    custom_print("END named_loggers")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_named_loggers():
    logs = load_logs_from_file()

    assert "[TEST-NAMED] Auth system message" in logs
    assert "[TEST-NAMED] Database message" in logs
    return 0


def test_level_filtering():
    """Test log level filtering"""
    custom_print("START level_filtering")
    # First create a logger with ERROR level
    test_logger = get_logger("filter_test")
    set_log_level("ERROR", "filter_test")

    # These should NOT appear in logs
    test_logger.debug("[FILTERED] Debug message")
    test_logger.info("[FILTERED] Info message")
    test_logger.warning("[FILTERED] Warning message")

    # These SHOULD appear in logs
    test_logger.error("[VISIBLE] Error message")
    test_logger.critical("[VISIBLE] Critical message")
    custom_print("END level_filtering")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_level_filtering():
    logs = load_logs_from_file()

    assert "[FILTERED] Debug message" not in logs
    assert "[FILTERED] Info message" not in logs
    assert "[FILTERED] Warning message" not in logs
    assert "[VISIBLE] Error message" in logs
    assert "[VISIBLE] Critical message" in logs
    return 0


def test_global_level():
    """Test global log level setting"""
    custom_print("START global_level")
    # Reset loggers to default state first
    enable_logging()

    # Set global level to ERROR
    set_log_level("ERROR")

    logger.debug("[GLOBAL-FILTERED] Debug should not appear")
    logger.info("[GLOBAL-FILTERED] Info should not appear")
    logger.error("[GLOBAL-VISIBLE] Error should appear")

    # Now set to DEBUG and try again
    set_log_level("DEBUG")
    logger.debug("[GLOBAL-NOW-VISIBLE] Debug should now appear")
    custom_print("END global_level")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_global_level():
    logs = load_logs_from_file()

    assert "[GLOBAL-FILTERED] Debug should not appear" not in logs
    assert "[GLOBAL-FILTERED] Info should not appear" not in logs
    assert "[GLOBAL-VISIBLE] Error should appear" in logs
    assert "[GLOBAL-NOW-VISIBLE] Debug should now appear" in logs
    return 0


def test_disable_enable():
    """Test disabling and enabling logging"""
    custom_print("START disable_enable")
    # Make sure logging is enabled to start
    enable_logging()

    logger.info("[BEFORE-DISABLE] This message should appear")

    disable_logging()
    logger.error("[DISABLED] This should NOT appear even though it's ERROR level")

    enable_logging()
    logger.info("[AFTER-ENABLE] This should appear again")
    custom_print("END disable_enable")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_disable_enable():
    logs = load_logs_from_file()

    assert "[BEFORE-DISABLE] This message should appear" in logs
    assert "[DISABLED] This should NOT appear even though it's ERROR level" not in logs
    assert "[AFTER-ENABLE] This should appear again" in logs
    return 0


def test_debug_vars():
    """Test the debug variable storage functions"""
    custom_print("START debug_vars")

    # Test saving and loading a simple variable
    save_var("test_string", "Hello, World!")
    loaded_string = load_var("test_string")
    custom_print(f"Loaded string: {loaded_string}")
    assert loaded_string == "Hello, World!"

    # Test saving and loading a more complex variable
    test_dict = {"name": "Test", "value": 42, "nested": {"key": "value"}}
    save_var("test_dict", test_dict)
    loaded_dict = load_var("test_dict")
    custom_print(f"Loaded dict: {loaded_dict}")

    # Test loading a non-existent variable
    non_existent = load_var("does_not_exist")
    custom_print(f"Non-existent var: {non_existent}")

    # List all stored variables
    vars_dict = list_vars()
    custom_print(f"Available debug variables: {vars_dict}")

    custom_print("END debug_vars")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_debug_vars():
    logs = load_logs_from_file()

    # Verify the debug messages about saving variables appear in logs
    assert "Variable saved with tag 'test_string'" in logs
    assert "Variable saved with tag 'test_dict'" in logs

    # Verify warning about non-existent variable
    assert "No variable found with tag 'does_not_exist'" in logs

    # Verify info message from list_vars
    assert "Available debug variables:" in logs

    return 0


def run_test(test_id: str) -> int:
    return globals()[f"test_{test_id}"]()


def run_assert(test_id: str) -> int:
    return globals()[f"assert_{test_id}"]()


if __name__ == "__main__":
    import sys

    operation = sys.argv[1]
    test_id = sys.argv[2]

    sys.exit(globals()[f"run_{operation}"](test_id))


def test_named_loggers():
    """Test multiple named loggers"""
    custom_print("START named_loggers")
    auth_logger = get_logger("auth")
    db_logger = get_logger("db")

    auth_logger.info("[TEST-NAMED] Auth system message")
    db_logger.info("[TEST-NAMED] Database message")
    custom_print("END named_loggers")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_named_loggers():
    logs = load_logs_from_file()

    assert "[TEST-NAMED] Auth system message" in logs
    assert "[TEST-NAMED] Database message" in logs
    return 0


def test_level_filtering():
    """Test log level filtering"""
    custom_print("START level_filtering")
    # First create a logger with ERROR level
    test_logger = get_logger("filter_test")
    set_log_level("ERROR", "filter_test")

    # These should NOT appear in logs
    test_logger.debug("[FILTERED] Debug message")
    test_logger.info("[FILTERED] Info message")
    test_logger.warning("[FILTERED] Warning message")

    # These SHOULD appear in logs
    test_logger.error("[VISIBLE] Error message")
    test_logger.critical("[VISIBLE] Critical message")
    custom_print("END level_filtering")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()
    return 0


def assert_level_filtering():
    logs = load_logs_from_file()

    assert "[FILTERED] Debug message" not in logs
    assert "[FILTERED] Info message" not in logs
    assert "[FILTERED] Warning message" not in logs
    assert "[VISIBLE] Error message" in logs
    assert "[VISIBLE] Critical message" in logs
    return 0


def test_global_level():
    """Test global log level setting"""
    custom_print("START global_level")
    # Reset loggers to default state first
    enable_logging()

    # Set global level to ERROR
    set_log_level("ERROR")

    logger.debug("[GLOBAL-FILTERED] Debug should not appear")
    logger.info("[GLOBAL-FILTERED] Info should not appear")
    logger.error("[GLOBAL-VISIBLE] Error should appear")

    # Now set to DEBUG and try again
    set_log_level("DEBUG")
    logger.debug("[GLOBAL-NOW-VISIBLE] Debug should now appear")
    custom_print("END global_level")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()

    return 0


def assert_global_level():
    logs = load_logs_from_file()

    assert "[GLOBAL-FILTERED] Debug should not appear" not in logs
    assert "[GLOBAL-FILTERED] Info should not appear" not in logs
    assert "[GLOBAL-VISIBLE] Error should appear" in logs
    assert "[GLOBAL-NOW-VISIBLE] Debug should now appear" in logs
    return 0


def test_disable_enable():
    """Test disabling and enabling logging"""
    custom_print("START disable_enable")
    # Make sure logging is enabled to start
    enable_logging()

    logger.info("[BEFORE-DISABLE] This message should appear")

    disable_logging()
    logger.error("[DISABLED] This should NOT appear even though it's ERROR level")

    enable_logging()
    logger.info("[AFTER-ENABLE] This should appear again")
    custom_print("END disable_enable")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()

    return 0


def assert_disable_enable():
    logs = load_logs_from_file()

    assert "[BEFORE-DISABLE] This message should appear" in logs
    assert "[DISABLED] This should NOT appear even though it's ERROR level" not in logs
    assert "[AFTER-ENABLE] This should appear again" in logs
    return 0


def test_debug_vars():
    """Test the debug variable storage functions"""
    custom_print("START debug_vars")

    # Test saving and loading a simple variable
    save_var("test_string", "Hello, World!")
    loaded_string = load_var("test_string")
    custom_print(f"Loaded string: {loaded_string}")
    assert loaded_string == "Hello, World!"

    # Test saving and loading a more complex variable
    test_dict = {"name": "Test", "value": 42, "nested": {"key": "value"}}
    save_var("test_dict", test_dict)
    loaded_dict = load_var("test_dict")
    custom_print(f"Loaded dict: {loaded_dict}")

    # Test loading a non-existent variable
    non_existent = load_var("does_not_exist")
    custom_print(f"Non-existent var: {non_existent}")

    # List all stored variables
    vars_dict = list_vars()
    custom_print(f"Available debug variables: {vars_dict}")

    custom_print("END debug_vars")

    if not IN_IC_ENVIRONMENT:
        save_logs_to_file()

    return 0


def assert_debug_vars():
    logs = load_logs_from_file()

    # Verify the debug messages about saving variables appear in logs
    assert "Variable saved with tag 'test_string'" in logs
    assert "Variable saved with tag 'test_dict'" in logs

    # Verify warning about non-existent variable
    assert "No variable found with tag 'does_not_exist'" in logs

    # Verify info message from list_vars
    assert "Available debug variables:" in logs

    return 0


def run_test(test_id: str) -> int:
    return globals()[f"test_{test_id}"]()


def run_assert(test_id: str) -> int:
    return globals()[f"assert_{test_id}"]()


if __name__ == "__main__":
    import sys

    operation = sys.argv[1]
    test_id = sys.argv[2]

    sys.exit(globals()[f"run_{operation}"](test_id))
