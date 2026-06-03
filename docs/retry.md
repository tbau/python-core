# Retry And Backoff Guide

## RetryPolicy Interface

`RetryPolicy` is the interface used by `retry_sync` and `retry_async`.
Concrete policy classes decide how many attempts are allowed and how delays are
calculated.

## Implementations

- `NoRetryPolicy`: one attempt, no retry.
- `FixedRetryPolicy`: same delay between attempts.
- `LinearBackoffRetryPolicy`: delay grows by a fixed step.
- `ExponentialBackoffRetryPolicy`: exponential backoff with optional jitter.

## Exponential Backoff

- `attempts`: maximum attempts
- `base_delay`: first delay
- `backoff`: multiplier per retry
- `max_delay`: upper delay bound
- `jitter`: random extra delay to avoid synchronized retries

## Rule

Retry reads freely when appropriate. Retry writes only when the operation is
idempotent or an idempotency key is present.
