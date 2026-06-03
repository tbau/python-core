"""Singleton provider pattern.

Use this to lazily create and reuse one instance behind a small provider object.
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class SingletonProvider(Generic[T]):
    """Lazily creates one instance from a factory and reuses it."""

    def __init__(self, factory: Callable[[], T]) -> None:
        self._factory = factory
        self._instance: T | None = None

    def get(self) -> T:
        """Return the existing instance or create it on first access."""

        if self._instance is None:
            self._instance = self._factory()
        return self._instance
