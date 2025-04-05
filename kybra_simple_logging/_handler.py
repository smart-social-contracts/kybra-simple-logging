# Simple custom logger that doesn't use Python's logging module
# to avoid process ID access which is unsupported in IC environment

import json
import pickle
import sys
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable, Deque, Dict, List, Literal, Optional, Union

# Global settings
_LOGGING_ENABLED = True
_MEMORY_LOGGING_ENABLED = True  # Controls whether logs are stored in memory
_LOGGERS: Dict[str, "SimpleLogger"] = {}

# Debug variable storage
_DEBUG_VARS: Dict[str, Any] = {}

# In-memory log storage
_MAX_LOG_ENTRIES = 1000  # Maximum number of log entries to keep in memory
_LOG_STORAGE: Deque["LogEntry"] = deque(maxlen=_MAX_LOG_ENTRIES)
_LOG_SEQUENCE_COUNTER = 0  # Global counter for generating unique log entry IDs


@dataclass
class LogEntry:
    """Represents a single log entry stored in memory"""

    timestamp: float
    level: str
    logger_name: str
    message: str
    id: int  # Unique identifier for the log entry

    def to_dict(self) -> Dict[str, Any]:
        """Convert log entry to dictionary for serialization"""
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "logger_name": self.logger_name,
            "message": self.message,
            "id": self.id,
        }


# Define a safe fallback first
def _print_log(level: str, message: str, logger_name: str) -> None:
    if not _LOGGING_ENABLED:
        return
    print(f"[{level}] [{logger_name}] {message}")
    # Store in memory regardless of print settings
    _store_log_entry(level, message, logger_name)


def _store_log_entry(level: str, message: str, logger_name: str) -> None:
    """Store a log entry in the memory buffer if memory logging is enabled"""
    if not _MEMORY_LOGGING_ENABLED:
        return

    global _LOG_SEQUENCE_COUNTER
    _LOG_SEQUENCE_COUNTER += 1

    entry = LogEntry(
        timestamp=time.time(),
        level=level,
        logger_name=logger_name,
        message=message,
        id=_LOG_SEQUENCE_COUNTER,
    )
    _LOG_STORAGE.append(entry)


# Now try to use the IC-specific functionality if available and working
_in_ic_environment = False
try:
    # First check if we can import kybra
    from kybra import ic

    # Now safely test if ic.print actually works
    try:
        # Try to use ic.print but catch any errors
        ic.print("Logger initializing")

        # If we get here, ic.print works!
        _in_ic_environment = True

        # Override the print_log function with IC-specific version
        def _ic_print_log(level: str, message: str, logger_name: str) -> None:
            if not _LOGGING_ENABLED:
                return
            ic.print(f"[{level}] [{logger_name}] {message}")
            # Store in memory regardless of print settings
            _store_log_entry(level, message, logger_name)

        # Define IC-specific version of store_log_entry using ic.time()
        def _ic_store_log_entry(level: str, message: str, logger_name: str) -> None:
            """Store a log entry in the memory buffer if memory logging is enabled"""
            if not _MEMORY_LOGGING_ENABLED:
                return

            global _LOG_SEQUENCE_COUNTER
            _LOG_SEQUENCE_COUNTER += 1

            entry = LogEntry(
                timestamp=ic.time(),
                level=level,
                logger_name=logger_name,
                message=message,
                id=_LOG_SEQUENCE_COUNTER,
            )
            _LOG_STORAGE.append(entry)

        # Replace the regular functions with IC versions
        _print_log = _ic_print_log
        _store_log_entry = _ic_store_log_entry

    except:
        # If we get an error trying to use ic.print, fall back to regular print
        pass

except ImportError:
    # If kybra isn't available, we're definitely not in an IC environment
    print("Note: Kybra not available, using regular print for logging")

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class SimpleLogger:
    # Level constants
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    # Level values for filtering
    LEVEL_VALUES = {DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40, CRITICAL: 50}

    def __init__(self, name: str = "kybra_simple_logger", level: LogLevel = "INFO"):
        self.name = name
        self.level = level

    def set_level(self, level: LogLevel) -> None:
        """Set the minimum logging level"""
        self.level = level

    def is_enabled_for(self, level: LogLevel) -> bool:
        """Check if this level should be logged"""
        return self.LEVEL_VALUES.get(level, 0) >= self.LEVEL_VALUES.get(self.level, 0)

    def log(self, level: LogLevel, message: str) -> None:
        if not self.is_enabled_for(level):
            return
        _print_log(level, message, self.name)

    def debug(self, message: str) -> None:
        self.log(self.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(self.INFO, message)

    def warning(self, message: str) -> None:
        self.log(self.WARNING, message)

    def warn(self, message: str) -> None:
        self.warning(message)

    def error(self, message: str) -> None:
        self.log(self.ERROR, message)

    def critical(self, message: str) -> None:
        self.log(self.CRITICAL, message)


# Public API functions
def get_logger(name: str = "kybra_simple_logging") -> SimpleLogger:
    """Get or create a logger with the specified name"""
    if name not in _LOGGERS:
        _LOGGERS[name] = SimpleLogger(name)
    return _LOGGERS[name]


def set_log_level(level: LogLevel, logger_name: Optional[str] = None) -> None:
    """Set log level for all loggers or a specific one"""
    if logger_name is not None:
        if logger_name in _LOGGERS:
            _LOGGERS[logger_name].set_level(level)
    else:
        # Set for all loggers
        for logger in _LOGGERS.values():
            logger.set_level(level)


def disable_logging() -> None:
    """Completely disable all logging"""
    global _LOGGING_ENABLED
    _LOGGING_ENABLED = False


def enable_logging() -> None:
    """Re-enable logging"""
    global _LOGGING_ENABLED
    _LOGGING_ENABLED = True


# Debug variable storage functions
def save_var(tag: str, obj: Any) -> None:
    """Store a variable with a tag for debugging purposes

    Args:
        tag: A string identifier to later retrieve the object
        obj: Any Python object to store
    """
    _DEBUG_VARS[tag] = obj


def load_var(tag: str) -> Any:
    """Retrieve a previously stored variable by its tag

    Args:
        tag: The identifier used when saving the variable

    Returns:
        The stored object or None if not found
    """
    if tag not in _DEBUG_VARS:
        return None
    return _DEBUG_VARS[tag]


def list_vars() -> Dict[str, str]:
    """List all stored variables with their types

    Returns:
        A dictionary mapping variable tags to their types
    """
    return {tag: str(type(obj).__name__) for tag, obj in _DEBUG_VARS.items()}


# Default logger for backwards compatibility
logger = get_logger()


# In-memory log retrieval functions
def get_logs(
    max_entries: Optional[int] = None,
    min_level: Optional[LogLevel] = None,
    logger_name: Optional[str] = None,
    filter_fn: Optional[Callable[[LogEntry], bool]] = None,
    oldest_first: bool = False,  # New parameter to control sort order
) -> List[Dict[str, Any]]:
    """Retrieve logs from memory with optional filtering

    Args:
        max_entries: Maximum number of entries to return (newest first by default)
        min_level: Minimum log level to include
        logger_name: Filter logs to a specific logger
        filter_fn: Custom filter function taking a LogEntry and returning boolean
        oldest_first: If True, return oldest logs first instead of newest first

    Returns:
        List of log entries as dictionaries
    """
    # Create a copy of the logs to avoid modifying the original
    logs = list(_LOG_STORAGE)

    # Apply filters
    if min_level is not None:
        min_level_value = SimpleLogger.LEVEL_VALUES.get(min_level, 0)
        logs = [
            log
            for log in logs
            if SimpleLogger.LEVEL_VALUES.get(log.level, 0) >= min_level_value
        ]

    if logger_name is not None:
        logs = [log for log in logs if log.logger_name == logger_name]

    if filter_fn is not None:
        logs = [log for log in logs if filter_fn(log)]

    # Sort by timestamp and id
    # When timestamps are identical, id ensures correct order
    logs.sort(key=lambda log: (log.timestamp, log.id), reverse=not oldest_first)

    # Limit the number of entries if requested
    if max_entries is not None:
        logs = logs[:max_entries]

    # Convert to dictionaries for easier serialization
    return [log.to_dict() for log in logs]


def clear_logs() -> None:
    """Clear all logs from memory"""
    _LOG_STORAGE.clear()


def disable_memory_logging() -> None:
    """Disable storing logs in memory"""
    global _MEMORY_LOGGING_ENABLED
    _MEMORY_LOGGING_ENABLED = False


def enable_memory_logging() -> None:
    """Enable storing logs in memory"""
    global _MEMORY_LOGGING_ENABLED
    _MEMORY_LOGGING_ENABLED = True


def is_memory_logging_enabled() -> bool:
    """Check if memory logging is enabled"""
    return _MEMORY_LOGGING_ENABLED


def set_max_log_entries(max_entries: int) -> None:
    """Set the maximum number of log entries to keep in memory

    Args:
        max_entries: New maximum capacity of the log storage
    """
    global _LOG_STORAGE, _MAX_LOG_ENTRIES
    # Create a new deque with the new max length
    _MAX_LOG_ENTRIES = max(1, max_entries)  # Ensure at least 1 entry
    new_storage = deque(maxlen=_MAX_LOG_ENTRIES)

    # Transfer any existing logs (up to the new capacity)
    logs = list(_LOG_STORAGE)
    logs.sort(key=lambda log: log.timestamp)  # Sort by timestamp (oldest first)

    # Keep the newest logs if we're reducing capacity
    if len(logs) > _MAX_LOG_ENTRIES:
        logs = logs[-_MAX_LOG_ENTRIES:]

    # Add logs to the new storage
    for log in logs:
        new_storage.append(log)

    # Replace the old storage with the new one
    _LOG_STORAGE = new_storage
