from kybra import ic, query

from kybra_simple_logging import logger

@query
def greet() -> str:
    logger.info("Hello from the logger!")
    return "Hello!"
