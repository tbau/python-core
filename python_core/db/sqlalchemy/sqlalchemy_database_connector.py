"""SQLAlchemy database connector adapter."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from python_core.db.sqlalchemy.async_session_factory import AsyncSessionFactory
from python_core.db.sqlalchemy.sqlalchemy_transaction import SQLAlchemyTransaction
from python_core.interfaces.database.database_connector import DatabaseConnector


class SQLAlchemyDatabaseConnector(DatabaseConnector):
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

    async def close(self) -> None:
        """Dispose database resources."""
        if self._engine is not None:
            await self._engine.dispose()

    async def ping(self) -> bool:
        """Return True when the database is reachable."""
        if self._ping_statement is None:
            return True
        async with self.open_transaction() as tx:
            await tx.execute(self._ping_statement)
        return True

    @asynccontextmanager
    async def open_transaction(self) -> AsyncIterator[SQLAlchemyTransaction]:
        """Open a transaction context and leave commit explicit."""
        session = self._session_factory()
        transaction = SQLAlchemyTransaction(session=session)
        try:
            yield transaction
        finally:
            await transaction.close()
