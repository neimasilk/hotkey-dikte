"""Logging configuration for Hotkey Dikte application.

This module sets up structured logging using Loguru with proper formatting,
log rotation, and log level configuration.
"""

from pathlib import Path
from loguru import logger
import sys

def setup_logging(log_path: Path = None) -> None:
    """Configure logging settings.

    Args:
        log_path: Path to the log file. If None, logs to stderr only.
    """
    # Remove default handler
    logger.remove()

    # Add stderr handler with custom format
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # Add file handler if log_path is provided
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            str(log_path),
            rotation="10 MB",
            retention="1 week",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level="DEBUG"
        )

def get_logger(name: str = __name__):
    """Get a logger instance with the specified name.

    Args:
        name: Name for the logger, typically __name__ of the calling module.

    Returns:
        Logger instance configured with the specified name.
    """
    return logger.bind(name=name)