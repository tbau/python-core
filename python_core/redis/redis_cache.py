"""Redis cache adapter."""

from __future__ import annotations

from typing import Any


class RedisCache:
    """Small cache adapter around a Redis-like client."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get(self, key: str) -> bytes | None:
        """Return a cached value."""
        return self._client.get(key)

    def set(self, key: str, value: bytes, *, ttl_seconds: int | None = None) -> None:
        """Store a cached value."""
        if ttl_seconds is None:
            self._client.set(key, value)
            return
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self._client.setex(key, ttl_seconds, value)

    def delete(self, key: str) -> None:
        """Delete a cached value."""
        self._client.delete(key)
