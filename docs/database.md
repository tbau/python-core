# Database Guide

## Interfaces

Use database interfaces to keep application services independent from a specific
driver or ORM:

- `DatabaseConnector`
- `Transaction`
- `Repository`

## SQLAlchemy

`python_core.db.sqlalchemy` contains SQLAlchemy adapters.
`SQLAlchemyDatabaseConnector` owns database health checks and transaction
creation.

## Transaction Rules

- Open transactions close to the use case.
- Commit explicitly after all write steps succeed.
- Roll back on exceptions.
- Close a manually managed transaction with `await tx.close()`.
- Dispose connector-owned engine resources with `await connector.close()`.
- Keep raw SQL or ORM details inside repositories.
- Use `DatabaseConnector.open_transaction()` for transaction contexts.
- Keep query and fetch calls on `Transaction` or repositories, not on the
  connector.

## Query Pattern

```python
async with connector.open_transaction() as tx:
    result = await repository.get_by_id("abc", tx=tx)
```

```python
async with connector.open_transaction() as tx:
    await repository.save(entity, tx=tx)
    await tx.commit()
```

The context manager closes the transaction for you. If you manage a transaction
directly inside a custom adapter or test, close it explicitly:

```python
tx = SQLAlchemyTransaction(session)
try:
    await repository.save(entity, tx=tx)
    await tx.commit()
finally:
    await tx.close()
```
