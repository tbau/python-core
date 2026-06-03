# Test Framework Guide

## Intent

This repo is a structure reference. The test folder should teach downstream
projects how to organize tests, fakes, builders, and contract checks.

## Layers

- Unit tests: no network, database, Redis, queue, or filesystem unless the file
  behavior is the unit.
- Integration tests: real adapters such as SQLAlchemy, Redis, message brokers,
  FastAPI, or external API sandboxes.
- Contract tests: shared tests that any repository, queue, cache, or gateway
  implementation must pass.

## Useful Test Support

- `tests/fakes`: in-memory implementations such as fake repositories and buses.
- `tests/builders`: object factories for readable setup.
- `tests/fixtures`: reusable setup for databases, Redis, queues, and files.

## Pattern

```python
def test_service_publishes_event() -> None:
    bus = FakeMessageBus()
    service = RegisterUserService(bus)

    service.register("user@example.com")

    assert bus.messages[0].name == "user.registered"
```
