"""Bridge pattern.

Use this to separate an abstraction from its implementation so either side can
change independently.
"""

from __future__ import annotations

from typing import Protocol


class Sender(Protocol):
    """Implementation side of the bridge for message delivery."""

    def send(self, body: str) -> None:
        """Send a message."""


class Notification:
    """Notification abstraction decoupled from sender implementation."""

    def __init__(self, sender: Sender) -> None:
        self._sender = sender

    def notify(self, body: str) -> None:
        """Send a notification through the configured sender."""

        self._sender.send(body)
