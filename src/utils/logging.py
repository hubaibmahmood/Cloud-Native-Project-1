"""Structured logging configuration for the Task Management API."""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

from src.utils.settings import settings


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging.

    Formats log records as JSON for easy parsing and aggregation.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON string.

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        return json.dumps(log_data)


class HumanReadableFormatter(logging.Formatter):
    """Human-readable formatter for development."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record for human readability.

        Args:
            record: Log record to format

        Returns:
            Human-readable log string
        """
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {record.levelname:8s} {record.module}:{record.lineno} - {record.getMessage()}"


def setup_logging() -> logging.Logger:
    """Configure application logging based on environment settings.

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("task_api")

    # Remove existing handlers
    logger.handlers.clear()

    # Set log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)

    # Use JSON formatter for production, human-readable for development
    if settings.LOG_LEVEL.upper() == "DEBUG":
        formatter = HumanReadableFormatter()
    else:
        formatter = JSONFormatter()

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Global logger instance
logger = setup_logging()
