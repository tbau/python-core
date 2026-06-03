"""Serializer interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

ValueT = TypeVar("ValueT")


class Serializer(Protocol[ValueT]):
    """Converts values to and from bytes."""

    def dumps(self, value: ValueT) -> bytes:
        """Serialize a value."""

    def loads(self, payload: bytes) -> ValueT:
        """Deserialize a value."""
