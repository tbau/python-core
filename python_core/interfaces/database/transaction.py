"""Transaction interface."""

from __future__ import annotations

from typing import Any, Protocol


class Transaction(Protocol):
    """Active transaction boundary."""

    @property
    def connection(self) -> Any:
        """Return the underlying driver connection or session."""

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        """Execute a statement and return the driver result."""

    async def fetch_one(
        self,
        statement: Any,
        parameters: dict[str, Any] | None = None,
    ) -> Any | None:
        """Execute a statement and return one row."""

    async def fetch_all(self, statement: Any, parameters: dict[str, Any] | None = None) -> list[Any]:
        """Execute a statement and return all rows."""

    async def commit(self) -> None:
        """Commit pending work."""

    async def rollback(self) -> None:
        """Rollback pending work."""
