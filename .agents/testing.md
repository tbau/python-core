# Testing Agent

Use this guide when adding or changing tests.

## Checklist

- Add unit tests for interfaces, reliability rules, and edge cases.
- Use fakes instead of real networks, databases, or files when possible.
- Use temporary directories for file and Excel workflows.
- Test retry counts, timeout values, idempotency headers, and transaction
  commit/rollback behavior.
- Keep integration tests explicit and optional when they require extra packages.
- Follow `docs/test-framework.md` when adding test folders, fakes, builders, or
  contract tests.

## Commands

```powershell
python -m pytest
python -m ruff check .
python -m mypy python_core
```
