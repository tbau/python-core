"""File parser interface."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, TypeVar

ParsedT = TypeVar("ParsedT")


class FileParser(Protocol[ParsedT]):
    """Parses a file into a typed value."""

    def parse(self, path: Path) -> ParsedT:
        """Read and parse a file."""
