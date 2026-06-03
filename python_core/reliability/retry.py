"""Retry execution helpers."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import TypeVar

from python_core.exceptions import RetryExhaustedError
from python_core.reliability.retry_policy import RetryPolicy

T = TypeVar("T")


def retry_sync(
    operation: Callable[[], T],
    *,
    policy: RetryPolicy,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    sleeper: Callable[[float], None] = time.sleep,
) -> T:
    """Run a sync operation with bounded retries."""

    last_error: BaseException | None = None
    for attempt in range(policy.attempts):
        try:
            return operation()
        except retry_on as exc:
            if policy.attempts == 1:
                raise
            last_error = exc
            if attempt == policy.attempts - 1:
                break
            sleeper(policy.delay_for_attempt(attempt))
    raise RetryExhaustedError("retry attempts exhausted") from last_error


async def retry_async(
    operation: Callable[[], Awaitable[T]],
    *,
    policy: RetryPolicy,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    sleeper: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> T:
    """Run an async operation with bounded retries."""

    last_error: BaseException | None = None
    for attempt in range(policy.attempts):
        try:
            return await operation()
        except retry_on as exc:
            if policy.attempts == 1:
                raise
            last_error = exc
            if attempt == policy.attempts - 1:
                break
            await sleeper(policy.delay_for_attempt(attempt))
    raise RetryExhaustedError("retry attempts exhausted") from last_error
