# Simple custom logger that doesn't use Python's logging module
# to avoid process ID access which is unsupported in IC environment

from typing import Literal, Optional, Union, Dict
import sys

# Global settings
_LOGGING_ENABLED = True
_LOGGERS: Dict[str, "SimpleLogger"] = {}

# Define a safe fallback first
def _print_log(level: str, message: str) -> None:
    if not _LOGGING_ENABLED:
        return
    print(f"[{level}] {message}")

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
        def _ic_print_log(level: str, message: str) -> None:
            if not _LOGGING_ENABLED:
                return
            ic.print(f"[{level}] {message}")
        
        # Replace the regular print with IC print
        _print_log = _ic_print_log
        
    except Exception as e:
        # If we get an error trying to use ic.print, fall back to regular print
        # print(f"Note: Using regular print for logging (IC environment not detected: {str(e)})")
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
    LEVEL_VALUES = {
        DEBUG: 10,
        INFO: 20,
        WARNING: 30,
        ERROR: 40,
        CRITICAL: 50
    }
    
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
        _print_log(level, f"[{self.name}] {message}")

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

# Default logger for backwards compatibility
logger = get_logger()
