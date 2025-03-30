from ._handler import LogLevel  # Type for log levels
from ._handler import SimpleLogger  # The logger class itself
from ._handler import disable_logging  # Function to disable all logging
from ._handler import enable_logging  # Function to re-enable logging
from ._handler import get_logger  # Function to get a named logger
from ._handler import logger  # Default logger for backwards compatibility
from ._handler import set_log_level  # Function to set log level for one or all loggers

# This allows imports like:
# from kybra_simple_logging import logger, get_logger, set_log_level
