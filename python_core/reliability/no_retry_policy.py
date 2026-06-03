"""No-retry policy."""

from __future__ import annotations


class NoRetryPolicy:
    """Runs the operation once without retry delay."""

    @property
    def attempts(self) -> int:
        """Maximum number of attempts."""
        return 1

    def delay_for_attempt(self, attempt_index: int) -> float:
        """Return no delay."""
        return 0.0
