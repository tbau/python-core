"""Dependency injection container."""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from python_core.di.container_scope import ContainerScope
from python_core.di.resolver import DependencyKey, Resolver
from python_core.di.service_descriptor import ServiceDescriptor
from python_core.di.service_lifetime import ServiceLifetime
from python_core.exceptions import ConfigurationError

T = TypeVar("T")


class Container:
    """Small dependency injection container."""

    def __init__(self) -> None:
        self._descriptors: dict[DependencyKey[Any], ServiceDescriptor] = {}

    def register_instance(self, key: DependencyKey[T], instance: T) -> None:
        """Register a singleton instance."""
        self._descriptors[key] = ServiceDescriptor(
            key=key,
            factory=lambda _resolver: instance,
            lifetime=ServiceLifetime.SINGLETON,
            instance=instance,
        )

    def register_factory(
        self,
        key: DependencyKey[T],
        factory: Callable[[Resolver], T],
        *,
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> None:
        """Register a factory."""
        self._descriptors[key] = ServiceDescriptor(key=key, factory=factory, lifetime=lifetime)

    def register_type(
        self,
        key: DependencyKey[T],
        implementation: type[T],
        *,
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> None:
        """Register a class with a zero-argument constructor."""
        self.register_factory(key, lambda _resolver: implementation(), lifetime=lifetime)

    def resolve(self, key: DependencyKey[T]) -> T:
        """Resolve a dependency from the root container."""
        descriptor = self.descriptor_for(key)
        if descriptor.lifetime is ServiceLifetime.SCOPED:
            raise ConfigurationError("scoped dependencies must be resolved from a ContainerScope")
        if descriptor.lifetime is ServiceLifetime.SINGLETON:
            if descriptor.instance is None:
                descriptor.instance = descriptor.factory(self)
            return descriptor.instance
        return descriptor.factory(self)

    def create_scope(self) -> ContainerScope:
        """Create a scope for request/job dependencies."""
        return ContainerScope(self)

    def descriptor_for(self, key: DependencyKey[T]) -> ServiceDescriptor:
        """Return a descriptor or raise a configuration error."""
        try:
            return self._descriptors[key]
        except KeyError as exc:
            raise ConfigurationError(f"dependency is not registered: {key}") from exc
