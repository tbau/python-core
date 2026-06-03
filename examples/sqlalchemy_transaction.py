"""Example SQLAlchemy transaction usage."""

from collections.abc import Callable
from typing import Any

from python_core.db.sqlalchemy.sqlalchemy_database_connector import SQLAlchemyDatabaseConnector


async def save_with_transaction(session_factory: Callable[[], Any], entity: object) -> None:
    connector = SQLAlchemyDatabaseConnector(session_factory)

    async with connector.open_transaction() as tx:
        tx.connection.add(entity)
        await tx.commit()
