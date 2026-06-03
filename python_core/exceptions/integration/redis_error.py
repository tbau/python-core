"""Redis error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class RedisError(PythonCoreError):
    """Raised when Redis operations fail."""
