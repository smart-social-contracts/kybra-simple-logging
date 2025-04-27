from kybra import ic, query, heartbeat, void

from kybra_simple_logging import get_logger


@heartbeat
def heartbeat_() -> void:
    logger = get_logger("heartbeat")
    logger.info("Heartbeat")
    logger.debug("Heartbeat")
    logger.warning("Heartbeat")
    logger.error("Heartbeat")
    logger.critical("Heartbeat")



# ##### Import Kybra and the internal function #####

from kybra import Opt, Record, Vec, ic, nat, query, update  # noqa: E402

from kybra_simple_logging import get_canister_logs as _get_canister_logs  # noqa: E402


# Define the PublicLogEntry class directly in the test canister
class PublicLogEntry(Record):
    timestamp: nat
    level: str
    logger_name: str
    message: str
    id: nat


@query
def get_canister_logs(
    max_entries: Opt[int] = None,
    min_level: Opt[str] = None,
    logger_name: Opt[str] = None,
) -> Vec[PublicLogEntry]:
    """
    Re-export the get_canister_logs query function from the library
    This makes it accessible as a query method on the test canister
    """
    logs = _get_canister_logs(
        max_entries=max_entries, min_level=min_level, logger_name=logger_name
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
