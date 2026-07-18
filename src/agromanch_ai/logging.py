"""Structured logging for AgroManch services.

Call :func:`configure_logging` once at process start (every example script
does this). Log level comes from ``AGROMANCH_LOG_LEVEL`` unless overridden,
and ``AGROMANCH_LOG_FORMAT=json`` switches to line-delimited JSON for log
aggregators.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

_LOGGER_NAME = "agromanch"


class JsonFormatter(logging.Formatter):
    """One JSON object per line — friendly to Cloud Logging / Loki / jq."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: str | None = None) -> logging.Logger:
    """Configure the root ``agromanch`` logger and return it.

    Idempotent: repeated calls reconfigure the level but never duplicate
    handlers.
    """
    resolved = (level or os.environ.get("AGROMANCH_LOG_LEVEL", "INFO")).upper()
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(resolved)

    if not logger.handlers:
        handler = logging.StreamHandler()
        if os.environ.get("AGROMANCH_LOG_FORMAT", "").lower() == "json":
            handler.setFormatter(JsonFormatter())
        else:
            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)-7s %(name)s: %(message)s",
                    datefmt="%H:%M:%S",
                )
            )
        logger.addHandler(handler)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Child logger under the ``agromanch`` namespace."""
    return logging.getLogger(f"{_LOGGER_NAME}.{name}")
