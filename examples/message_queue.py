"""Message queue/bus example."""

from python_core.messaging.in_memory_message_bus import InMemoryMessageBus
from python_core.messaging.message import Message


def send_welcome_email(message: Message) -> None:
    email = message.payload["email"]
    print(f"send welcome email to {email}")


bus = InMemoryMessageBus()
bus.subscribe("user.registered", send_welcome_email)
bus.publish(Message(name="user.registered", payload={"email": "person@example.com"}))
