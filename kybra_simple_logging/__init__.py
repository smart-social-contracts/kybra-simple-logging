# Debug variable storage functions
# New in-memory logging functions
from ._handler import Level  # Enum for log levels
from ._handler import LogEntry  # Log entry data class
from ._handler import SimpleLogger  # The logger class itself
from ._handler import clear_logs  # Function to clear all logs from memory
from ._handler import disable_logging  # Function to disable all logging
from ._handler import disable_memory_logging  # Function to disable in-memory logging
from ._handler import enable_logging  # Function to re-enable logging
from ._handler import enable_memory_logging  # Function to enable in-memory logging
from ._handler import get_logger  # Function to get a named logger
from ._handler import get_logs  # Function to retrieve logs from memory
from ._handler import list_vars  # Function to list all saved variables
from ._handler import load_var  # Function to load a saved variable
from ._handler import logger  # Default logger for backwards compatibility
from ._handler import save_var  # Function to save a variable for debugging
from ._handler import set_log_level  # Function to set log level for one or all loggers
from ._handler import set_max_log_entries  # Function to set maximum log storage size
from ._handler import (  # Function to check memory logging status
    is_memory_logging_enabled,
)

# New canister query function for exposing logs
try:
    from ._handler import PublicLogEntry  # Public log entry type for canister queries
    from ._handler import (  # Query function to expose logs via canister query
        get_canister_logs,
    )
except ImportError:
    # If kybra isn't available, these imports will fail
    # This allows the library to be used in non-IC environments
    pass

# This allows imports like:
# from kybra_simple_logging import logger, get_logger, set_log_level
# from kybra_simple_logging import save_var, load_var, list_vars
# from kybra_simple_logging import get_logs, clear_logs, set_max_log_entries, enable_memory_logging, disable_memory_logging
# from kybra_simple_logging import PublicLogEntry, get_canister_logs
