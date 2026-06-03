"""Query handler interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

QueryT = TypeVar("QueryT")
ResultT = TypeVar("ResultT")


class QueryHandler(Protocol[QueryT, ResultT]):
    """Handles a read-only query."""

    def handle(self, query: QueryT) -> ResultT:
        """Return query results."""
