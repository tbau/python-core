"""Decorator pattern.

Use this to add behavior around a function or object without changing the
original implementation.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import TypeVar

T = TypeVar("T")


def audit(event: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Return a decorator that prints audit messages before and after a call."""

    def decorate(func: Callable[..., T]) -> Callable[..., T]:
        """Wrap one function with audit logging."""

        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> T:
            """Run the wrapped function between audit messages."""

            print(f"audit.start {event}")
            result = func(*args, **kwargs)
            print(f"audit.end {event}")
            return result

        return wrapper

    return decorate
