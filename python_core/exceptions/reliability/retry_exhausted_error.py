"""Retry exhaustion error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class RetryExhaustedError(PythonCoreError):
    """Raised when retry attempts are exhausted."""
