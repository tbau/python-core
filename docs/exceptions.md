# Exceptions Guide

## Layout

Exceptions are grouped by failure domain:

- `exceptions/common`: validation, configuration, not found, and conflict.
- `exceptions/security`: authentication and authorization.
- `exceptions/integration`: APIs, queues, Redis, rate limits, timeouts, and dependencies.
- `exceptions/persistence`: transactions, repositories, queries, and outbox.
- `exceptions/reliability`: retry and idempotency failures.
- `exceptions/web`: middleware and web boundary failures.

## Import Style

Application code may use the grouped path or the root export:

```python
from python_core.exceptions import ValidationError
from python_core.exceptions.persistence.transaction_error import TransactionError
```
