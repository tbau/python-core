"""Standard event logger."""

from __future__ import annotations

import logging
from typing import Any


class StandardEventLogger:
    """Adapts stdlib logging to the EventLogger interface."""

    def __init__(self, name: str = "python_core") -> None:
        self._logger = logging.getLogger(name)

    def debug(self, event: str, **fields: Any) -> None:
        """Log a debug event with structured fields."""

        self._logger.debug(event, extra={"fields": fields})

    def info(self, event: str, **fields: Any) -> None:
        """Log an info event with structured fields."""

        self._logger.info(event, extra={"fields": fields})

    def warning(self, event: str, **fields: Any) -> None:
        """Log a warning event with structured fields."""

        self._logger.warning(event, extra={"fields": fields})

    def error(self, event: str, **fields: Any) -> None:
        """Log an error event with structured fields."""

        self._logger.error(event, extra={"fields": fields})
