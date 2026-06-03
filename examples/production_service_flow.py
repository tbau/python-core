"""End-to-end service flow using core building blocks.

This is the closest thing to a small production slice in the examples folder:
an application service validates a command, writes through a repository,
records an outbox message, and a dispatcher publishes that message through a
message bus. The dependency injection setup shows how to wire the same flow for
one request or background job.
"""

from __future__ import annotations

from dataclasses import dataclass

from python_core.di.container import Container
from python_core.di.service_lifetime import ServiceLifetime
from python_core.exceptions import ConflictError, ValidationError
from python_core.messaging.in_memory_message_bus import InMemoryMessageBus
from python_core.messaging.message import Message
from python_core.outbox.memory_outbox import MemoryOutbox
from python_core.outbox.outbox_message import OutboxMessage


@dataclass(frozen=True)
class RegisterCustomer:
    """Command accepted by the application service."""

    customer_id: str
    email: str


@dataclass(frozen=True)
class Customer:
    """Small domain model stored by the repository."""

    id: str
    email: str


class CustomerRepository:
    """In-memory repository with intent-named methods."""

    def __init__(self) -> None:
        self._customers: dict[str, Customer] = {}

    def get_by_id(self, customer_id: str) -> Customer | None:
        """Return a customer or None when it is missing."""
        return self._customers.get(customer_id)

    def save(self, customer: Customer) -> None:
        """Persist a customer."""
        self._customers[customer.id] = customer


class CustomerRegistrationService:
    """Coordinates validation, persistence, and post-commit messaging."""

    def __init__(self, repository: CustomerRepository, outbox: MemoryOutbox) -> None:
        self._repository = repository
        self._outbox = outbox

    def register(self, command: RegisterCustomer) -> Customer:
        """Register a customer and queue an event for later dispatch."""
        self._validate(command)
        if self._repository.get_by_id(command.customer_id) is not None:
            raise ConflictError(f"customer already exists: {command.customer_id}")

        customer = Customer(id=command.customer_id, email=command.email)
        self._repository.save(customer)
        self._outbox.add(
            OutboxMessage(
                name="customer.registered",
                payload={"customer_id": customer.id, "email": customer.email},
            )
        )
        return customer

    def _validate(self, command: RegisterCustomer) -> None:
        if not command.customer_id:
            raise ValidationError("customer_id is required")
        if "@" not in command.email:
            raise ValidationError("email must contain @")


class OutboxDispatcher:
    """Publishes pending outbox messages and marks them sent."""

    def __init__(self, outbox: MemoryOutbox, bus: InMemoryMessageBus) -> None:
        self._outbox = outbox
        self._bus = bus

    def dispatch_pending(self) -> int:
        """Publish every pending message and return the dispatch count."""
        dispatched = 0
        for item in self._outbox.pending():
            self._bus.publish(Message(name=item.name, payload=item.payload, headers=item.headers))
            self._outbox.mark_sent(item.id)
            dispatched += 1
        return dispatched


def build_container() -> Container:
    """Create app wiring for one process."""
    container = Container()
    container.register_type(CustomerRepository, CustomerRepository, lifetime=ServiceLifetime.SCOPED)
    container.register_type(MemoryOutbox, MemoryOutbox, lifetime=ServiceLifetime.SCOPED)
    container.register_instance(InMemoryMessageBus, InMemoryMessageBus())
    container.register_factory(
        CustomerRegistrationService,
        lambda resolver: CustomerRegistrationService(
            resolver.resolve(CustomerRepository),
            resolver.resolve(MemoryOutbox),
        ),
        lifetime=ServiceLifetime.SCOPED,
    )
    container.register_factory(
        OutboxDispatcher,
        lambda resolver: OutboxDispatcher(
            resolver.resolve(MemoryOutbox),
            resolver.resolve(InMemoryMessageBus),
        ),
        lifetime=ServiceLifetime.SCOPED,
    )
    return container


def main() -> None:
    """Run the service flow with in-memory infrastructure."""
    container = build_container()
    scope = container.create_scope()
    delivered: list[str] = []

    bus = scope.resolve(InMemoryMessageBus)
    bus.subscribe("customer.registered", lambda message: delivered.append(message.payload["email"]))

    service = scope.resolve(CustomerRegistrationService)
    dispatcher = scope.resolve(OutboxDispatcher)
    customer = service.register(RegisterCustomer("cust_123", "person@example.com"))

    print(f"registered: {customer.id}")
    print(f"dispatched: {dispatcher.dispatch_pending()}")
    print(f"delivered: {delivered}")
    scope.close()


if __name__ == "__main__":
    main()
