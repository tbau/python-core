"""Example SQLAlchemy unit-of-work usage."""

from collections.abc import Callable
from typing import Any

from python_core.db.sqlalchemy.sqlalchemy_unit_of_work import SQLAlchemyUnitOfWork


async def save_with_transaction(session_factory: Callable[[], Any], entity: object) -> None:
    unit_of_work = SQLAlchemyUnitOfWork(session_factory)

    async with unit_of_work as work:
        work.transaction.connection.add(entity)
