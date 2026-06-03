"""Message queue error."""

from python_core.exceptions.base.python_core_error import PythonCoreError


class MessageQueueError(PythonCoreError):
    """Raised when publishing or consuming messages fails."""
