"""Service descriptor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from python_core.di.resolver import DependencyKey, Resolver
from python_core.di.service_lifetime import ServiceLifetime

Factory = Callable[[Resolver], Any]


@dataclass
class ServiceDescriptor:
    """Registered dependency factory and lifetime."""

    key: DependencyKey[Any]
    factory: Factory
    lifetime: ServiceLifetime
    instance: Any | None = None
