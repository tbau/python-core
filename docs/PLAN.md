# Python Core Library Plan

## Goal

Build a personal Python foundation that can be reused across APIs, automation,
data workflows, integrations, and internal tools.

## Priorities

- Interfaces first: stable boundaries for databases, file parsers, loggers,
  external APIs, and structured data.
- Optional adapters: FastAPI, SQLAlchemy, pandas, and openpyxl stay
  isolated so the base package remains lightweight.
- Reliability by default: explicit timeout, retry, idempotency, transaction, and
  logging behavior.
- Project-template value: examples for Redis, queues, middleware, auth, queries,
  repositories, facades, outbox, and testing structure.
- Auth foundation: JWT, OAuth helpers, role/permission checks, and ownership
  policy examples.
- Dependency management: a small DI container for examples and downstream
  service wiring.
- Spreadsheet workflows: workbook models and customizable Excel writer adapters.
- Human readability: small files, plain names, and predictable folders.

## Initial Milestones

1. Establish package, docs, agents, tests, and development tooling.
2. Add core interfaces and reliability primitives.
3. Add optional adapters for external APIs, SQLAlchemy, FastAPI, and Excel.
4. Grow examples from real downstream use cases.
5. Harden with tests, type checking, and security review.
6. Add deeper guides for logging, data structures, migrations, packaging, and
   observability as real use cases appear.
7. Add optional real adapters only after the interface and in-memory example are
   clear.

## Non-Goals For The First Pass

- No app-specific business models.
- No global service locator.
- No required database, web framework, or spreadsheet dependency.
- No hidden background retries or implicit transactions.
