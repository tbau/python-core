"""Abstract factory pattern.

Use this when a caller needs families of related objects but should not know the
concrete classes used to create them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Button:
    """Example product representing a clickable UI button."""

    label: str


@dataclass(frozen=True)
class TextInput:
    """Example product representing a text input field."""

    name: str


class FormFactory(Protocol):
    """Factory interface for a related family of form controls."""

    def button(self, label: str) -> Button:
        """Create a button."""

    def text_input(self, name: str) -> TextInput:
        """Create a text input."""


class SimpleFormFactory:
    """Concrete factory that creates the simple form control family."""

    def button(self, label: str) -> Button:
        """Create a simple button product."""

        return Button(label)

    def text_input(self, name: str) -> TextInput:
        """Create a simple text input product."""

        return TextInput(name)
