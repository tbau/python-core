"""Service interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class Service(Protocol[RequestT, ResponseT]):
    """Use-case boundary for application behavior."""

    async def execute(self, request: RequestT) -> ResponseT:
        """Execute a use case."""
