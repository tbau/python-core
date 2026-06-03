# Redis Guide

## Intent

Redis should sit behind small interfaces so projects can swap clients, test
with fakes, and avoid leaking Redis commands into services.

## Uses

- Cache
- Distributed locks
- Rate limiting
- Idempotency key storage
- Lightweight pub/sub

## Adapter Shape

`RedisCache` wraps a Redis-like client with `get`, `set`, and `delete`. More
specific adapters should be added only when a project needs them.
