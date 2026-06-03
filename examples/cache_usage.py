"""Cache adapter example using a Redis-like fake client."""

from __future__ import annotations

from python_core.redis.redis_cache import RedisCache


class FakeRedisClient:
    """Small Redis-like client for examples and tests."""

    def __init__(self) -> None:
        self.values: dict[str, bytes] = {}
        self.ttls: dict[str, int] = {}

    def get(self, key: str) -> bytes | None:
        """Return a value by key."""
        return self.values.get(key)

    def set(self, key: str, value: bytes) -> None:
        """Store a value without a TTL."""
        self.values[key] = value

    def setex(self, key: str, ttl_seconds: int, value: bytes) -> None:
        """Store a value with a TTL."""
        self.values[key] = value
        self.ttls[key] = ttl_seconds

    def delete(self, key: str) -> None:
        """Delete a value and any tracked TTL."""
        self.values.pop(key, None)
        self.ttls.pop(key, None)


def main() -> None:
    """Store, read, and delete a cache value."""
    client = FakeRedisClient()
    cache = RedisCache(client)

    cache.set("customer:cust_123", b'{"id": "cust_123"}', ttl_seconds=60)
    print(cache.get("customer:cust_123"))
    cache.delete("customer:cust_123")
    print(cache.get("customer:cust_123"))


if __name__ == "__main__":
    main()
