# Testing Guide

## Test Pyramid

- Unit tests for interfaces, retry logic, idempotency, parsers, and transaction
  behavior.
- Adapter tests with fakes for external API clients and database sessions.
- Optional integration tests for real FastAPI, SQLAlchemy, Redis, queues, and
  Excel packages.

See `docs/test-framework.md` for the folder layout and fake/builder/contract
test conventions.

## What To Test

- Retries stop after the configured attempt count.
- Retry delay calculation is bounded.
- Timeout settings are passed to external clients.
- Idempotency checkers generate keys, add unseen keys, and detect duplicates.
- Transactions commit on success and roll back on failure.
- Excel profiles reject missing sheets or columns.
- Outbox dispatch marks messages as sent after publishing.
- Repositories and query handlers return predictable results for common filters.

## Commands

```powershell
python -m pytest
python -m ruff check .
python -m mypy python_core
```
