"""Event logger interface."""

from __future__ import annotations

from typing import Any, Protocol


class EventLogger(Protocol):
    """Structured event logger used by services and adapters."""

    def debug(self, event: str, **fields: Any) -> None:
        """Log debug details."""

    def info(self, event: str, **fields: Any) -> None:
        """Log an informational event."""

    def warning(self, event: str, **fields: Any) -> None:
        """Log a warning event."""

    def error(self, event: str, **fields: Any) -> None:
        """Log an error event."""
