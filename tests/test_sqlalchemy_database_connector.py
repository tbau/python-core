import asyncio
from typing import Any

from python_core.exceptions import TransactionError
from python_core.db.sqlalchemy.sqlalchemy_database_connector import SQLAlchemyDatabaseConnector


class FakeSession:
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False
        self.closed = False
        self.added: list[object] = []

    def add(self, entity: object) -> None:
        self.added.append(entity)

    async def execute(self, statement: Any, parameters: dict[str, Any] | None = None) -> Any:
        return statement, parameters

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True

    async def close(self) -> None:
        self.closed = True


def test_open_transaction_rolls_back_uncommitted_clean_exit() -> None:
    session = FakeSession()
    connector = SQLAlchemyDatabaseConnector(lambda: session)

    async def run() -> None:
        async with connector.open_transaction() as tx:
            tx.connection.add("entity")

    asyncio.run(run())

    assert session.added == ["entity"]
    assert not session.committed
    assert session.rolled_back
    assert session.closed


def test_open_transaction_commits_when_called_explicitly() -> None:
    session = FakeSession()
    connector = SQLAlchemyDatabaseConnector(lambda: session)

    async def run() -> None:
        async with connector.open_transaction() as tx:
            await tx.commit()

    asyncio.run(run())

    assert session.committed
    assert not session.rolled_back
    assert session.closed


def test_transaction_connection_is_unavailable_after_commit() -> None:
    session = FakeSession()
    connector = SQLAlchemyDatabaseConnector(lambda: session)

    async def run() -> None:
        async with connector.open_transaction() as tx:
            await tx.commit()
            try:
                tx.connection.add("entity")
            except TransactionError:
                return
            raise AssertionError("expected TransactionError")

    asyncio.run(run())


def test_transaction_close_rolls_back_unfinished_work_and_closes_session() -> None:
    session = FakeSession()
    connector = SQLAlchemyDatabaseConnector(lambda: session)

    async def run() -> None:
        async with connector.open_transaction() as tx:
            tx.connection.add("entity")
            await tx.close()
            try:
                await tx.commit()
            except TransactionError:
                return
            raise AssertionError("expected TransactionError")

    asyncio.run(run())

    assert session.added == ["entity"]
    assert not session.committed
    assert session.rolled_back
    assert session.closed


def test_transaction_close_after_commit_closes_without_rollback() -> None:
    session = FakeSession()
    connector = SQLAlchemyDatabaseConnector(lambda: session)

    async def run() -> None:
        async with connector.open_transaction() as tx:
            await tx.commit()
            await tx.close()
            await tx.close()

    asyncio.run(run())

    assert session.committed
    assert not session.rolled_back
    assert session.closed


def test_open_transaction_rolls_back_on_error() -> None:
    session = FakeSession()
    connector = SQLAlchemyDatabaseConnector(lambda: session)

    async def run() -> None:
        async with connector.open_transaction():
            raise RuntimeError("write failed")

    try:
        asyncio.run(run())
    except RuntimeError:
        pass
    else:
        raise AssertionError("expected RuntimeError")

    assert not session.committed
    assert session.rolled_back
    assert session.closed
