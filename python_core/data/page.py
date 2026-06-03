"""Page data structure."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Generic, TypeVar

EntityT = TypeVar("EntityT")


class Page(Generic[EntityT]):
    """Simple pagination result for list endpoints and repositories."""

    def __init__(self, items: Iterable[EntityT], *, total: int, limit: int, offset: int) -> None:
        if total < 0:
            raise ValueError("total cannot be negative")
        if limit <= 0:
            raise ValueError("limit must be positive")
        if offset < 0:
            raise ValueError("offset cannot be negative")
        self.items = list(items)
        self.total = total
        self.limit = limit
        self.offset = offset

    @property
    def has_more(self) -> bool:
        """Return True when another page is available."""
        return self.offset + len(self.items) < self.total
