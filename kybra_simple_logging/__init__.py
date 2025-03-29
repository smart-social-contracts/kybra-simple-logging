from ._handler import (
    logger,  # Default logger for backwards compatibility
    get_logger,  # Function to get a named logger
    set_log_level,  # Function to set log level for one or all loggers
    disable_logging,  # Function to disable all logging
    enable_logging,  # Function to re-enable logging
    SimpleLogger,  # The logger class itself
    LogLevel  # Type for log levels
)

# This allows imports like:
# from kybra_simple_logging import logger, get_logger, set_log_level
