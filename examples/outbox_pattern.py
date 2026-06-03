"""Outbox pattern example."""

from python_core.messaging.in_memory_message_bus import InMemoryMessageBus
from python_core.messaging.message import Message
from python_core.outbox.memory_outbox import MemoryOutbox
from python_core.outbox.outbox_message import OutboxMessage


def dispatch_outbox(outbox: MemoryOutbox, bus: InMemoryMessageBus) -> None:
    """Publish pending outbox messages and mark them sent."""
    for item in outbox.pending():
        bus.publish(Message(name=item.name, payload=item.payload, headers=item.headers))
        outbox.mark_sent(item.id)


def main() -> None:
    """Queue an event and dispatch it through the local bus."""
    delivered: list[str] = []
    bus = InMemoryMessageBus()
    bus.subscribe("invoice.created", lambda message: delivered.append(message.payload["invoice_id"]))

    outbox = MemoryOutbox()
    outbox.add(OutboxMessage(name="invoice.created", payload={"invoice_id": "inv_123"}))
    dispatch_outbox(outbox, bus)

    print(f"delivered={delivered}; pending={len(outbox.pending())}")


if __name__ == "__main__":
    main()
