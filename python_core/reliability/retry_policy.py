"""Retry policy interface."""

from __future__ import annotations

from typing import Protocol


class RetryPolicy(Protocol):
    """Interface for retry attempt counts and delays."""

    @property
    def attempts(self) -> int:
        """Maximum number of attempts."""

    def delay_for_attempt(self, attempt_index: int) -> float:
        """Return delay before the next retry attempt."""
