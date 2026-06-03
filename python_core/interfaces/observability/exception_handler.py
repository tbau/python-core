"""Exception handler interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

ResponseT = TypeVar("ResponseT")


class ExceptionHandler(Protocol[ResponseT]):
    """Maps exceptions to caller-specific responses."""

    def can_handle(self, exc: BaseException) -> bool:
        """Return True when this handler can handle the exception."""

    def handle(self, exc: BaseException) -> ResponseT:
        """Convert the exception into a response."""
