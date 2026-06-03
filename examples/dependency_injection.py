"""Dependency injection example."""

from python_core.di.container import Container
from python_core.di.service_lifetime import ServiceLifetime


class UserRepository:
    """Example repository."""


class RegisterUserService:
    """Example service with dependencies."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository


container = Container()
container.register_type(UserRepository, UserRepository, lifetime=ServiceLifetime.SCOPED)
container.register_factory(
    RegisterUserService,
    lambda resolver: RegisterUserService(resolver.resolve(UserRepository)),
)

scope = container.create_scope()
service = scope.resolve(RegisterUserService)
