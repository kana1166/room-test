import logging


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("my_logger")
    # ここに追加の設定を記述できます
    return logger
