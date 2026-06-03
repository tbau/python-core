"""Spreadsheet workbook model."""

from __future__ import annotations

from dataclasses import dataclass

from python_core.files.spreadsheet_sheet import SpreadsheetSheet
from python_core.files.spreadsheet_style import SpreadsheetStyle


@dataclass(frozen=True)
class SpreadsheetWorkbook:
    """Workbook definition for spreadsheet writing."""

    sheets: tuple[SpreadsheetSheet, ...]
    styles: dict[str, SpreadsheetStyle] | None = None
    active_sheet: str | None = None
