"""Dependency injection example for request/job scoped services."""

from __future__ import annotations

from python_core.di.container import Container
from python_core.di.service_lifetime import ServiceLifetime


class UserRepository:
    """Example repository scoped to one request or job."""

    def __init__(self) -> None:
        self.saved: list[str] = []

    def save(self, email: str) -> None:
        """Persist a user email."""
        self.saved.append(email)


class RegisterUserService:
    """Example service with dependencies."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def register(self, email: str) -> None:
        """Register a user through the repository dependency."""
        self.repository.save(email)


def build_container() -> Container:
    """Wire services for the application."""
    container = Container()
    container.register_type(UserRepository, UserRepository, lifetime=ServiceLifetime.SCOPED)
    container.register_factory(
        RegisterUserService,
        lambda resolver: RegisterUserService(resolver.resolve(UserRepository)),
        lifetime=ServiceLifetime.SCOPED,
    )
    return container


def main() -> None:
    """Resolve a service in a scope and clean up the scope."""
    scope = build_container().create_scope()
    service = scope.resolve(RegisterUserService)
    service.register("person@example.com")

    repository = scope.resolve(UserRepository)
    print(repository.saved)
    scope.close()


if __name__ == "__main__":
    main()
