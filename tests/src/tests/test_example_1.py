
from kybra import query

# Import the kybra_simple_logging module
import sys
import os
sys.path.append("/app")
from kybra_simple_logging import logger, get_logger, set_log_level, disable_logging, enable_logging

@query
def test_basic_logging() -> str:
    """Test basic logging with all levels"""
    logger.debug("[TEST-BASIC] Debug message")
    logger.info("[TEST-BASIC] Info message")
    logger.warning("[TEST-BASIC] Warning message") 
    logger.error("[TEST-BASIC] Error message")
    logger.critical("[TEST-BASIC] Critical message")
    return "Completed basic logging test"

@query 
def test_named_loggers() -> str:
    """Test multiple named loggers"""
    auth_logger = get_logger("auth")
    db_logger = get_logger("db")
    
    auth_logger.info("[TEST-NAMED] Auth system message")
    db_logger.info("[TEST-NAMED] Database message")
    return "Completed named logger test"

@query
def test_level_filtering() -> str:
    """Test log level filtering"""
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
    
    return "Completed level filtering test"

@query
def test_global_level() -> str:
    """Test global log level setting"""
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
    
    return "Completed global level test"

@query
def test_disable_enable() -> str:
    """Test disabling and enabling logging"""
    # Make sure logging is enabled to start
    enable_logging()
    
    logger.info("[BEFORE-DISABLE] This message should appear")
    
    disable_logging()
    logger.error("[DISABLED] This should NOT appear even though it's ERROR level")
    
    enable_logging()
    logger.info("[AFTER-ENABLE] This should appear again")
    
    return "Completed disable/enable test"

@query
def run() -> str:
    """Run a simple test to verify the logger functions"""
    test_basic_logging()
    test_named_loggers()
    test_level_filtering()
    test_global_level()
    test_disable_enable()
    
    return "All logging tests completed successfully"


if __name__ == "__main__":
    exit(0)
