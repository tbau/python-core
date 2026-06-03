"""SQLAlchemy transaction adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SQLAlchemyTransaction:
    """Transaction wrapper around a SQLAlchemy async session."""

    session: Any

    @property
    def connection(self) -> Any:
        """Return the wrapped SQLAlchemy session."""
        return self.session

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        """Execute a SQLAlchemy statement."""
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
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback pending work."""
        await self.session.rollback()
