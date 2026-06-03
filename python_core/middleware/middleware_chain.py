"""Middleware chain."""

from __future__ import annotations

from collections.abc import Iterable

from python_core.interfaces.middleware.middleware import Middleware
from python_core.middleware.middleware_context import MiddlewareContext


class MiddlewareChain:
    """Runs middleware in order."""

    def __init__(self, middleware: Iterable[Middleware]) -> None:
        self._middleware = list(middleware)

    def handle(self, context: MiddlewareContext) -> MiddlewareContext:
        """Run each middleware and return the final context."""
        for item in self._middleware:
            context = item.handle(context)
        return context
