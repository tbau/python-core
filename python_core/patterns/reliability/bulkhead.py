"""Bulkhead pattern.

Use this to limit concurrent calls to one dependency so saturation in that area
does not consume all application capacity.
"""

from __future__ import annotations

from threading import BoundedSemaphore
from typing import Callable, TypeVar

T = TypeVar("T")


class Bulkhead:
    """Semaphore-backed concurrency limiter for one kind of work."""

    def __init__(self, max_concurrent: int) -> None:
        if max_concurrent < 1:
            raise ValueError("max_concurrent must be at least 1")
        self._semaphore = BoundedSemaphore(max_concurrent)

    def run(self, operation: Callable[[], T]) -> T:
        """Run an operation while holding one bulkhead slot."""

        with self._semaphore:
            return operation()
