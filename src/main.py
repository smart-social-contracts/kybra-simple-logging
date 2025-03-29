from kybra import ic, query

from kybra_simple_logging import logger, set_log_level, get_logger


def logging_test(l: "SimpleLogger"):
    ic.print('******************')
    l.debug('Hello from DEBUG in ' + l.name)
    l.info("Hello from INFO in " + l.name)
    l.warning('Hello from WARNING in ' + l.name)
    l.error('Hello from ERROR in ' + l.name)
    l.critical('Hello from CRITICAL in ' + l.name)


@query
def greet() -> str:
    logging_test(logger)
    set_log_level("DEBUG")
    logging_test(logger)

    
    my_logger_1 = get_logger("my_logger_1")
    logging_test(my_logger_1)
    logging_test(logger)

    set_log_level("ERROR", "my_logger_1")
    logging_test(my_logger_1)
    logging_test(logger)
    

    return "end"

