# test_logging.py
# Demonstrates how to use the enhanced logging system

# Add the src directory to the Python path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the logger for basic usage
from kybra_simple_logging import logger, get_logger, set_log_level, disable_logging, enable_logging

# PART 1: Using the default logger
print("\n=== Using default logger ===\n")
logger.debug("This DEBUG message won't show because default level is INFO")
logger.info("This is an INFO message from the default logger")
logger.warning("This is a WARNING message from the default logger")
logger.error("This is an ERROR message from the default logger")

# PART 2: Creating component-specific loggers
print("\n=== Using named loggers ===\n")
auth_logger = get_logger("auth")
db_logger = get_logger("database")

auth_logger.info("User login attempted")
db_logger.info("Database connection established")

# PART 3: Setting log levels
print("\n=== Changing log levels ===\n")

# Set specific log level for auth logger
set_log_level("DEBUG", "auth")
auth_logger.debug("This DEBUG message will now show for auth logger")
db_logger.debug("This DEBUG message still won't show for db logger")

# Set global log level
print("\n=== Setting global log level ===\n")
set_log_level("DEBUG")
logger.debug("Now DEBUG messages show for the default logger too")
db_logger.debug("And for the database logger as well")

# PART 4: Disabling logging
print("\n=== Disabling all logging ===\n")
disable_logging()
logger.error("This ERROR won't show because logging is disabled")
auth_logger.critical("Even CRITICAL messages are suppressed")

# Re-enable logging
print("\n=== Re-enabling logging ===\n")
enable_logging()
logger.info("Logging is now re-enabled")

# PART 5: Showing how a library would use this
print("\n=== Library usage example ===\n")

# Example library code
def library_function():
    # Library gets its own logger
    lib_logger = get_logger("my_library")
    lib_logger.info("Library function called")
    lib_logger.debug("Detailed library debug info")

# Application can control library's logging
library_function()  # Will show INFO but not DEBUG

# App can change just the library's logging level
set_log_level("ERROR", "my_library")
library_function()  # Won't show INFO anymore

print("\nTest complete!")
