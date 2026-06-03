"""Dependency resolver interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

T = TypeVar("T")
DependencyKey = type[T] | str


class Resolver(Protocol):
    """Resolves dependencies by type or string key."""

    def resolve(self, key: DependencyKey[T]) -> T:
        """Resolve a dependency."""
