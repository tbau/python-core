"""In-memory outbox."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from python_core.exceptions import OutboxError
from python_core.outbox.outbox_message import OutboxMessage


class MemoryOutbox:
    """Small outbox implementation for examples and tests."""

    def __init__(self) -> None:
        self._messages: dict[str, OutboxMessage] = {}

    def add(self, message: OutboxMessage) -> None:
        """Store a message."""
        self._messages[message.id] = message

    def pending(self) -> list[OutboxMessage]:
        """Return unsent messages."""
        return [message for message in self._messages.values() if message.sent_at is None]

    def mark_sent(self, message_id: str) -> None:
        """Mark a message as sent."""
        try:
            message = self._messages[message_id]
        except KeyError as exc:
            raise OutboxError(f"outbox message not found: {message_id}") from exc
        self._messages[message_id] = replace(message, sent_at=datetime.now(UTC))
