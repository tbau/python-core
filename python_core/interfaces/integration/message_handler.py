"""Message handler interface."""

from __future__ import annotations

from typing import Protocol

from python_core.messaging.message import Message


class MessageHandler(Protocol):
    """Handles one message from a queue or bus."""

    def handle(self, message: Message) -> None:
        """Process a message."""
