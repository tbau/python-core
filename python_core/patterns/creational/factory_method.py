"""Factory method pattern.

Use this when creation logic should choose a concrete implementation while
callers depend only on a product interface.
"""

from __future__ import annotations

from typing import Protocol


class Parser(Protocol):
    """Product interface shared by all parser implementations."""

    def parse(self, text: str) -> dict[str, str]:
        """Parse text."""


class CsvParser:
    """Concrete parser product for a tiny ``key,value`` CSV shape."""

    def parse(self, text: str) -> dict[str, str]:
        """Parse ``key,value`` text into a dictionary."""

        key, value = text.split(",", maxsplit=1)
        return {key: value}


def create_parser(kind: str) -> Parser:
    """Create a parser implementation from a simple kind string."""

    if kind == "csv":
        return CsvParser()
    raise ValueError(f"unknown parser kind: {kind}")
