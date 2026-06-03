"""Retry with backoff pattern."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy
from python_core.reliability.retry import retry_sync

T = TypeVar("T")


def run_with_backoff(operation: Callable[[], T]) -> T:
    """Run an operation with exponential backoff and jitter."""
    return retry_sync(operation, policy=ExponentialBackoffRetryPolicy(attempts=3, jitter=0.1))
