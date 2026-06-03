# Retry Policies Guide

## Structure

`RetryPolicy` is the interface. Concrete policy classes live in class-named
modules under `python_core/reliability`.

## Included Policies

- `NoRetryPolicy`
- `FixedRetryPolicy`
- `LinearBackoffRetryPolicy`
- `ExponentialBackoffRetryPolicy`

## Example

```python
from python_core.reliability.exponential_backoff_retry_policy import (
    ExponentialBackoffRetryPolicy,
)
from python_core.reliability.retry import retry_sync

result = retry_sync(
    call_dependency,
    policy=ExponentialBackoffRetryPolicy(attempts=3, jitter=0.1),
)
```
