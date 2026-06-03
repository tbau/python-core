"""External API error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class ExternalApiError(PythonCoreError):
    """Raised when an external API request fails."""
