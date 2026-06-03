"""Circuit breaker pattern.

Use this to stop calling a dependency after repeated failures, giving it time to
recover instead of making every caller wait for another failure.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class CircuitBreaker:
    """Tiny failure-count circuit breaker example."""

    def __init__(self, *, failure_limit: int) -> None:
        self.failure_limit = failure_limit
        self.failures = 0
        self.open = False

    def call(self, operation: Callable[[], T]) -> T:
        """Run an operation unless the circuit is open."""

        if self.open:
            raise RuntimeError("circuit is open")
        try:
            result = operation()
        except Exception:
            self.failures += 1
            self.open = self.failures >= self.failure_limit
            raise
        self.failures = 0
        return result
