"""Transaction error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class TransactionError(PythonCoreError):
    """Raised when a transaction cannot be completed."""
