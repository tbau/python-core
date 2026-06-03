"""Excel profile."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

HeaderNormalizer = Callable[[str], str]
RowFilter = Callable[[dict[str, Any]], bool]


def default_header_normalizer(value: str) -> str:
    """Normalize a spreadsheet header into a Python-friendly key."""
    return value.strip().lower().replace(" ", "_")


@dataclass(frozen=True)
class ExcelProfile:
    """Controls workbook parsing and writing behavior."""

    sheet_name: str
    required_columns: set[str] = field(default_factory=set)
    output_columns: tuple[str, ...] = ()
    header_row: int = 1
    normalize_header: HeaderNormalizer = default_header_normalizer
    row_filter: RowFilter | None = None
