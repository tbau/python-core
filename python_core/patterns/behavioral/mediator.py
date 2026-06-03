"""Mediator pattern.

Use this to route messages between components without making those components
reference each other directly.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

Handler = Callable[[object], None]


class Mediator:
    """Simple in-memory mediator keyed by message name."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)

    def register(self, name: str, handler: Handler) -> None:
        """Register a handler for a message name."""

        self._handlers[name].append(handler)

    def publish(self, name: str, payload: object) -> None:
        """Publish payload to every handler registered for the message name."""

        for handler in self._handlers[name]:
            handler(payload)
