"""Query specification."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class QuerySpec:
    """Common filtering, sorting, and pagination shape."""

    filters: dict[str, object] = field(default_factory=dict)
    sort_by: tuple[str, ...] = ()
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if self.limit <= 0:
            raise ValueError("limit must be positive")
        if self.offset < 0:
            raise ValueError("offset cannot be negative")
