"""SQLAlchemy transaction usage with explicit commit and automatic close."""

import asyncio
from collections.abc import Callable
from typing import Any

from python_core.db.sqlalchemy.sqlalchemy_database_connector import SQLAlchemyDatabaseConnector


class FakeAsyncSession:
    """Tiny AsyncSession-like object for demonstrating the transaction shape."""

    def __init__(self) -> None:
        self.added: list[object] = []
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def add(self, entity: object) -> None:
        """Track an entity added through the transaction connection."""
        self.added.append(entity)

    async def commit(self) -> None:
        """Mark the fake session committed."""
        self.committed = True

    async def rollback(self) -> None:
        """Mark the fake session rolled back."""
        self.rolled_back = True

    async def close(self) -> None:
        """Mark the fake session closed."""
        self.closed = True


async def save_with_transaction(session_factory: Callable[[], Any], entity: object) -> None:
    """Save an entity and explicitly commit before leaving the context."""
    connector = SQLAlchemyDatabaseConnector(session_factory)

    async with connector.open_transaction() as tx:
        tx.connection.add(entity)
        await tx.commit()


async def rollback_uncommitted_work(session_factory: Callable[[], Any], entity: object) -> None:
    """Leave the transaction uncommitted so the context rolls it back."""
    connector = SQLAlchemyDatabaseConnector(session_factory)

    async with connector.open_transaction() as tx:
        tx.connection.add(entity)


async def demo() -> FakeAsyncSession:
    """Run the example with the fake async session."""
    session = FakeAsyncSession()
    await save_with_transaction(lambda: session, {"id": "order_123"})
    return session


def main() -> None:
    """Run the async transaction demo."""
    session = asyncio.run(demo())
    print(f"committed={session.committed}; closed={session.closed}")


if __name__ == "__main__":
    main()
