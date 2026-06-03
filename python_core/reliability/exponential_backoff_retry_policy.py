"""Exponential backoff retry policy."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class ExponentialBackoffRetryPolicy:
    """Retries with exponential backoff and optional jitter."""

    attempts: int = 3
    base_delay: float = 0.25
    max_delay: float = 5.0
    backoff: float = 2.0
    jitter: float = 0.1

    def __post_init__(self) -> None:
        if self.attempts < 1:
            raise ValueError("attempts must be at least 1")
        if self.base_delay < 0 or self.max_delay < 0:
            raise ValueError("delays must be non-negative")
        if self.backoff < 1:
            raise ValueError("backoff must be at least 1")
        if self.jitter < 0:
            raise ValueError("jitter must be non-negative")

    def delay_for_attempt(self, attempt_index: int) -> float:
        """Return bounded exponential delay."""
        raw_delay = self.base_delay * (self.backoff**attempt_index)
        bounded = min(raw_delay, self.max_delay)
        if self.jitter == 0:
            return bounded
        return bounded + random.uniform(0, self.jitter)
