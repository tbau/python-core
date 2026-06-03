"""Authorization error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class AuthorizationError(PythonCoreError):
    """Raised when a caller is not allowed to perform an action."""
