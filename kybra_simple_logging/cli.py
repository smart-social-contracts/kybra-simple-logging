#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
import time
import select
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


def get_logs(canister_id, tail=None, level=None, network=None, from_entry=None):
    """Query log entries from a canister
    
    Args:
        canister_id: ID of the canister to query
        tail: Maximum number of entries to return (optional)
        level: Minimum log level to include (optional)
        network: Network to query (optional)
        from_entry: Start retrieving logs from this ID (optional)
        
    Returns:
        List of log entries as dictionaries
    
    Note:
        The parameters are passed to the canister in the following order:
        1. from_entry
        2. max_entries (tail)
        3. min_level (level)
        4. logger_name (always null in CLI)
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
    
    # 4. logger_name parameter (always null in our CLI)
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
            last_poll_time = 0
            last_log_id = 0  # Track the ID of the last log we've seen
            all_displayed_logs = []  # Keep track of all logs we've displayed
            first_poll = True  # Flag for first poll
            
            while True:
                current_time = time.time()
                force_refresh = False
                
                # Check if it's time to poll or if there's input available
                if current_time - last_poll_time >= args.interval or select.select([sys.stdin], [], [], 0)[0]:
                    # If there's input, consume it and force a full refresh
                    if select.select([sys.stdin], [], [], 0)[0]:
                        input()
                        force_refresh = True
                    
                    # On first poll or manual refresh, get all logs
                    if first_poll or force_refresh:
                        logs = get_logs(args.canister_id, args.tail, args.level, network)
                        all_displayed_logs = logs
                        first_poll = False
                    else:
                        # Get only new logs using from_entry
                        logs = get_logs(args.canister_id, None, args.level, network, from_entry=last_log_id + 1)
                        all_displayed_logs.extend(logs)
                    
                    last_poll_time = current_time
                    
                    # Update the last log ID if we have logs
                    if logs:
                        last_log_id = max(int(log.get("id", 0)) for log in logs)
                    
                    # Trim if we have a tail limit
                    if args.tail is not None and len(all_displayed_logs) > args.tail:
                        all_displayed_logs = all_displayed_logs[-args.tail:]
                    
                    # Clear screen and print all logs
                    print("\033c", end="")
                    for log in all_displayed_logs:
                        print(format_log(log))
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting log follower")
    else:
        # One-time query
        logs = get_logs(args.canister_id, args.tail, args.level, network)
        for log in logs:
            print(format_log(log))


if __name__ == "__main__":
    main()
