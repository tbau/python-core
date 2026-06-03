"""Not found error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class NotFoundError(PythonCoreError):
    """Raised when a requested resource does not exist."""
