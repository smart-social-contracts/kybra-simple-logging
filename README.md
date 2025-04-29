# Kybra Simple Logging

[![Test IC](https://github.com/smart-social-contracts/kybra-simple-logging/actions/workflows/test_ic.yml/badge.svg)](https://github.com/smart-social-contracts/kybra-simple-logging/actions)
[![Test](https://github.com/smart-social-contracts/kybra-simple-logging/actions/workflows/test.yml/badge.svg)](https://github.com/smart-social-contracts/kybra-simple-logging/actions)
[![PyPI version](https://badge.fury.io/py/kybra-simple-logging.svg)](https://badge.fury.io/py/kybra-simple-logging)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3107/)
[![License](https://img.shields.io/github/license/smart-social-contracts/kybra-simple-logging.svg)](https://github.com/smart-social-contracts/kybra-simple-logging/blob/main/LICENSE)

A simple logging system for the [Internet Computer](https://internetcomputer.org) built with [Kybra](https://github.com/demergent-labs/kybra). The library includes in-memory log storage capabilities, providing robust logging for all canister functions including asynchronous operations.


## Features

- CLI tool for querying logs directly from canisters to your local machine (including in semi-real time with `--follow`)
- Works seamlessly in both Internet Computer and non-IC environments
- Avoids using Python's standard logging module (which has compatibility issues in the IC environment)
- Named loggers with `get_logger()` function similar to Python's standard library
- Support for level-based filtering (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Global and per-logger log level configuration
- Ability to enable/disable logging completely
- Circular buffer to store logs in memory without exhausting memory


## Installation

```bash
pip install kybra-simple-logging
```

## Quick Start

```python
from kybra_simple_logging import get_logger

# Create a logger
logger = get_logger("my_canister")

# Log messages at a specific level
logger.info("This is an info message")

# Set log level for a specific logger
logger.set_level(LogLevel.DEBUG)

# Use in-memory logging to retrieve logs
from kybra_simple_logging import get_logs, clear_logs, enable_memory_logging, disable_memory_logging

# Retrieve only ERROR logs
error_logs = get_logs(min_level="ERROR")

# Filter logs by logger name
component_logs = get_logs(logger_name="my_component")
```

## CLI Tool

The package includes a command-line tool for querying logs from canisters.
Example:

```bash
# View the first 10 ERROR log entries of logger with name MY_LOGGER_NAME, and then follow and poll every 5 seconds, from the canister with ID <CANISTER_ID> on the IC network
kslog <CANISTER_ID> --tail 10 --level ERROR --name MY_LOGGER_NAME --follow --ic --interval 5
```

To use this `kslog` with your canister, expose the query function:

```python
# ##### Import Kybra and the internal function #####

from kybra import Opt, Record, Vec, nat, query
from kybra_simple_logging import get_canister_logs as _get_canister_logs


# Define the PublicLogEntry class directly in the test canister
class PublicLogEntry(Record):
    timestamp: nat
    level: str
    logger_name: str
    message: str
    id: nat


@query
def get_canister_logs(
        from_entry: Opt[nat] = None,
        max_entries: Opt[nat] = None,
        min_level: Opt[str] = None,
        logger_name: Opt[str] = None,
) -> Vec[PublicLogEntry]:
    """
    Re-export the get_canister_logs query function from the library
    This makes it accessible as a query method on the test canister
    """
    logs = _get_canister_logs(
        from_entry=from_entry,
        max_entries=max_entries,
        min_level=min_level,
        logger_name=logger_name
    )

    # Convert the logs to our local PublicLogEntry type
    return [
        PublicLogEntry(
            timestamp=log["timestamp"],
            level=log["level"],
            logger_name=log["logger_name"],
            message=log["message"],
            id=log["id"],
        )
        for log in logs
    ]
```

## Development

```bash
# Clone the repository
git clone https://github.com/smart-social-contracts/kybra-simple-logging.git
cd kybra-simple-logging

# Recommended setup
pyenv install 3.10.7
pyenv local 3.10.7
python -m venv venv
source venv/bin/activate
pip install kybra
python -m kybra install-dfx-extension

# Install development dependencies
pip install -r requirements-dev.txt

# Run linters
./run_linters.sh

# Run tests
cd tests && ./run_test.sh
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT