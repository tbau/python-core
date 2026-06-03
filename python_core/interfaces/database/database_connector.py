"""Database connector interface."""

from __future__ import annotations

from contextlib import AbstractAsyncContextManager
from typing import Protocol

from python_core.interfaces.database.transaction import Transaction


class DatabaseConnector(Protocol):
    """Owns database health checks and transaction creation."""

    async def close(self) -> None:
        """Dispose database resources."""

    async def ping(self) -> bool:
        """Return True when the database is reachable."""

    def open_transaction(self) -> AbstractAsyncContextManager[Transaction]:
        """Open a transaction context."""
