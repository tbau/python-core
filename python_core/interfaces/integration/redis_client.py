"""Redis client interface."""

from __future__ import annotations

from typing import Protocol


class RedisClient(Protocol):
    """Small Redis boundary for cache and coordination code."""

    def get(self, key: str) -> bytes | None:
        """Return a value by key."""

    def set(self, key: str, value: bytes, *, ttl_seconds: int | None = None) -> None:
        """Store a value with an optional TTL."""

    def delete(self, key: str) -> None:
        """Delete a key."""
