"""Visitor pattern.

Use this to add operations to value objects without putting every operation on
the value object itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Visitor(Protocol):
    """Interface for operations that can visit supported value objects."""

    def visit_total(self, total: "Total") -> str:
        """Process a ``Total`` value."""


@dataclass(frozen=True)
class Total:
    """Value object that lets a visitor decide how to process it."""

    cents: int

    def accept(self, visitor: Visitor) -> str:
        """Dispatch this object to the matching visitor method."""

        return visitor.visit_total(self)
