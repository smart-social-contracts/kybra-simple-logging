#!/usr/bin/env python3

import argparse
import json
import os
import select
import subprocess
import sys
import time
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="Query and display canister logs")
    parser.add_argument("canister_id", help="Canister ID to query logs from")

    # Log filtering options
    parser.add_argument("--tail", type=int, help="Show only the last N logs")
    parser.add_argument(
        "--level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Minimum log level to display",
    )
    parser.add_argument(
        "--name",
        help="Filter logs by logger name",
    )

    # Follow mode options
    parser.add_argument(
        "--follow", action="store_true", help="Follow logs (poll every 5 seconds)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Polling interval in seconds for follow mode",
    )

    # Network options
    network_group = parser.add_mutually_exclusive_group()
    network_group.add_argument(
        "--network", help="Network URL (e.g., http://localhost:4943)"
    )
    network_group.add_argument("--ic", action="store_true", help="Use the IC mainnet")

    return parser.parse_args()


def get_logs(
    canister_id, tail=None, level=None, network=None, from_entry=None, name=None
):
    """Query log entries from a canister

    Args:
        canister_id: ID of the canister to query
        tail: Maximum number of entries to return (optional)
        level: Minimum log level to include (optional)
        network: Network to query (optional)
        from_entry: Start retrieving logs from this ID (optional)
        name: Filter logs by logger name (optional)

    Returns:
        List of log entries as dictionaries

    Note:
        The parameters are passed to the canister in the following order:
        1. from_entry
        2. max_entries (tail)
        3. min_level (level)
        4. logger_name (name)
    """
    # Build the query arguments in the correct order as expected by the canister API
    args = []

    # 1. from_entry parameter
    if from_entry is not None:
        args.append(f"(opt {from_entry})")
    else:
        args.append("null")

    # 2. tail/max_entries parameter
    if tail is not None:
        args.append(f"(opt {tail})")
    else:
        args.append("null")

    # 3. level/min_level parameter
    if level is not None:
        args.append(f'(opt "{level}")')
    else:
        args.append("null")

    # 4. logger_name parameter
    if name is not None:
        args.append(f'(opt "{name}")')
    else:
        args.append("null")

    query_args = ", ".join(args)

    # Call dfx to query the logs with JSON output
    cmd = ["dfx", "canister", "call", "--output", "json"]

    # Add network option if specified
    if network is not None:
        cmd.extend(["--network", network])

    # Add canister ID and method
    cmd.extend([canister_id, "get_canister_logs", f"({query_args})"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error querying logs: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        sys.exit(1)


def format_log(log_entry):
    # Convert timestamp from nanoseconds to seconds and format as datetime
    try:
        timestamp = datetime.fromtimestamp(int(log_entry["timestamp"]) / 1e9).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    except (ValueError, KeyError):
        timestamp = "Unknown time"

    level = log_entry.get("level", "UNKNOWN")
    name = log_entry.get("logger_name", "unknown")
    message = log_entry.get("message", "")
    id = log_entry.get("id", "unknown")

    # Add colors based on log level
    level_colors = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[91m\033[1m",  # Bold Red
    }
    reset = "\033[0m"
    color = level_colors.get(level, "")

    return f"{timestamp} [{id}] {color}[{level}]{reset} [{name}] {message}"


def main():
    # Set stdout to line buffering mode to ensure timely output when piped
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, line_buffering=True)

    args = parse_args()

    # Determine network option
    network = None
    if args.ic:
        network = "ic"
    elif args.network:
        network = args.network

    if not args.follow:
        # One-time query
        logs = get_logs(
            args.canister_id,
            tail=args.tail,
            level=args.level,
            network=network,
            name=args.name,
        )

        for log in logs:
            print(format_log(log), flush=True)
        return

    # Follow mode
    try:
        last_poll_time = 0
        last_log_id = 0
        first_poll = True

        while True:
            current_time = time.time()
            if (
                first_poll
                or current_time - last_poll_time >= args.interval
                or select.select([sys.stdin], [], [], 0)[0]
            ):
                if select.select([sys.stdin], [], [], 0)[0]:
                    input()

                if first_poll:
                    logs = get_logs(
                        args.canister_id,
                        tail=args.tail,
                        level=args.level,
                        network=network,
                        name=args.name,
                    )
                    first_poll = False
                else:
                    logs = get_logs(
                        args.canister_id,
                        tail=None,
                        level=args.level,
                        network=network,
                        from_entry=last_log_id + 1,
                        name=args.name,
                    )

                last_poll_time = current_time

                for log in logs:
                    print(format_log(log), flush=True)

                # Update the last log ID if we have logs
                if logs:
                    last_log_id = max(int(log.get("id", 0)) for log in logs)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting log follower")


if __name__ == "__main__":
    main()
