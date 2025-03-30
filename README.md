# Kybra Simple Logging

[![Test](https://github.com/smart-social-contracts/kybra-simple-logging/actions/workflows/test_ic.yml/badge.svg)](https://github.com/smart-social-contracts/kybra-simple-logging/actions/workflows/test_ic.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/kybra-simple-logging.svg)](https://pypi.org/project/kybra-simple-logging/)
[![License](https://img.shields.io/github/license/smart-social-contracts/kybra-simple-logging.svg)](https://github.com/smart-social-contracts/kybra-simple-logging/blob/main/LICENSE)

A robust logging system for Internet Computer canisters built with Kybra, designed to overcome the limitations of Python's standard logging module in the IC environment.

## Features

- Works seamlessly in both Internet Computer and non-IC environments
- Avoids using Python's standard logging module (which has compatibility issues in the IC environment)
- Named loggers with `get_logger()` function similar to Python's standard library
- Support for level-based filtering (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Global and per-logger log level configuration
- Ability to enable/disable logging completely
- Best practices for library logging implementation

## Installation

### Using pip

```bash
pip install kybra-simple-logging
```

### Manual Installation

In your Kybra project, simply copy the `kybra_simple_logging` directory to your project.

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