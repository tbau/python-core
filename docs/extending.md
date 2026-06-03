# Extending The Library

## Add A New Integration

1. Define the smallest useful interface.
2. Keep provider-specific code in its own adapter module.
3. Accept dependencies in constructors.
4. Make timeouts, retries, logging, and transactions explicit.
5. Add docs and tests before using the integration elsewhere.

## Add A Pattern

1. Add the smallest interface.
2. Add one in-memory or example implementation.
3. Add a docs page that explains when to use it.
4. Add an example that can be copied into a new project.
5. Avoid framework dependencies unless they are optional.

## Naming

- Use concrete names for adapters: `SQLAlchemyUnitOfWork`, `SQLAlchemyDatabaseConnector`, `ApiClient`.
- Use capability names for interfaces: `UnitOfWork`, `FileParser`, `EventLogger`.
- Avoid names like `Manager`, `Helper`, or `Utils` unless the scope is truly
  generic.
