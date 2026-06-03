# Patterns Agent

Use this guide when adding architectural pattern examples.

## Checklist

- Keep pattern code small and readable.
- Prefer interfaces plus one in-memory or example implementation.
- Add a short docs page when a pattern affects project structure.
- Avoid introducing a broker, database, Redis, or web framework dependency unless
  it is isolated behind an adapter.

## Patterns To Preserve

- Creational: builder, factory method, abstract factory, prototype, singleton
  provider, object pool.
- Structural: adapter, bridge, composite, decorator, facade, proxy.
- Behavioral: chain of responsibility, command, mediator, observer,
  specification, state, strategy, template method, visitor.
- Reliability: bulkhead, circuit breaker, idempotency, outbox, retry policies
  including fixed, linear, and exponential backoff with jitter.
- Repository and query handler for reads and persistence.
- Facade for coarse feature APIs.
- Outbox for transactional message publishing.
- Middleware for cross-cutting request concerns.
- Authenticator and authorizer as separate concepts.
- Retry policy interface plus fixed, linear, and exponential implementations.
