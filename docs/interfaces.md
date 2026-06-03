# Interfaces Guide

## Layout

Interfaces are grouped by responsibility:

- `interfaces/application`: services and facades.
- `interfaces/auth`: authentication, authorization, ownership, password hashing,
  and token services.
- `interfaces/data`: repositories, queries, caches, and serializers.
- `interfaces/database`: connector and transaction boundaries.
- `interfaces/files`: parsers, writers, and spreadsheet writers.
- `interfaces/integration`: external APIs, Redis, queues, and outbox.
- `interfaces/middleware`: request context processing.
- `interfaces/observability`: logging and exception reporting.

## Rule

Use grouped imports in new code:

```python
from python_core.interfaces.data.repository import Repository
from python_core.interfaces.application.facade import Facade
```
