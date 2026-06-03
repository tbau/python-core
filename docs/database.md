# Database Guide

## Interfaces

Use database interfaces to keep application services independent from a specific
driver or ORM:

- `DatabaseConnector`
- `Transaction`
- `UnitOfWork`
- `Repository`

## SQLAlchemy

`python_core.db.sqlalchemy` contains SQLAlchemy adapters. `SQLAlchemyUnitOfWork`
wraps a SQLAlchemy async session factory, and `SQLAlchemyDatabaseConnector`
provides connector-level execute/fetch helpers.

## Transaction Rules

- Open transactions close to the use case.
- Commit only after all write steps succeed.
- Roll back on exceptions.
- Keep raw SQL or ORM details inside repositories.
- Use `UnitOfWork` as the request/use-case transaction boundary.
- Use `DatabaseConnector.begin()` for lower-level transaction contexts.

## Query Pattern

```python
async with unit_of_work as work:
    result = await repository.get_by_id("abc", tx=work.transaction)
```
