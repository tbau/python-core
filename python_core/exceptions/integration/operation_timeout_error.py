"""Operation timeout error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class OperationTimeoutError(PythonCoreError):
    """Raised when an operation exceeds its timeout budget."""
