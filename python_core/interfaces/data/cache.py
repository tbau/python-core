"""Cache interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

KeyT = TypeVar("KeyT")
ValueT = TypeVar("ValueT")


class Cache(Protocol[KeyT, ValueT]):
    """Small cache boundary with optional TTL support."""

    def get(self, key: KeyT) -> ValueT | None:
        """Return a cached value or None."""

    def set(self, key: KeyT, value: ValueT, *, ttl_seconds: int | None = None) -> None:
        """Store a cached value."""

    def delete(self, key: KeyT) -> None:
        """Remove a cached value."""
