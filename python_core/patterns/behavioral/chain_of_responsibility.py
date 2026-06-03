"""Chain of responsibility pattern.

Use this when a request can be handled by one of several handlers and the caller
should not know which handler will accept it.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

Handler = Callable[[dict[str, object]], bool]


class HandlerChain:
    """Runs handlers until one reports that it handled the request."""

    def __init__(self, handlers: Iterable[Handler]) -> None:
        self._handlers = list(handlers)

    def handle(self, request: dict[str, object]) -> bool:
        """Return ``True`` when any handler accepts the request."""

        return any(handler(request) for handler in self._handlers)
