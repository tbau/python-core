"""String utility functions for user input, identifiers, and display text."""

from __future__ import annotations

import re
import unicodedata


def is_blank(value: str | None) -> bool:
    """Return whether a string is ``None`` or only whitespace."""

    return value is None or value.strip() == ""


def coalesce_blank(value: str | None, default: str) -> str:
    """Return ``default`` when value is blank, otherwise return stripped text."""

    return default if is_blank(value) else value.strip()


def normalize_whitespace(value: str) -> str:
    """Collapse repeated whitespace into single spaces."""

    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str, *, separator: str = "-") -> str:
    """Return a URL-friendly ASCII slug.

    Useful for filenames, route fragments, and stable human-readable IDs.
    """

    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[a-zA-Z0-9]+", normalized.lower())
    return separator.join(words)


def snake_case(value: str) -> str:
    """Return ``snake_case`` text for Python identifiers or JSON keys."""

    words = _words(value)
    return "_".join(word.lower() for word in words)


def camel_case(value: str) -> str:
    """Return ``camelCase`` text for JavaScript-style property names."""

    words = _words(value)
    if not words:
        return ""
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def pascal_case(value: str) -> str:
    """Return ``PascalCase`` text for class names or type names."""

    return "".join(word.capitalize() for word in _words(value))


def truncate(value: str, max_length: int, *, suffix: str = "...") -> str:
    """Truncate text to a maximum length while preserving a suffix."""

    if max_length < 0:
        raise ValueError("max_length cannot be negative")
    if len(value) <= max_length:
        return value
    if max_length <= len(suffix):
        return value[:max_length]
    return value[: max_length - len(suffix)] + suffix


def strip_blank_lines(value: str) -> str:
    """Remove leading and trailing blank lines from multi-line text."""

    lines = value.splitlines()
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    return "\n".join(lines)


def ensure_prefix(value: str, prefix: str) -> str:
    """Add a prefix when it is missing."""

    return value if value.startswith(prefix) else f"{prefix}{value}"


def ensure_suffix(value: str, suffix: str) -> str:
    """Add a suffix when it is missing."""

    return value if value.endswith(suffix) else f"{value}{suffix}"


def _words(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return re.findall(r"[A-Za-z0-9]+", spaced)
