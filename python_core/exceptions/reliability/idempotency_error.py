"""Idempotency error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class IdempotencyError(PythonCoreError):
    """Raised when an idempotency key has already been used."""
