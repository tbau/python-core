"""Database connector interface."""

from __future__ import annotations

from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol

from python_core.interfaces.database.transaction import Transaction
from python_core.interfaces.database.unit_of_work import UnitOfWork


class DatabaseConnector(Protocol):
    """Owns database lifecycle and unit-of-work creation."""

    async def connect(self) -> None:
        """Initialize database resources."""

    async def close(self) -> None:
        """Dispose database resources."""

    async def ping(self) -> bool:
        """Return True when the database is reachable."""

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        """Execute a statement outside an explicit unit of work."""

    async def fetch_one(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any | None:
        """Fetch one row outside an explicit unit of work."""

    async def fetch_all(self, statement: Any, parameters: dict[str, Any] | None = None) -> list[Any]:
        """Fetch rows outside an explicit unit of work."""

    def begin(self) -> AbstractAsyncContextManager[Transaction]:
        """Open a transaction context."""

    def unit_of_work(self) -> UnitOfWork:
        """Return a unit of work for transaction scopes."""
