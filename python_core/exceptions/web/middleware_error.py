"""Middleware error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class MiddlewareError(PythonCoreError):
    """Raised when middleware cannot process a request."""
