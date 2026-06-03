"""Adapter pattern.

Use this when existing code has the behavior you need but exposes the wrong
interface for your current code.
"""

from __future__ import annotations


class LegacyLogger:
    """Existing incompatible logger with a low-level ``write`` method."""

    def write(self, message: str) -> None:
        """Write a raw log message."""

        print(message)


class LoggerAdapter:
    """Adapts ``LegacyLogger`` to an event-style ``info`` interface."""

    def __init__(self, logger: LegacyLogger) -> None:
        self._logger = logger

    def info(self, event: str, **fields: object) -> None:
        """Log a structured event through the legacy logger."""

        self._logger.write(f"{event}: {fields}")
