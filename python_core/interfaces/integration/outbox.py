"""Outbox interface."""

from __future__ import annotations

from typing import Protocol

from python_core.outbox.outbox_message import OutboxMessage


class Outbox(Protocol):
    """Stores messages that should be published after a transaction."""

    def add(self, message: OutboxMessage) -> None:
        """Store a message."""

    def pending(self) -> list[OutboxMessage]:
        """Return messages that have not been dispatched."""

    def mark_sent(self, message_id: str) -> None:
        """Mark a message as dispatched."""
