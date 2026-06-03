"""SQLAlchemy transaction adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from python_core.exceptions import TransactionError


@dataclass
class SQLAlchemyTransaction:
    """Transaction wrapper around a SQLAlchemy async session."""

    session: Any
    _finished: bool = field(default=False, init=False, repr=False)
    _closed: bool = field(default=False, init=False, repr=False)

    @property
    def is_finished(self) -> bool:
        """Return True after commit or rollback."""
        return self._finished

    @property
    def is_closed(self) -> bool:
        """Return True after the wrapped session has been closed."""
        return self._closed

    @property
    def connection(self) -> Any:
        """Return the wrapped SQLAlchemy session."""
        self._ensure_open()
        return self.session

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        """Execute a SQLAlchemy statement."""
        self._ensure_open()
        return await self.session.execute(statement, parameters or {})

    async def fetch_one(
        self,
        statement: Any,
        parameters: dict[str, Any] | None = None,
    ) -> Any | None:
        """Execute and return one mapping row."""
        result = await self.execute(statement, parameters)
        return result.mappings().first()

    async def fetch_all(self, statement: Any, parameters: dict[str, Any] | None = None) -> list[Any]:
        """Execute and return all mapping rows."""
        result = await self.execute(statement, parameters)
        return list(result.mappings().all())

    async def commit(self) -> None:
        """Commit pending work."""
        self._ensure_open()
        await self.session.commit()
        self._finished = True

    async def rollback(self) -> None:
        """Rollback pending work."""
        self._ensure_open()
        await self.session.rollback()
        self._finished = True

    async def close(self) -> None:
        """Close the session, rolling back unfinished work first."""
        if self._closed:
            return

        try:
            if not self._finished:
                await self.session.rollback()
                self._finished = True
        finally:
            await self.session.close()
            self._closed = True

    def _ensure_open(self) -> None:
        if self._closed:
            raise TransactionError("transaction has already been closed")
        if self._finished:
            raise TransactionError("transaction has already been committed or rolled back")
