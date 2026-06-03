"""Object pool pattern.

Use this when creating objects is expensive and a bounded set of reusable
instances is safer than creating new ones for every request.
"""

from __future__ import annotations

from collections.abc import Callable
from queue import SimpleQueue
from typing import Generic, TypeVar

T = TypeVar("T")


class ObjectPool(Generic[T]):
    """Small blocking pool of reusable objects."""

    def __init__(self, factory: Callable[[], T], *, size: int) -> None:
        self._items: SimpleQueue[T] = SimpleQueue()
        for _ in range(size):
            self._items.put(factory())

    def acquire(self) -> T:
        """Take an item from the pool, blocking until one is available."""

        return self._items.get()

    def release(self, item: T) -> None:
        """Return an item to the pool."""

        self._items.put(item)
