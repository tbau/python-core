"""Outbox pattern."""

from __future__ import annotations

from python_core.messaging.in_memory_message_bus import InMemoryMessageBus
from python_core.messaging.message import Message
from python_core.outbox.memory_outbox import MemoryOutbox


def dispatch_pending(outbox: MemoryOutbox, bus: InMemoryMessageBus) -> None:
    """Publish pending outbox messages and mark them sent."""
    for item in outbox.pending():
        bus.publish(Message(item.name, item.payload, item.headers))
        outbox.mark_sent(item.id)
