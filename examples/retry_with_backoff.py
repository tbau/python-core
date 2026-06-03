"""Retry with exponential backoff and jitter."""

from python_core.reliability.retry import retry_sync
from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy


def call_dependency() -> str:
    return "ok"


result = retry_sync(
    call_dependency,
    policy=ExponentialBackoffRetryPolicy(
        attempts=4,
        base_delay=0.2,
        backoff=2.0,
        max_delay=3.0,
        jitter=0.1,
    ),
)
