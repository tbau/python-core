"""Spreadsheet style model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpreadsheetStyle:
    """Basic spreadsheet cell style."""

    bold: bool = False
    font_color: str | None = None
    fill_color: str | None = None
    number_format: str | None = None
