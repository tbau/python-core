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
