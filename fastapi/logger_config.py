import logging


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("my_logger")
    return logger
