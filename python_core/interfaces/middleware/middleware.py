"""Middleware interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from python_core.middleware.middleware_context import MiddlewareContext


class Middleware(Protocol):
    """Processes context before and after a handler."""

    def handle(self, context: "MiddlewareContext") -> "MiddlewareContext":
        """Return the processed context."""
