 # dfx-logs: Canister Log Viewer CLI

A command-line tool for viewing logs from Internet Computer canisters that use the kybra-simple-logging library.

## Installation

You can install the CLI tool system-wide:

```bash
# Install from the project directory
pip install -e .

# Or install directly
pip install git+https://github.com/smart-social-contracts/kybra-simple-logging.git
```

After installation, the `dfx-logs` command will be available globally in your system.

## Usage

Basic usage:

```bash
# View all logs from a canister
dfx-logs rrkah-fqaaa-aaaaa-aaaaq-cai

# Show only the last 10 logs
dfx-logs rrkah-fqaaa-aaaaa-aaaaq-cai --tail 10

# Show only ERROR and CRITICAL logs
dfx-logs rrkah-fqaaa-aaaaa-aaaaq-cai --level ERROR

# Follow logs with updates every 5 seconds
dfx-logs rrkah-fqaaa-aaaaa-aaaaq-cai --follow

# Use a custom polling interval (in seconds)
dfx-logs rrkah-fqaaa-aaaaa-aaaaq-cai --follow --interval 10

# Connect to a specific network
dfx-logs rrkah-fqaaa-aaaaa-aaaaq-cai --network http://localhost:8080

# Connect to mainnet
dfx-logs rrkah-fqaaa-aaaaa-aaaaq-cai --ic
```

## Requirements

- Python 3.7+
- dfx command-line tool
- A canister that uses kybra-simple-logging and exports the `get_canister_logs` query function

## How It Works

The CLI tool connects to a canister that has incorporated the kybra-simple-logging library and re-exported the `get_canister_logs` function. It retrieves and formats logs for easy viewing in the terminal.

For follow mode, the tool polls the canister at regular intervals to show new logs as they become available.

## Adding Logging to Your Canister

To use this CLI tool with your canister, you need to:

1. Import kybra-simple-logging in your canister
2. Re-export the query function in your canister

Example code:

```python
from kybra import query, Record, Opt, Vec
from kybra_simple_logging import get_canister_logs_internal

# Define the PublicLogEntry class in your canister
class PublicLogEntry(Record):
    timestamp: float
    level: str
    logger_name: str
    message: str
    id: int

# Re-export as a query function
@query
def get_canister_logs(
    max_entries: Opt[int] = None,
    min_level: Opt[str] = None,
    logger_name: Opt[str] = None,
) -> Vec[PublicLogEntry]:
    logs = get_canister_logs_internal(
        max_entries=max_entries,
        min_level=min_level,
        logger_name=logger_name
    )
    
    # Convert the logs to the local PublicLogEntry type
    return [
        PublicLogEntry(
            timestamp=log.timestamp,
            level=log.level,
            logger_name=log.logger_name,
            message=log.message,
            id=log.id
        ) for log in logs
    ]
```
