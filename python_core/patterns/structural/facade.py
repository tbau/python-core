"""Facade pattern.

Use this to provide one coarse, intention-revealing API over several lower-level
operations.
"""

from __future__ import annotations


class BillingFacade:
    """Coarse API over lower-level billing steps."""

    def create_invoice(self, customer_id: str, amount: int) -> dict[str, object]:
        """Create an invoice without exposing lower-level billing details."""

        return {"customer_id": customer_id, "amount": amount, "status": "created"}
