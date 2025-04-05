# Kybra Simple Logging

[![Test](https://github.com/smart-social-contracts/kybra-simple-logging/actions/workflows/test_ic.yml/badge.svg)](https://github.com/smart-social-contracts/kybra-simple-logging/actions/workflows/test_ic.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/kybra-simple-logging.svg)](https://pypi.org/project/kybra-simple-logging/)
[![License](https://img.shields.io/github/license/smart-social-contracts/kybra-simple-logging.svg)](https://github.com/smart-social-contracts/kybra-simple-logging/blob/main/LICENSE)

A robust logging system for Internet Computer canisters built with Kybra, designed to overcome the limitations of Python's standard logging module in the IC environment. The library includes in-memory log storage capabilities, making it ideal for debugging asynchronous functions where standard logging might be unreliable.

## Features

### Basic Logging
- Works seamlessly in both Internet Computer and non-IC environments
- Avoids using Python's standard logging module (which has compatibility issues in the IC environment)
- Named loggers with `get_logger()` function similar to Python's standard library
- Support for level-based filtering (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Global and per-logger log level configuration
- Ability to enable/disable logging completely
- Best practices for library logging implementation

### In-Memory Logging
- Circular buffer to store logs in memory without exhausting memory
- Capture logs even when display/printing is disabled
- Store detailed log entries with timestamp, level, logger name, and message
- Retrieve and filter logs by level, logger name, or custom criteria
- Independent controls to enable/disable in-memory logging separately from console output
- Ideal for debugging asynchronous functions in the Internet Computer environment

## Installation

### Using pip

```bash
pip install kybra-simple-logging
```

### Manual Installation

Either copy the `kybra_simple_logging` directory from this repository, or use this script to install from PyPI:

```bash
#!/bin/bash
# Download and extract kybra-simple-logging
temp_dir=$(mktemp -d)
pip download --no-deps --dest "$temp_dir" kybra-simple-logging
wheel_file=$(find "$temp_dir" -name "*.whl" | head -n 1)
unzip -q "$wheel_file" -d "$temp_dir/extract"
pkg_dir=$(find "$temp_dir/extract" -type d -name "kybra_simple_logging")
cp -r "$pkg_dir" .
rm -rf "$temp_dir"
```

Save as `install.sh`, run with: `chmod +x install.sh && ./install.sh`

## Quick Start

```python
from kybra_simple_logging import get_logger

# Create a logger
logger = get_logger("my_canister")

# Log messages at different levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Configure logging
from kybra_simple_logging import set_log_level, LogLevel

# Set global log level
set_log_level(LogLevel.INFO)

# Set log level for a specific logger
logger.set_level(LogLevel.DEBUG)

# Disable logging completely
from kybra_simple_logging import disable_logging, enable_logging

disable_logging()
# ... operations without logging ...
enable_logging()

# Use in-memory logging to retrieve logs
from kybra_simple_logging import get_logs, clear_logs, enable_memory_logging, disable_memory_logging

# Clear any existing logs
clear_logs()

# Control memory logging (independent from console output)
disable_memory_logging()  # Stop storing logs in memory (still prints to console if enabled)
logger.info("This will NOT be stored in memory")  

enable_memory_logging()  # Start storing logs in memory again
logger.info("This message is stored in memory")

# Retrieve all logs
logs = get_logs()
for log in logs:
    print(f"{log['timestamp']} [{log['level']}] [{log['logger_name']}]: {log['message']}")

# Retrieve only ERROR logs
error_logs = get_logs(min_level="ERROR")

# Filter logs by logger name
component_logs = get_logs(logger_name="my_component")
```

## Advanced Usage

### Creating Multiple Loggers

```python
# Create loggers for different components
db_logger = get_logger("database")
api_logger = get_logger("api")
auth_logger = get_logger("auth")

# Set different log levels per component
db_logger.set_level(LogLevel.DEBUG)  # More verbose logging for database
api_logger.set_level(LogLevel.INFO)  # Standard logging for API
auth_logger.set_level(LogLevel.WARNING)  # Only warnings and above for auth
```

### In Kybra Canister Functions

```python
from kybra import query
from kybra_simple_logging import get_logger

logger = get_logger("my_canister")

@query
def get_data():
    logger.info("Processing get_data request")
    # ... your code ...
    return result
```

### In-Memory Logging for Debugging

```python
from kybra import update, query
from kybra_simple_logging import (
    get_logger, get_logs, clear_logs, set_max_log_entries,
    enable_memory_logging, disable_memory_logging, is_memory_logging_enabled
)

logger = get_logger("debug_logger")

# Configure the maximum number of logs to keep in memory
set_max_log_entries(1000)

@update
def process_async_task():
    # Clear logs for this specific task
    clear_logs()
    
    # Make sure memory logging is enabled for this task
    if not is_memory_logging_enabled():
        enable_memory_logging()
    
    logger.debug("Starting async task")
    # ... complex asynchronous operations ...
    logger.debug("Step 1 completed")
    # ... more operations ...
    logger.debug("Async task completed")
    
    return "Task completed"

@query
def get_debug_logs(min_level=None, component=None):
    """Retrieve logs for debugging purposes"""
    return get_logs(min_level=min_level, logger_name=component)

@query
def toggle_memory_logging(enabled=True):
    """Enable or disable memory logging"""
    if enabled:
        enable_memory_logging()
    else:
        disable_memory_logging()
    return is_memory_logging_enabled()
```

### Using In-Memory Logs with kybra_simple_shell

You can use this logging system with `kybra_simple_shell` to debug asynchronous functions:

```python
# In your canister code
from kybra_simple_logging import logger, get_logs

# Later, in kybra_simple_shell
logs = get_logs(min_level="DEBUG")
for log in logs:
    print(f"{log['timestamp']} [{log['level']}] [{log['logger_name']}]: {log['message']}")
```

## Development

```bash
# Clone the repository
git clone https://github.com/smart-social-contracts/kybra-simple-logging.git
cd kybra-simple-logging

# Recommended setup
pip install pyenv virtualenv
pyenv local 3.10.7
python -m virtualenv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
cd tests && ./run_test.sh

# Run linters
black .
isort .
flake8 .
mypy .
```

## Running Tests

```bash
pip install -r requirements-dev.txt
python -m pytest -v
```

## License

MIT