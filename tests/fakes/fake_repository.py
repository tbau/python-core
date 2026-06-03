"""Fake repository template for downstream tests."""

from typing import Generic, TypeVar

EntityT = TypeVar("EntityT")


class FakeRepository(Generic[EntityT]):
    """Small in-memory repository fake."""

    def __init__(self) -> None:
        self.items: dict[str, EntityT] = {}

    def add(self, item_id: str, item: EntityT) -> None:
        self.items[item_id] = item

    def get_by_id(self, item_id: str) -> EntityT | None:
        return self.items.get(item_id)
