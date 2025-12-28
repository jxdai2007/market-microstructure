"""Logging configuration and utilities."""

import logging
import sys
from typing import Optional

from config import LogConfig


def setup_logger(
    name: str,
    level: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Set up and configure a logger.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level or LogConfig.LEVEL)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level or LogConfig.LEVEL)

    # Create formatter
    formatter = logging.Formatter(
        format_string or LogConfig.FORMAT,
        datefmt=LogConfig.DATE_FORMAT
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
