# Test Framework

This folder is a template for downstream projects.

## Suggested Layout

```text
tests/
  unit/          pure logic, no network or database
  integration/   real adapters, databases, queues, Redis, and HTTP clients
  contract/      interface compliance tests for repositories and gateways
  fakes/         in-memory implementations for services
  builders/      readable object factories for tests
```

## Naming

- `test_<behavior>.py` for unit tests.
- `test_<adapter>_integration.py` for adapter tests.
- `test_<interface>_contract.py` for reusable interface tests.

## Rule

Tests should show how a project is meant to be structured. Keep fakes small,
named by intent, and close to the interface they replace.
