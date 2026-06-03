"""SQLAlchemy unit-of-work adapter."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Self

from python_core.db.sqlalchemy.async_session_factory import AsyncSessionFactory
from python_core.db.sqlalchemy.sqlalchemy_transaction import SQLAlchemyTransaction
from python_core.exceptions import TransactionError


class SQLAlchemyUnitOfWork:
    """Async context manager for one SQLAlchemy transaction scope."""

    def __init__(self, session_factory: AsyncSessionFactory) -> None:
        self._session_factory = session_factory
        self._session: Any | None = None
        self._transaction: SQLAlchemyTransaction | None = None

    @property
    def transaction(self) -> SQLAlchemyTransaction:
        """Return the active transaction."""
        if self._transaction is None:
            raise TransactionError("unit of work is not open")
        return self._transaction

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self._transaction = SQLAlchemyTransaction(session=self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            if self._session is not None:
                await self._session.close()
            self._session = None
            self._transaction = None

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        """Execute within the active transaction."""
        return await self.transaction.execute(statement, parameters)

    async def commit(self) -> None:
        """Commit pending work."""
        await self.transaction.commit()

    async def rollback(self) -> None:
        """Rollback pending work."""
        await self.transaction.rollback()
