# python-core

Core Python helper library for reusable application building blocks.

This repo is intended to become a personal foundation for Python projects:
interfaces first, optional framework adapters second, and small readable files
that are easy to change.

## What Is Included

- Reliability primitives for retry policy interfaces, retry strategies,
  timeouts, and idempotency.
- External API client scaffolding built on the Python standard library, with an
  optional `requests` transport.
- Database interfaces plus SQLAlchemy connector and transaction adapters.
- File parser/writer interfaces and customizable spreadsheet workbook writers.
- Class-named modules under `python_core/interfaces`, `python_core/db`,
  `python_core/external_api`, `python_core/files`, and `python_core/reliability`.
- Dependency injection container with singleton, transient, and scoped lifetimes.
- FastAPI app and router scaffolding for adding routes consistently.
- Authentication, middleware, Redis, messaging, outbox, query, repository, and
  facade patterns.
- Helper modules for dates/timezones, geo distance, math, statistics,
  similarity, physics, chemistry, electrical, finance, and unit conversion.
- Utility modules for collections, strings, paths, validation, security tokens,
  HMACs, redaction, and optional Fernet encryption.
- Test framework guidance for fakes, builders, contract tests, unit tests, and
  integration tests.
- Agent and Markdown planning docs for architecture, testing, security, DB,
  routes, external APIs, Excel workflows, and extension work.

## Layout

```text
python_core/interfaces/    grouped interface modules by responsibility
python_core/exceptions/    grouped exception modules by failure domain
python_core/reliability/   retries, timeouts, idempotency
python_core/external_api/  external API models and simple API client
python_core/db/            database interfaces and SQLAlchemy adapter package
python_core/files/         file, spreadsheet, and Excel adapters
python_core/di/            dependency injection container
python_core/auth/          identity, permission, JWT, OAuth, ownership, password hashing
python_core/messaging/     message envelope and in-memory bus
python_core/middleware/    middleware context and chain
python_core/outbox/        outbox message and memory implementation
python_core/patterns/      creational, structural, behavioral, reliability patterns
python_core/helpers/       domain calculations and conversion helpers
python_core/utils/         cross-cutting collection, string, path, and security utilities
python_core/redis/         Redis adapter shapes
docs/                      implementation guides
.agents/                   focused task instructions for coding agents
examples/                  small examples showing intended usage
tests/                     starter test suite
```

## Install For Development

For a fully pinned environment that installs every optional adapter and tool in
this repo:

```powershell
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
python -m pytest
```

For a lighter editable install that lets pip resolve current compatible
versions:

```powershell
python -m pip install -e ".[dev,api,db,excel]"
python -m pytest
```

Install only the extras you need in downstream projects:

```powershell
python -m pip install -e ".[api]"
python -m pip install -e ".[auth]"
python -m pip install -e ".[db]"
python -m pip install -e ".[excel]"
python -m pip install -e ".[redis]"
python -m pip install -e ".[requests]"
python -m pip install -e ".[security]"
```

## Design Rules

- Keep files near or below 300 lines.
- Prefer interfaces, protocols, and dependency injection over hard coupling.
- Keep framework-specific code behind optional adapters.
- Make failure behavior explicit: timeouts, retries, idempotency, transactions,
  validation, logging, and security checks should be visible in the API.
- Favor boring, testable code over clever abstractions.

See [docs/PLAN.md](docs/PLAN.md) and [AGENTS.md](AGENTS.md) for the working
plan and agent guidance.

Useful pattern guides:

- [docs/design-patterns.md](docs/design-patterns.md)
- [docs/interfaces.md](docs/interfaces.md)
- [docs/exceptions.md](docs/exceptions.md)
- [docs/test-framework.md](docs/test-framework.md)
- [docs/messaging.md](docs/messaging.md)
- [docs/authentication.md](docs/authentication.md)
- [docs/repositories.md](docs/repositories.md)
- [docs/middleware.md](docs/middleware.md)
- [docs/redis.md](docs/redis.md)
- [docs/retry.md](docs/retry.md)
- [docs/dependency-injection.md](docs/dependency-injection.md)
- [docs/helpers-and-utils.md](docs/helpers-and-utils.md)
