# Architecture Guide

## Package Shape

`python_core` is organized around stable concepts:

- `interfaces`: shared protocols for services, databases, parsers, logging,
  exceptions, external APIs, idempotency checks, and data access.
- `exceptions`: grouped failures for common, security, integration, persistence,
  reliability, and web concerns.
- `reliability`: timeout, retry, and idempotency primitives.
- `external_api`: external API client scaffolding.
- `db`: database interfaces and adapter packages such as `db/sqlalchemy`.
- `files`: parser/writer interfaces plus spreadsheet workbook models and Excel helpers.
- `di`: dependency injection container and scoped resolver.
- `fastapi`: optional app and router scaffolding.
- `logging`: structured logger adapter.
- `auth`, `middleware`, `messaging`, `outbox`, and `redis`: optional pattern
  shapes for common project infrastructure.
- `patterns`: creational, structural, behavioral, and reliability examples.

## Dependency Direction

Core interfaces do not import adapters. Adapters may import interfaces and
reliability primitives. Examples may import anything.

```text
examples -> adapters -> interfaces/reliability -> exceptions
```

## SOLID Defaults

- Single responsibility: one module owns one behavior family.
- Open/closed: add adapters without changing core interfaces.
- Liskov: implementations must honor contract error and return semantics.
- Interface segregation: small protocols beat one large base class.
- Dependency inversion: services depend on interfaces, not concrete clients.

## Adding A New Subsystem

1. Add a small interface if callers need a stable boundary.
2. Add the implementation in an adapter module.
3. Add docs that show the intended use.
4. Add tests for both success and failure behavior.

## Related Guides

- `docs/testing.md`
- `docs/security.md`
- `docs/logging.md`
- `docs/data-structures.md`
- `docs/design-patterns.md`
- `docs/interfaces.md`
- `docs/exceptions.md`
- `docs/test-framework.md`
- `docs/dependency-injection.md`
