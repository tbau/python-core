"""Unit of work interface."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Protocol, Self

from python_core.interfaces.database.transaction import Transaction


class UnitOfWork(Protocol):
    """Owns one transaction scope for a use case."""

    @property
    def transaction(self) -> Transaction:
        """Return the active transaction."""

    async def __aenter__(self) -> Self:
        """Open the unit of work."""

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Commit or rollback and release resources."""

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        """Execute within the active transaction."""

    async def commit(self) -> None:
        """Commit pending work."""

    async def rollback(self) -> None:
        """Rollback pending work."""
