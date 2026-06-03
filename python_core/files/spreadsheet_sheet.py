"""Spreadsheet sheet model."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from python_core.files.spreadsheet_column import SpreadsheetColumn
from python_core.files.spreadsheet_style import SpreadsheetStyle


@dataclass(frozen=True)
class SpreadsheetSheet:
    """Sheet definition for spreadsheet writing."""

    name: str
    rows: Iterable[Mapping[str, Any]]
    columns: tuple[SpreadsheetColumn, ...] = ()
    header_style: SpreadsheetStyle = field(default_factory=lambda: SpreadsheetStyle(bold=True))
    freeze_panes: str | None = "A2"
    auto_filter: bool = True
    tab_color: str | None = None

    def materialized_rows(self) -> list[dict[str, Any]]:
        """Return rows as mutable dictionaries."""
        return [dict(row) for row in self.rows]

    def resolved_columns(self, rows: list[dict[str, Any]]) -> list[SpreadsheetColumn]:
        """Return explicit columns or infer them from rows."""
        if self.columns:
            return list(self.columns)

        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        return [SpreadsheetColumn(key=key) for key in keys]
