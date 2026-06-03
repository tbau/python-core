"""Spreadsheet writer interface."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from python_core.files.spreadsheet_workbook import SpreadsheetWorkbook


class SpreadsheetWriter(Protocol):
    """Writes a workbook model to a spreadsheet file."""

    def write(self, workbook: "SpreadsheetWorkbook", path: Path) -> Path:
        """Write a workbook and return the output path."""
