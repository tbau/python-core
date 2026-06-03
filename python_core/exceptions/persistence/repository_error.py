"""Repository error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class RepositoryError(PythonCoreError):
    """Raised when repository persistence fails."""
