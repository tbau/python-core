"""Specification pattern.

Use this to package business rules as reusable predicate objects that can be
combined, tested, and passed into repositories or services.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MinimumAmount:
    """Specification that checks whether an amount meets a threshold."""

    amount: int

    def is_satisfied_by(self, value: int) -> bool:
        """Return whether the candidate value satisfies this rule."""

        return value >= self.amount
