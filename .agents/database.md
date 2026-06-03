# Database Agent

Use this guide when adding database connectors, repositories, or transactions.

## Checklist

- Depend on `DatabaseConnector` or `Transaction` interfaces.
- Keep SQLAlchemy-specific code inside class-named `python_core.db` modules.
- Use transactions for multi-step writes.
- Keep query and fetch methods on `Transaction` or repositories, not
  `DatabaseConnector`.
- Keep repository methods small and named by intent.
- Test commit, rollback, close, and exception paths.

## Transaction Pattern

```python
async with connector.open_transaction() as tx:
    await repository.save(entity, tx=tx)
    await tx.commit()
```

The context manager closes the transaction. Call `await tx.close()` only when a
transaction is managed directly outside the connector context.
