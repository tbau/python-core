"""Spreadsheet column model."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

ValueFormatter = Callable[[Any], Any]


@dataclass(frozen=True)
class SpreadsheetColumn:
    """Column definition for spreadsheet writing."""

    key: str
    header: str | None = None
    width: float | None = None
    style_key: str | None = None
    formatter: ValueFormatter | None = None

    @property
    def label(self) -> str:
        """Return the visible header label."""
        return self.header or self.key

    def value_for(self, row: dict[str, Any]) -> Any:
        """Return formatted row value."""
        value = row.get(self.key)
        if self.formatter is None:
            return value
        return self.formatter(value)
