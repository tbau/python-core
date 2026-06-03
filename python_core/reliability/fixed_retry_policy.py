"""Fixed-delay retry policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FixedRetryPolicy:
    """Retries with the same delay between attempts."""

    attempts: int = 3
    delay_seconds: float = 0.25

    def __post_init__(self) -> None:
        if self.attempts < 1:
            raise ValueError("attempts must be at least 1")
        if self.delay_seconds < 0:
            raise ValueError("delay_seconds must be non-negative")

    def delay_for_attempt(self, attempt_index: int) -> float:
        """Return a fixed delay."""
        return self.delay_seconds
