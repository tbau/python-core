"""Exception reporter interface."""

from __future__ import annotations

from typing import Any, Protocol


class ExceptionReporter(Protocol):
    """Reports exceptions to logs, telemetry, or alerting systems."""

    def report(self, exc: BaseException, **context: Any) -> None:
        """Report an exception with safe structured context."""
