"""Facade interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class Facade(Protocol[RequestT, ResponseT]):
    """Coarse-grained API over one or more services."""

    def handle(self, request: RequestT) -> ResponseT:
        """Handle a high-level request."""
