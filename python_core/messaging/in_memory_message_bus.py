"""In-memory message bus."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field

from python_core.messaging.message import Message

Handler = Callable[[Message], None]


@dataclass
class InMemoryMessageBus:
    """Simple message bus for examples and tests."""

    handlers: dict[str, list[Handler]] = field(default_factory=lambda: defaultdict(list))

    def subscribe(self, message_name: str, handler: Handler) -> None:
        """Subscribe a handler to a message name."""
        self.handlers[message_name].append(handler)

    def publish(self, message: Message) -> None:
        """Publish a message to local subscribers."""
        for handler in self.handlers.get(message.name, []):
            handler(message)
