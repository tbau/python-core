"""Dependency error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class DependencyError(PythonCoreError):
    """Raised when a required external dependency fails."""
