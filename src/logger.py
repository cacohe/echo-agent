"""
Logger module - unified configuration, global usage.
All modules use `from src.logger import get_logger`.
Business code MUST NOT call logging.basicConfig().
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get logger instance by name.

    Args:
        name: logger name, recommend passing __name__
        level: log level, defaults to LOG_LEVEL env or INFO

    Returns:
        Configured Logger instance
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level or logging.INFO)

    return logger
