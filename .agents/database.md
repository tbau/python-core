# Database Agent

Use this guide when adding database connectors, repositories, or transactions.

## Checklist

- Depend on `DatabaseConnector`, `Transaction`, or `UnitOfWork` interfaces.
- Keep SQLAlchemy-specific code inside class-named `python_core.db` modules.
- Use transactions for multi-step writes.
- Keep repository methods small and named by intent.
- Test commit, rollback, and exception paths.

## Transaction Pattern

```python
async with unit_of_work as work:
    await repository.save(entity, tx=work.transaction)
```
