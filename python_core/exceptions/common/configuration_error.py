"""Configuration error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class ConfigurationError(PythonCoreError):
    """Raised when required configuration is missing or invalid."""
