"""Idempotency required error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class IdempotencyRequiredError(PythonCoreError):
    """Raised when a retryable write is missing an idempotency key."""
