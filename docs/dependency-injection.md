# Dependency Injection Guide

## Intent

Use `python_core.di` to show a simple dependency registration pattern for
services, repositories, clients, and units of work.

## Lifetimes

- `SINGLETON`: one instance for the process.
- `TRANSIENT`: a new instance each resolve.
- `SCOPED`: one instance per `ContainerScope`, useful for request/job state.

## Example

```python
container = Container()
container.register_type(UserRepository, UserRepository, lifetime=ServiceLifetime.SCOPED)
container.register_factory(
    RegisterUserService,
    lambda resolver: RegisterUserService(resolver.resolve(UserRepository)),
)

scope = container.create_scope()
service = scope.resolve(RegisterUserService)
```
