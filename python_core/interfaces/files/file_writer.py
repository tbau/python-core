"""File writer interface."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, TypeVar

WrittenT = TypeVar("WrittenT")


class FileWriter(Protocol[WrittenT]):
    """Writes a typed value to a file."""

    def write(self, value: WrittenT, path: Path) -> Path:
        """Write a value and return the output path."""
