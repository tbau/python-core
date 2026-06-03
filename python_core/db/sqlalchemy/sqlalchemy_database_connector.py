"""SQLAlchemy database connector adapter."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from python_core.db.sqlalchemy.async_session_factory import AsyncSessionFactory
from python_core.db.sqlalchemy.sqlalchemy_transaction import SQLAlchemyTransaction
from python_core.db.sqlalchemy.sqlalchemy_unit_of_work import SQLAlchemyUnitOfWork


class SQLAlchemyDatabaseConnector:
    """Database connector around a SQLAlchemy async session factory."""

    def __init__(
        self,
        session_factory: AsyncSessionFactory,
        *,
        engine: Any | None = None,
        ping_statement: Any | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._engine = engine
        self._ping_statement = ping_statement

    async def connect(self) -> None:
        """Initialize database resources."""

    async def close(self) -> None:
        """Dispose database resources."""
        if self._engine is not None:
            await self._engine.dispose()

    async def ping(self) -> bool:
        """Return True when the database is reachable."""
        if self._ping_statement is None:
            return True
        async with self.begin() as tx:
            await tx.execute(self._ping_statement)
        return True

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        """Execute outside an explicit unit of work."""
        async with self.begin() as tx:
            return await tx.execute(statement, parameters)

    async def fetch_one(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any | None:
        """Fetch one row outside an explicit unit of work."""
        async with self.begin() as tx:
            return await tx.fetch_one(statement, parameters)

    async def fetch_all(self, statement: Any, parameters: dict[str, Any] | None = None) -> list[Any]:
        """Fetch rows outside an explicit unit of work."""
        async with self.begin() as tx:
            return await tx.fetch_all(statement, parameters)

    @asynccontextmanager
    async def begin(self) -> AsyncIterator[SQLAlchemyTransaction]:
        """Open a transaction context."""
        async with self.unit_of_work() as unit_of_work:
            yield unit_of_work.transaction

    def unit_of_work(self) -> SQLAlchemyUnitOfWork:
        """Return a SQLAlchemy unit of work."""
        return SQLAlchemyUnitOfWork(self._session_factory)
