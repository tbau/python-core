"""Repository interface."""

from __future__ import annotations

from typing import Protocol, TypeVar

EntityT = TypeVar("EntityT")
IdT = TypeVar("IdT")


class Repository(Protocol[EntityT, IdT]):
    """Persistence boundary for entity-oriented services."""

    def get_by_id(self, entity_id: IdT) -> EntityT | None:
        """Return one entity by id, or None."""

    def save(self, entity: EntityT) -> EntityT:
        """Persist and return an entity."""

    def delete(self, entity_id: IdT) -> None:
        """Delete an entity by id."""
