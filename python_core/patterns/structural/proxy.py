"""Proxy pattern.

Use this when access to an object needs to be controlled, delayed, cached, or
guarded without changing the object itself.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class LazyProxy:
    """Proxy that defers object creation until first use."""

    def __init__(self, factory: Callable[[], T]) -> None:
        self._factory = factory
        self._value: T | None = None

    def get(self) -> T:
        """Return the proxied value, creating it if needed."""

        if self._value is None:
            self._value = self._factory()
        return self._value
