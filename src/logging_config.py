
# Tracks API failures and row counts.
import logging
import sys
from typing import Optional


def configure_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("etl")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name:
        return logging.getLogger(name)
    return logging.getLogger("etl")