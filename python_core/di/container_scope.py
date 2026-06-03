"""Dependency injection scope."""

from __future__ import annotations

from typing import Any, TypeVar

from python_core.di.resolver import DependencyKey
from python_core.di.service_lifetime import ServiceLifetime
from python_core.exceptions import ConfigurationError

T = TypeVar("T")


class ContainerScope:
    """Caches scoped dependencies for one request or job."""

    def __init__(self, container: Any) -> None:
        self._container = container
        self._instances: dict[DependencyKey[Any], Any] = {}

    def resolve(self, key: DependencyKey[T]) -> T:
        """Resolve a dependency inside this scope."""
        descriptor = self._container.descriptor_for(key)
        if descriptor.lifetime is ServiceLifetime.SCOPED:
            if key not in self._instances:
                self._instances[key] = descriptor.factory(self)
            return self._instances[key]
        return self._container.resolve(key)

    def close(self) -> None:
        """Forget scoped instances."""
        self._instances.clear()

    def descriptor_for(self, key: DependencyKey[T]) -> Any:
        """Expose descriptors for nested scope-aware factories."""
        try:
            return self._container.descriptor_for(key)
        except KeyError as exc:
            raise ConfigurationError(f"dependency is not registered: {key}") from exc
