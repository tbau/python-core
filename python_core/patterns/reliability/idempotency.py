"""Idempotency pattern."""

from __future__ import annotations

from python_core.reliability.idempotency_checker import IdempotencyChecker
from python_core.reliability.idempotency_key import IdempotencyKey


def should_execute(checker: IdempotencyChecker, key: IdempotencyKey) -> bool:
    """Return True only for the first use of a key."""
    return checker.check_and_add(key)
