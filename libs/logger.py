import logging
from logging import (
    handlers,
)  # Do not remove this for logging.handlers.RotatingFileHandler
from datetime import datetime


def get_logger(config):
    log_file_max_bytes = 1024 * 1024 * 100

    logger = logging.getLogger("crawl_log")
    fomatter = logging.Formatter("[%(levelname)s] %(asctime)s > %(message)s")

    today = datetime.today().strftime("%Y%m%d")
    file_handler = logging.handlers.RotatingFileHandler(
        filename=f'{config["log_dir"]}{today}',
        maxBytes=log_file_max_bytes,
        encoding="utf-8",
    )

    file_handler.setFormatter(fomatter)
    logger.addHandler(file_handler)

    # 로거 표현 범위 지정 DEBUG > INFO > WARNING > ERROR > Critical
    logger.setLevel(logging.DEBUG)

    return logger
