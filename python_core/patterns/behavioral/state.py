"""State pattern.

Use this when an object's behavior changes based on its current lifecycle state.
"""

from __future__ import annotations


class OrderState:
    """Simple order state object with transition rules."""

    def __init__(self, name: str = "draft") -> None:
        self.name = name

    def submit(self) -> "OrderState":
        """Move an order from ``draft`` to ``submitted``."""

        if self.name != "draft":
            raise ValueError("only draft orders can be submitted")
        return OrderState("submitted")
