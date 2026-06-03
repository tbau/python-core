"""Rate limit error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class RateLimitError(PythonCoreError):
    """Raised when a dependency or API rate limit is reached."""
