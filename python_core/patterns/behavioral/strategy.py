"""Strategy pattern.

Use this when a caller should choose among interchangeable algorithms without
hard-coding conditional branches into the caller.
"""

from __future__ import annotations

from typing import Protocol


class PricingStrategy(Protocol):
    """Interface for any price calculation algorithm."""

    def price(self, cents: int) -> int:
        """Return adjusted price."""


class PercentDiscount:
    """Strategy that subtracts a percentage from a price in cents."""

    def __init__(self, percent: int) -> None:
        self.percent = percent

    def price(self, cents: int) -> int:
        """Return price after applying the percentage discount."""

        return cents - (cents * self.percent // 100)
