"""Excel writer."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from python_core.exceptions import ConfigurationError
from python_core.files.excel_profile import ExcelProfile


class ExcelWriter:
    """Write dictionaries to an Excel workbook."""

    def __init__(self, profile: ExcelProfile) -> None:
        self.profile = profile

    def write(self, value: Iterable[Mapping[str, Any]], path: Path) -> Path:
        """Write rows to an Excel workbook."""
        openpyxl = self._openpyxl()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = self.profile.sheet_name

        rows = list(value)
        headers = self._ordered_headers(rows)
        sheet.append(headers)
        for row in rows:
            sheet.append([row.get(header) for header in headers])

        workbook.save(path)
        return path

    def _ordered_headers(self, rows: list[Mapping[str, Any]]) -> list[str]:
        if self.profile.output_columns:
            return list(self.profile.output_columns)
        if self.profile.required_columns:
            return sorted(self.profile.required_columns)

        headers: list[str] = []
        for row in rows:
            for key in row:
                if key not in headers:
                    headers.append(key)
        return headers

    def _openpyxl(self) -> Any:
        try:
            import openpyxl
        except ImportError as exc:
            raise ConfigurationError("Install python-core[excel] to write Excel files") from exc
        return openpyxl
