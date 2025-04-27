#!/usr/bin/env python3

from kybra_simple_logging import (  # In-memory logging imports
    Level,
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

    # Test 5: Log Entry IDs and Order
    total += 1
    try:
        test_log_entry_ids()
        custom_print("✓ Log entry ID and ordering test passed!")
    except AssertionError as e:
        custom_print(f"✗ Log entry ID and ordering test FAILED: {e}")
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
    test_logger.set_level(Level.DEBUG)

    # Create logs with different loggers and levels
    logger.info("[MEMORY-TEST] Info message from default logger")
    test_logger.debug("[MEMORY-TEST] Debug message")
    test_logger.warning("[MEMORY-TEST] Warning message")
    test_logger.error("[MEMORY-TEST] Error message")

    # Retrieve logs and verify
    logs = get_logs()
    custom_print(f"Retrieved {len(logs)} memory logs")

    # Check that logs contain all expected messages
    debug_found = False
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

        if "[MEMORY-TEST] Debug message" in log["message"]:
            debug_found = True
            assert log["level"] == "DEBUG", f"Expected DEBUG level, got {log['level']}"
            assert (
                log["logger_name"] == "memory_test"
            ), f"Expected memory_test logger, got {log['logger_name']}"

    # Verify all messages were found
    assert info_found, "INFO message not found in logs"
    assert warning_found, "WARNING message not found in logs"
    assert error_found, "ERROR message not found in logs"
    assert debug_found, "DEBUG message not found in logs"


def test_log_filtering():
    # Test log filtering capabilities
    custom_print("Testing log filtering...")

    # Clear existing logs
    clear_logs()

    # Create logs with different loggers and levels for testing filtering
    error_logger = get_logger("error_only")
    set_log_level(Level.ERROR, "error_only")

    info_logger = get_logger("info_only")
    set_log_level(Level.INFO, "info_only")

    # Generate test logs
    error_logger.debug("[FILTER-TEST] Debug from error_only - should not appear")
    error_logger.info("[FILTER-TEST] Info from error_only - should not appear")
    error_logger.error("[FILTER-TEST] Error from error_only")
    error_logger.critical("[FILTER-TEST] Critical from error_only")

    info_logger.debug("[FILTER-TEST] Debug from info_only - should not appear")
    info_logger.info("[FILTER-TEST] Info from info_only")

    # 1. Test filtering by level
    error_logs = get_logs(min_level=Level.ERROR)
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

    for log in info_only_logs:
        assert (
            log["logger_name"] == "info_only"
        ), f"Found wrong logger in info_only logs: {log['logger_name']}"

    # 3. Test combined filtering
    default_info_logs = get_logs(
        min_level=Level.INFO, logger_name="kybra_simple_logging"
    )
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
    # Test maximum entries limit functionality
    custom_print("Testing max entries limit...")

    # Set a small max entries value
    original_max = 1000  # Default
    set_max_log_entries(5)

    # Clear existing logs
    clear_logs()

    # Generate more logs than the max
    test_logger = get_logger("max_test")
    for i in range(10):
        test_logger.info(f"[MAX-TEST] Log message {i}")

    # Get logs and check that only max_entries are returned
    logs = get_logs()
    custom_print(f"Retrieved {len(logs)} logs after setting max_entries=5")

    # Restore original max for other tests
    set_max_log_entries(original_max)

    assert len(logs) == 5, f"Expected exactly 5 logs, found {len(logs)}"


def test_memory_logging_toggle():
    """Test enabling and disabling in-memory logging"""
    custom_print("Testing memory logging toggle...")

    # First make sure memory logging is enabled
    enable_memory_logging()
    assert is_memory_logging_enabled(), "Memory logging should be enabled"

    # Clear existing logs
    clear_logs()

    # Log some messages with memory logging enabled
    logger.info("[TOGGLE-TEST] Memory logging enabled")

    # Get logs and verify they're stored
    logs_before = get_logs()
    custom_print(f"Retrieved {len(logs_before)} logs before disabling")

    memory_enabled_found = False
    for log in logs_before:
        if "[TOGGLE-TEST] Memory logging enabled" in log["message"]:
            memory_enabled_found = True
            assert log["level"] == "INFO", f"Expected INFO level, got {log['level']}"

    assert memory_enabled_found, "Could not find memory enabled log message"

    # Now disable memory logging
    disable_memory_logging()
    assert not is_memory_logging_enabled(), "Memory logging should be disabled"

    # Log some messages with memory logging disabled
    logger.warning("[TOGGLE-TEST] Memory logging disabled")

    # Get logs and verify the disabled messages are not stored
    logs_after_disable = get_logs()
    custom_print(f"Retrieved {len(logs_after_disable)} logs after disabling")
    assert len(logs_after_disable) == len(
        logs_before
    ), "Log count should not change when logging is disabled"

    # Make sure that even after retrieving, the disabled log isn't there
    memory_disabled_found = False
    for log in get_logs():
        if "[TOGGLE-TEST] Memory logging disabled" in log["message"]:
            memory_disabled_found = True

    assert (
        not memory_disabled_found
    ), "Found log message that was logged with memory logging disabled"

    # Now re-enable memory logging
    enable_memory_logging()
    assert is_memory_logging_enabled(), "Memory logging should be re-enabled"

    # Log some messages with memory logging re-enabled
    logger.error("[TOGGLE-TEST] Memory logging re-enabled")

    # Get logs and verify that new messages are stored again
    logs_after_enable = get_logs()
    custom_print(f"Retrieved {len(logs_after_enable)} logs after re-enabling")
    assert len(logs_after_enable) > len(
        logs_after_disable
    ), "Log count should increase after re-enabling"

    memory_reenabled_found = False
    for log in logs_after_enable:
        if "[TOGGLE-TEST] Memory logging re-enabled" in log["message"]:
            memory_reenabled_found = True
            assert log["level"] == "ERROR", f"Expected ERROR level, got {log['level']}"

    assert memory_reenabled_found, "Could not find memory re-enabled log message"


def test_log_entry_ids():
    """Test log entry ID assignment and retrieval"""
    custom_print("Testing log entry IDs and ordering...")

    # Clear existing logs
    clear_logs()

    # Create a sequence of logs
    logger.info("[ID-TEST] First message")
    logger.warning("[ID-TEST] Second message")
    logger.error("[ID-TEST] Third message")

    # Get all logs and verify sequence
    all_logs = get_logs()
    custom_print(f"Retrieved {len(all_logs)} logs for ID test")

    # Verify we have at least 3 logs with sequential IDs
    assert len(all_logs) >= 3, f"Expected at least 3 logs, found {len(all_logs)}"

    # Find our test logs
    test_logs = []
    for log in all_logs:
        if "[ID-TEST]" in log["message"]:
            test_logs.append(log)

    # Sort by ID for safety
    test_logs.sort(key=lambda x: x["id"])

    # Verify the test logs
    assert len(test_logs) == 3, f"Expected 3 test logs, found {len(test_logs)}"

    assert (
        test_logs[0]["message"] == "[ID-TEST] First message"
    ), "First message doesn't match"
    assert (
        test_logs[0]["level"] == "INFO"
    ), f"Expected INFO level, got {test_logs[0]['level']}"

    assert (
        test_logs[1]["message"] == "[ID-TEST] Second message"
    ), "Second message doesn't match"
    assert (
        test_logs[1]["level"] == "WARNING"
    ), f"Expected WARNING level, got {test_logs[1]['level']}"

    assert (
        test_logs[2]["message"] == "[ID-TEST] Third message"
    ), "Third message doesn't match"
    assert (
        test_logs[2]["level"] == "ERROR"
    ), f"Expected ERROR level, got {test_logs[2]['level']}"

    # Verify IDs are sequential
    assert (
        test_logs[0]["id"] < test_logs[1]["id"] < test_logs[2]["id"]
    ), "Log IDs are not sequential"

    # Now test from_entry parameter
    logs_from_second = get_logs(from_entry=test_logs[1]["id"])
    custom_print(f"Retrieved {len(logs_from_second)} logs after second message")

    # Verify we don't get the first message
    first_found = False
    for log in logs_from_second:
        if log["message"] == "[ID-TEST] First message":
            first_found = True

    assert not first_found, "First message should be filtered out when using from_entry"

    # Verify we do get the second and third messages
    second_found = False
    third_found = False
    for log in logs_from_second:
        if log["message"] == "[ID-TEST] Second message":
            second_found = True
        elif log["message"] == "[ID-TEST] Third message":
            third_found = True

    assert second_found, "Second message not found when using from_entry"
    assert third_found, "Third message not found when using from_entry"

    # Test max_entries parameter
    limited_logs = get_logs(max_entries=1)
    custom_print(f"Retrieved {len(limited_logs)} logs with max_entries=1")
    assert len(limited_logs) == 1, f"Expected 1 log, found {len(limited_logs)}"

    # Create more logs and test combining parameters
    logger.critical("[ID-TEST] Fourth message")
    logger.debug("[ID-TEST] Fifth message")

    # Combined test: from_entry + max_entries
    combined_logs = get_logs(from_entry=test_logs[1]["id"], max_entries=2)
    custom_print(f"Retrieved {len(combined_logs)} logs with from_entry + max_entries")
    assert len(combined_logs) == 2, f"Expected 2 logs, found {len(combined_logs)}"

    # Combined test: from_entry + min_level
    high_level_logs = get_logs(from_entry=test_logs[1]["id"], min_level=Level.ERROR)
    custom_print(
        f"Retrieved {len(high_level_logs)} logs with from_entry + min_level=ERROR"
    )

    # Should only get ERROR and CRITICAL messages after the second message
    for log in high_level_logs:
        assert log["level"] in [
            "ERROR",
            "CRITICAL",
        ], f"Found non-ERROR/CRITICAL level in filtered logs: {log['level']}"


if __name__ == "__main__":
    import sys

    sys.exit(run_tests())
