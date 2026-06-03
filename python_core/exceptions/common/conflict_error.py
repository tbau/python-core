"""Conflict error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class ConflictError(PythonCoreError):
    """Raised when a requested change conflicts with current state."""
