
try:
    from kybra import ic
except:
    pass

from kybra_simple_logging import logger, get_logger, set_log_level, disable_logging, enable_logging
from tests.utils import extract_between

def custom_print(message: str):
    try:
        ic.print(message)
    except:
        print(message)


def test_basic_logging():
    custom_print('START basic_logging')
    logger.debug("[TEST-BASIC] Debug message")
    logger.info("[TEST-BASIC] Info message")
    logger.warning("[TEST-BASIC] Warning message")
    logger.error("[TEST-BASIC] Error message")
    logger.critical("[TEST-BASIC] Critical message")
    custom_print('END basic_logging')
    return 0


def assert_basic_logging():
    logs = open("log.txt").read()
    logs = extract_between(logs, 'START basic_logging', 'END basic_logging')
    assert "[TEST-BASIC] Debug message" not in logs
    assert "[TEST-BASIC] Info message" in logs
    assert "[TEST-BASIC] Warning message" in logs
    assert "[TEST-BASIC] Error message" in logs
    assert "[TEST-BASIC] Critical message" in logs
    return 0


def test_named_loggers():
    """Test multiple named loggers"""
    custom_print('START named_loggers')
    auth_logger = get_logger("auth")
    db_logger = get_logger("db")

    auth_logger.info("[TEST-NAMED] Auth system message")
    db_logger.info("[TEST-NAMED] Database message")
    custom_print('END named_loggers')
    return 0


def assert_named_loggers():
    logs = open("log.txt").read()
    logs = extract_between(logs, 'START named_loggers', 'END named_loggers')
    assert "[TEST-NAMED] Auth system message" in logs
    assert "[TEST-NAMED] Database message" in logs
    return 0


def test_level_filtering():
    """Test log level filtering"""
    custom_print('START level_filtering')
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
    custom_print('END level_filtering')
    return 0


def assert_level_filtering():
    logs = open("log.txt").read()
    logs = extract_between(logs, 'START level_filtering', 'END level_filtering')
    assert "[FILTERED] Debug message" not in logs
    assert "[FILTERED] Info message" not in logs
    assert "[FILTERED] Warning message" not in logs
    assert "[VISIBLE] Error message" in logs
    assert "[VISIBLE] Critical message" in logs
    return 0


def test_global_level():
    """Test global log level setting"""
    custom_print('START global_level')
    # Reset loggers to default state first
    enable_logging()
    test_logger = get_logger("global_test")

    # Set global level to ERROR
    set_log_level("ERROR")

    logger.debug("[GLOBAL-FILTERED] Debug should not appear")
    logger.info("[GLOBAL-FILTERED] Info should not appear")
    logger.error("[GLOBAL-VISIBLE] Error should appear")

    # Now set to DEBUG and try again
    set_log_level("DEBUG")
    logger.debug("[GLOBAL-NOW-VISIBLE] Debug should now appear")
    custom_print('END global_level')
    return 0


def assert_global_level():
    logs = open("log.txt").read()
    logs = extract_between(logs, 'START global_level', 'END global_level')
    assert "[GLOBAL-FILTERED] Debug should not appear" not in logs
    assert "[GLOBAL-FILTERED] Info should not appear" not in logs
    assert "[GLOBAL-VISIBLE] Error should appear" in logs
    assert "[GLOBAL-NOW-VISIBLE] Debug should now appear" in logs
    return 0


def test_disable_enable():
    """Test disabling and enabling logging"""
    custom_print('START disable_enable')
    # Make sure logging is enabled to start
    enable_logging()

    logger.info("[BEFORE-DISABLE] This message should appear")

    disable_logging()
    logger.error("[DISABLED] This should NOT appear even though it's ERROR level")

    enable_logging()
    logger.info("[AFTER-ENABLE] This should appear again")
    custom_print('END disable_enable')
    return 0


def assert_disable_enable():
    logs = open("log.txt").read()
    logs = extract_between(logs, 'START disable_enable', 'END disable_enable')
    assert "[BEFORE-DISABLE] This message should appear" in logs
    assert "[DISABLED] This should NOT appear even though it's ERROR level" not in logs
    assert "[AFTER-ENABLE] This should appear again" in logs
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
