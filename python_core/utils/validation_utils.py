"""Validation utility functions that raise domain-friendly errors."""

from __future__ import annotations

from collections.abc import Collection
import re
from typing import TypeVar
from urllib.parse import urlparse
from uuid import UUID

from python_core.exceptions import ValidationError

T = TypeVar("T")


def require(condition: bool, message: str) -> None:
    """Raise ``ValidationError`` when a condition is false."""

    if not condition:
        raise ValidationError(message)


def require_not_none(value: T | None, name: str) -> T:
    """Return a value or raise when it is ``None``."""

    if value is None:
        raise ValidationError(f"{name} is required")
    return value


def require_non_empty_string(value: str | None, name: str) -> str:
    """Return stripped string or raise when it is blank."""

    if value is None or value.strip() == "":
        raise ValidationError(f"{name} is required")
    return value.strip()


def require_in_range(
    value: float,
    name: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    """Return value or raise when outside configured numeric bounds."""

    if minimum is not None and value < minimum:
        raise ValidationError(f"{name} must be at least {minimum}")
    if maximum is not None and value > maximum:
        raise ValidationError(f"{name} must be at most {maximum}")
    return value


def require_allowed(value: T, allowed: Collection[T], name: str) -> T:
    """Return value or raise when it is not in an allowed set."""

    if value not in allowed:
        allowed_text = ", ".join(str(item) for item in allowed)
        raise ValidationError(f"{name} must be one of: {allowed_text}")
    return value


def is_email_like(value: str) -> bool:
    """Return whether a string looks like an email address.

    This is a lightweight shape check, not full RFC validation.
    """

    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) is not None


def is_url_like(value: str, *, allowed_schemes: Collection[str] = ("http", "https")) -> bool:
    """Return whether a string looks like a URL with an allowed scheme."""

    parsed = urlparse(value)
    return parsed.scheme in allowed_schemes and bool(parsed.netloc)


def is_uuid_like(value: str) -> bool:
    """Return whether a string can be parsed as a UUID."""

    try:
        UUID(value)
    except ValueError:
        return False
    return True
