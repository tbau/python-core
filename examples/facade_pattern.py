"""Facade example."""

from dataclasses import dataclass

from python_core.outbox.memory_outbox import MemoryOutbox
from python_core.outbox.outbox_message import OutboxMessage


@dataclass(frozen=True)
class RegisterUser:
    user_id: str
    email: str


class UserFacade:
    """Coarse API that coordinates services and outbox messages."""

    def __init__(self, outbox: MemoryOutbox) -> None:
        self._outbox = outbox

    def register(self, command: RegisterUser) -> None:
        self._outbox.add(
            OutboxMessage(
                name="user.registered",
                payload={"user_id": command.user_id, "email": command.email},
            )
        )
