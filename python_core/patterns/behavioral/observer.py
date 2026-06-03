"""Observer pattern.

Use this when many listeners need to react to a subject's events without the
subject knowing listener details.
"""

from __future__ import annotations

from collections.abc import Callable

Observer = Callable[[str], None]


class Subject:
    """Stores observers and notifies them about string events."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Add an observer callback."""

        self._observers.append(observer)

    def notify(self, event: str) -> None:
        """Send an event to all attached observers."""

        for observer in self._observers:
            observer(event)
