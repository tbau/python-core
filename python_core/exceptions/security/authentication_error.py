"""Authentication error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class AuthenticationError(PythonCoreError):
    """Raised when a caller cannot be authenticated."""
