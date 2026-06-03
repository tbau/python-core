"""Async session factory interface for SQLAlchemy adapters."""

from __future__ import annotations

from typing import Any, Protocol


class AsyncSessionFactory(Protocol):
    """Callable that returns a SQLAlchemy AsyncSession-like object."""

    def __call__(self) -> Any:
        """Create a new async session."""
