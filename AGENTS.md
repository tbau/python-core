# Agent Guide

Use this repo as a reusable Python core library, not as a one-off app.

## Operating Principles

- Read existing docs and interfaces before adding new abstractions.
- Keep each file around 300 lines or less.
- Prefer small interfaces, protocols, and dependency injection.
- Keep FastAPI, SQLAlchemy, Redis, pandas, and openpyxl code in optional
  adapter modules.
- Make runtime behavior explicit: timeout, retry, idempotency, transaction,
  validation, logging, and security choices should be visible at call sites.
- Avoid broad refactors unless the requested change needs them.

## Where To Start

- Common tasks: `.agents/common.md`
- Uncommon tasks: `.agents/uncommon.md`
- Architecture: `.agents/architecture.md`
- Tests: `.agents/testing.md`
- Security: `.agents/security.md`
- FastAPI routes: `.agents/fastapi-routes.md`
- Database work: `.agents/database.md`
- External APIs: `.agents/external-apis.md`
- Excel parsing/writing: `.agents/excel.md`
- Design patterns: `.agents/patterns.md`
- Refactors and cleanup: `.agents/refactor.md`

## Code Style

- Use type hints on public functions and methods.
- Favor `Protocol` for structural interfaces and `ABC` where shared behavior is
  useful.
- Put each public interface or adapter class in a class-named module.
- Raise domain-specific exceptions from `python_core.exceptions`.
- Do not import optional dependencies from top-level package modules.
- Add focused tests for new behavior.
- Prefer examples and docs when this repo is acting as a project template.
