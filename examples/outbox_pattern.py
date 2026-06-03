"""Outbox pattern example."""

from python_core.messaging.in_memory_message_bus import InMemoryMessageBus
from python_core.messaging.message import Message
from python_core.outbox.memory_outbox import MemoryOutbox
from python_core.outbox.outbox_message import OutboxMessage


def dispatch_outbox(outbox: MemoryOutbox, bus: InMemoryMessageBus) -> None:
    for item in outbox.pending():
        bus.publish(Message(name=item.name, payload=item.payload, headers=item.headers))
        outbox.mark_sent(item.id)


outbox = MemoryOutbox()
outbox.add(OutboxMessage(name="invoice.created", payload={"invoice_id": "inv_123"}))
dispatch_outbox(outbox, InMemoryMessageBus())
