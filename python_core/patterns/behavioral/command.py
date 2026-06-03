"""Command pattern.

Use this to represent work as an object so it can be queued, retried, logged,
undone, or passed around without immediately executing it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Command(Protocol):
    """Interface for an object that performs one action."""

    def execute(self) -> None:
        """Execute command."""


@dataclass(frozen=True)
class PrintCommand:
    """Example command that prints a message when executed."""

    message: str

    def execute(self) -> None:
        """Run the command's action."""

        print(self.message)
