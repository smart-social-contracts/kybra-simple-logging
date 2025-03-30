
try:
    from kybra import ic
except:
    pass

from kybra_simple_logging import logger, get_logger, set_log_level, disable_logging, enable_logging
from tests.utils import extract_between


def test_basic_logging():
    ic.print('START basic_logging')
    logger.debug("[TEST-BASIC] Debug message")
    logger.info("[TEST-BASIC] Info message")
    logger.warning("[TEST-BASIC] Warning message")
    logger.error("[TEST-BASIC] Error message")
    logger.critical("[TEST-BASIC] Critical message")
    ic.print('END basic_logging')
    return 0


def assert_basic_logging():
    logs = open("/app/log.txt").read()
    logs = extract_between(logs, 'START basic_logging', 'END basic_logging')
    assert "[TEST-BASIC] Debug message" not in logs
    assert "[TEST-BASIC] Info message" in logs
    assert "[TEST-BASIC] Warning message" in logs
    assert "[TEST-BASIC] Error message" in logs
    assert "[TEST-BASIC] Critical message" in logs
    return 0


# def test_named_loggers() -> str:
#     """Test multiple named loggers"""
#     auth_logger = get_logger("auth")
#     db_logger = get_logger("db")

#     auth_logger.info("[TEST-NAMED] Auth system message")
#     db_logger.info("[TEST-NAMED] Database message")
#     return "Completed named logger test"

# def test_level_filtering() -> str:
#     """Test log level filtering"""
#     # First create a logger with ERROR level
#     test_logger = get_logger("filter_test")
#     set_log_level("ERROR", "filter_test")

#     # These should NOT appear in logs
#     test_logger.debug("[FILTERED] Debug message")
#     test_logger.info("[FILTERED] Info message")
#     test_logger.warning("[FILTERED] Warning message")

#     # These SHOULD appear in logs
#     test_logger.error("[VISIBLE] Error message")
#     test_logger.critical("[VISIBLE] Critical message")

#     return "Completed level filtering test"


# def test_global_level() -> str:
#     """Test global log level setting"""
#     # Reset loggers to default state first
#     enable_logging()
#     test_logger = get_logger("global_test")

#     # Set global level to ERROR
#     set_log_level("ERROR")

#     logger.debug("[GLOBAL-FILTERED] Debug should not appear")
#     logger.info("[GLOBAL-FILTERED] Info should not appear")
#     logger.error("[GLOBAL-VISIBLE] Error should appear")

#     # Now set to DEBUG and try again
#     set_log_level("DEBUG")
#     logger.debug("[GLOBAL-NOW-VISIBLE] Debug should now appear")

#     return "Completed global level test"


# def test_disable_enable() -> str:
#     """Test disabling and enabling logging"""
#     # Make sure logging is enabled to start
#     enable_logging()

#     logger.info("[BEFORE-DISABLE] This message should appear")

#     disable_logging()
#     logger.error("[DISABLED] This should NOT appear even though it's ERROR level")

#     enable_logging()
#     logger.info("[AFTER-ENABLE] This should appear again")

#     return "Completed disable/enable test"


def run_test(function_name: str) -> int:
    return globals()[f"test_{function_name}"]()


def run_assert(function_name: str) -> int:
    return globals()[f"assert_{function_name}"]()


if __name__ == "__main__":
    import sys
    function_name = sys.argv[1]
    sys.exit(run_assert(function_name))
