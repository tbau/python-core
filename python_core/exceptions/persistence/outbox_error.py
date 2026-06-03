"""Outbox error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class OutboxError(PythonCoreError):
    """Raised when an outbox message cannot be stored or dispatched."""
