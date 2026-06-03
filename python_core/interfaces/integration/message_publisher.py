"""Message publisher interface."""

from __future__ import annotations

from typing import Protocol

from python_core.messaging.message import Message


class MessagePublisher(Protocol):
    """Publishes messages to a bus, queue, or broker."""

    def publish(self, message: Message) -> None:
        """Publish one message."""
