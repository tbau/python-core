"""Fake message bus template for downstream tests."""

from python_core.messaging.message import Message


class FakeMessageBus:
    """Captures messages for assertions."""

    def __init__(self) -> None:
        self.messages: list[Message] = []

    def publish(self, message: Message) -> None:
        self.messages.append(message)
