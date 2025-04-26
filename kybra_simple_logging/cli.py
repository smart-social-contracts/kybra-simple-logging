#!/usr/bin/env python3

import argparse
import json
import os
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


def get_logs(canister_id, tail=None, level=None, network=None):
    # Build the query arguments
    args = []
    if tail is not None:
        args.append(f"(opt {tail})")
    else:
        args.append("null")

    if level is not None:
        args.append(f'(opt "{level}")')
    else:
        args.append("null")

    args.append("null")  # logger_name is null

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
    logger = log_entry.get("logger_name", "unknown")
    message = log_entry.get("message", "")

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

    return f"{timestamp} {color}[{level}]{reset} [{logger}] {message}"


def main():
    args = parse_args()

    # Determine network option
    network = None
    if args.ic:
        network = "ic"
    elif args.network:
        network = args.network

    if args.follow:
        # Follow mode
        try:
            while True:
                logs = get_logs(args.canister_id, args.tail, args.level, network)

                # Clear screen and print logs
                print("\033c", end="")
                for log in logs:
                    print(format_log(log))

                network_display = f" on {network}" if network else ""
                print(
                    f"\nPolling logs from {args.canister_id}{network_display}... (Ctrl+C to quit)"
                )
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nExiting log follower")
    else:
        # One-time query
        logs = get_logs(args.canister_id, args.tail, args.level, network)
        for log in logs:
            print(format_log(log))


if __name__ == "__main__":
    main()
