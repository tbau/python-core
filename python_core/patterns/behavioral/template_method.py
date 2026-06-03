"""Template method pattern.

Use this when a base class owns the workflow order and subclasses customize one
or more steps.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ImportTemplate(ABC):
    """Defines import steps while subclasses customize parsing."""

    def run(self, text: str) -> list[dict[str, str]]:
        """Run the fixed import workflow before delegating parsing."""

        cleaned = text.strip()
        return self.parse(cleaned)

    @abstractmethod
    def parse(self, text: str) -> list[dict[str, str]]:
        """Parse cleaned text in a subclass-specific way."""
