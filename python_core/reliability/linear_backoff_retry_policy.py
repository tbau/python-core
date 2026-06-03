"""Linear backoff retry policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LinearBackoffRetryPolicy:
    """Retries with delay growing linearly by attempt."""

    attempts: int = 3
    step_seconds: float = 0.25
    max_delay: float = 5.0

    def __post_init__(self) -> None:
        if self.attempts < 1:
            raise ValueError("attempts must be at least 1")
        if self.step_seconds < 0 or self.max_delay < 0:
            raise ValueError("delays must be non-negative")

    def delay_for_attempt(self, attempt_index: int) -> float:
        """Return bounded linear delay."""
        return min(self.step_seconds * (attempt_index + 1), self.max_delay)
