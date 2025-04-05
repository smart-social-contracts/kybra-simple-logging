#!/usr/bin/env python3

from kybra_simple_logging import (  # In-memory logging imports
    clear_logs,
    disable_logging,
    disable_memory_logging,
    enable_logging,
    enable_memory_logging,
    get_logger,
    get_logs,
    is_memory_logging_enabled,
    logger,
    set_log_level,
    set_max_log_entries,
)


def custom_print(message):
    """Print wrapper that works in both normal and IC environments"""
    try:
        from kybra import ic

        ic.print(message)
    except:
        print(message)


def run_tests():
    """Run all memory logging tests"""
    failures = 0
    total = 0

    custom_print("\n=== Testing Memory Logging ===\n")

    # Test 1: Basic Memory Logging
    total += 1
    try:
        test_basic_memory_logging()
        custom_print("✓ Basic memory logging test passed!")
    except AssertionError as e:
        custom_print(f"✗ Basic memory logging test FAILED: {e}")
        failures += 1

    # Test 2: Log Filtering
    total += 1
    try:
        test_log_filtering()
        custom_print("✓ Log filtering test passed!")
    except AssertionError as e:
        custom_print(f"✗ Log filtering test FAILED: {e}")
        failures += 1

    # Test 3: Max Entries
    total += 1
    try:
        test_max_entries()
        custom_print("✓ Max entries test passed!")
    except AssertionError as e:
        custom_print(f"✗ Max entries test FAILED: {e}")
        failures += 1

    # Test 4: Memory Logging Toggle
    total += 1
    try:
        test_memory_logging_toggle()
        custom_print("✓ Memory logging toggle test passed!")
    except AssertionError as e:
        custom_print(f"✗ Memory logging toggle test FAILED: {e}")
        failures += 1

    custom_print("\n=== Memory Logging Tests Complete ===")
    custom_print(f"Ran {total} tests with {failures} failures")

    return failures


def test_basic_memory_logging():
    """Test basic in-memory logging functionality"""
    custom_print("Testing basic memory logging...")

    # Clear any existing logs
    clear_logs()

    # Set the memory_test logger to DEBUG level to capture all logs
    test_logger = get_logger("memory_test")
    test_logger.set_level("DEBUG")

    # Create logs with different loggers and levels
    logger.info("[MEMORY-TEST] Info message from default logger")
    test_logger.debug("[MEMORY-TEST] Debug message")
    test_logger.warning("[MEMORY-TEST] Warning message")
    test_logger.error("[MEMORY-TEST] Error message")

    # Retrieve logs and verify they were stored
    logs = get_logs()
    custom_print(f"Retrieved {len(logs)} log entries")

    # Check that logs exist - now we should have at least 4 logs (including the debug log)
    assert len(logs) >= 4, f"Expected at least 4 logs, but found {len(logs)}"

    # Check for specific log entries
    info_found = False
    warning_found = False
    error_found = False

    for log in logs:
        if "[MEMORY-TEST] Info message from default logger" in log["message"]:
            info_found = True
            assert log["level"] == "INFO", f"Expected INFO level, got {log['level']}"
            assert (
                log["logger_name"] == "kybra_simple_logging"
            ), f"Expected kybra_simple_logging logger, got {log['logger_name']}"

        if "[MEMORY-TEST] Warning message" in log["message"]:
            warning_found = True
            assert (
                log["level"] == "WARNING"
            ), f"Expected WARNING level, got {log['level']}"
            assert (
                log["logger_name"] == "memory_test"
            ), f"Expected memory_test logger, got {log['logger_name']}"

        if "[MEMORY-TEST] Error message" in log["message"]:
            error_found = True
            assert log["level"] == "ERROR", f"Expected ERROR level, got {log['level']}"
            assert (
                log["logger_name"] == "memory_test"
            ), f"Expected memory_test logger, got {log['logger_name']}"

    assert info_found, "Info log entry not found in memory"
    assert warning_found, "Warning log entry not found in memory"
    assert error_found, "Error log entry not found in memory"


def test_log_filtering():
    """Test log filtering capabilities"""
    custom_print("Testing log filtering...")

    # Clear logs and set up test
    clear_logs()
    default_logger = logger
    error_logger = get_logger("error_only")
    info_logger = get_logger("info_only")

    # Create logs with different levels and loggers
    default_logger.debug("[FILTER-TEST] Debug from default")
    default_logger.info("[FILTER-TEST] Info from default")
    default_logger.error("[FILTER-TEST] Error from default")

    error_logger.debug("[FILTER-TEST] Debug from error_only")
    error_logger.error("[FILTER-TEST] Error from error_only")

    info_logger.info("[FILTER-TEST] Info from info_only")

    # 1. Test filtering by level
    error_logs = get_logs(min_level="ERROR")
    custom_print(f"Retrieved {len(error_logs)} ERROR logs")

    assert (
        len(error_logs) >= 2
    ), f"Expected at least 2 ERROR logs, found {len(error_logs)}"
    for log in error_logs:
        assert log["level"] in [
            "ERROR",
            "CRITICAL",
        ], f"Found non-ERROR level in ERROR logs: {log['level']}"

    # 2. Test filtering by logger
    info_only_logs = get_logs(logger_name="info_only")
    custom_print(f"Retrieved {len(info_only_logs)} logs from info_only logger")

    assert (
        len(info_only_logs) >= 1
    ), f"Expected at least 1 info_only log, found {len(info_only_logs)}"
    for log in info_only_logs:
        assert (
            log["logger_name"] == "info_only"
        ), f"Found wrong logger in info_only logs: {log['logger_name']}"

    # 3. Test combined filtering
    default_info_logs = get_logs(min_level="INFO", logger_name="kybra_simple_logging")
    custom_print(f"Retrieved {len(default_info_logs)} INFO+ logs from default logger")

    for log in default_info_logs:
        assert (
            log["logger_name"] == "kybra_simple_logging"
        ), f"Found wrong logger in combined filter: {log['logger_name']}"
        assert log["level"] in [
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ], f"Found invalid level in INFO+ logs: {log['level']}"
        assert log["level"] != "DEBUG", "DEBUG level found in INFO+ logs"


def test_max_entries():
    """Test maximum entries limit functionality"""
    custom_print("Testing max entries limit...")

    # Set a small limit to test circular buffer behavior
    set_max_log_entries(5)
    clear_logs()

    # Create more logs than the limit
    for i in range(10):
        logger.info(f"[MAX-TEST] Log message {i}")

    # Check we only have the max number of logs
    logs = get_logs()
    custom_print(f"Retrieved {len(logs)} logs after setting max to 5")

    assert len(logs) == 5, f"Expected exactly 5 logs, found {len(logs)}"


def test_memory_logging_toggle():
    """Test enabling and disabling memory logging functionality"""
    custom_print("Testing memory logging enable/disable...")

    # Start with a clean state
    clear_logs()
    enable_memory_logging()  # Make sure memory logging is enabled first

    # First, verify memory logging is working when enabled
    test_logger = get_logger("toggle_test")
    initial_status = is_memory_logging_enabled()
    custom_print(f"Initial memory logging status: {initial_status}")
    assert initial_status, "Memory logging should be enabled by default"

    # Log a message when memory logging is enabled
    test_logger.info("[TOGGLE-TEST] This message should be stored (enabled)")
    logs_before = get_logs()
    assert (
        len(logs_before) > 0
    ), "Expected at least one log message when memory logging is enabled"
    assert any(
        "[TOGGLE-TEST] This message should be stored (enabled)" in log["message"]
        for log in logs_before
    ), "Test message not found in logs when memory logging was enabled"

    # Now disable memory logging
    disable_memory_logging()
    disabled_status = is_memory_logging_enabled()
    custom_print(f"Memory logging status after disable: {disabled_status}")
    assert (
        not disabled_status
    ), "Memory logging should be disabled after calling disable_memory_logging()"

    # Log more messages when disabled (these should not be captured)
    test_logger.info("[TOGGLE-TEST] This message should NOT be stored (disabled)")
    test_logger.error("[TOGGLE-TEST] This error should NOT be stored (disabled)")

    # Get logs to ensure nothing new was added
    logs_during_disable = get_logs()
    custom_print(
        f"Found {len(logs_during_disable)} logs when checking during disabled state"
    )

    # Count shouldn't have increased (might even be less if other tests cleared logs)
    assert all(
        "[TOGGLE-TEST] This message should NOT be stored" not in log["message"]
        for log in logs_during_disable
    ), "Found a log message that should NOT have been captured while memory logging was disabled"

    # Re-enable memory logging
    enable_memory_logging()
    reenabled_status = is_memory_logging_enabled()
    custom_print(f"Memory logging status after re-enable: {reenabled_status}")
    assert (
        reenabled_status
    ), "Memory logging should be enabled after calling enable_memory_logging()"

    # Log more messages when re-enabled
    test_logger.info("[TOGGLE-TEST] This message should be stored again (re-enabled)")

    # Check that new logs are being captured again
    logs_after = get_logs()
    custom_print(f"Found {len(logs_after)} logs after re-enabling")

    assert any(
        "[TOGGLE-TEST] This message should be stored again (re-enabled)"
        in log["message"]
        for log in logs_after
    ), "Test message not found in logs after re-enabling memory logging"


if __name__ == "__main__":
    import sys

    sys.exit(run_tests())
