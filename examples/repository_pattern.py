"""Repository and query example."""

from dataclasses import dataclass

from python_core.data.query_spec import QuerySpec


@dataclass(frozen=True)
class User:
    id: str
    email: str
    active: bool = True


class UserRepository:
    """Small repository example using in-memory data."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def add(self, user: User) -> None:
        self._users[user.id] = user

    def get_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def query(self, spec: QuerySpec) -> list[User]:
        users = list(self._users.values())
        if spec.filters.get("active") is not None:
            users = [user for user in users if user.active is spec.filters["active"]]
        return users[spec.offset : spec.offset + spec.limit]
