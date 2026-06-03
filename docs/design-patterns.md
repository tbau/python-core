# Design Patterns Guide

Patterns live under `python_core/patterns` and are grouped by family.

## Creational

- Builder
- Factory Method
- Abstract Factory
- Prototype
- Singleton Provider
- Object Pool

## Structural

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Proxy

## Behavioral

- Chain of Responsibility
- Command
- Mediator
- Observer
- Specification
- State
- Strategy
- Template Method
- Visitor

## Reliability

- Bulkhead
- Circuit Breaker
- Idempotency
- Outbox
- Retry policies: no retry, fixed, linear backoff, exponential backoff with jitter

## Repository

Repositories hide persistence details behind intent-named methods. Keep SQL,
ORM, Redis, and API-specific code inside repository implementations.

## Query Handler

Use query handlers for read-only use cases that need filtering, sorting, or
projection. `QuerySpec` gives projects a starter shape for common list queries.

## Facade

Use facades when a feature needs to coordinate multiple services, repositories,
queues, outbox messages, or external APIs behind one simple API.

## Outbox

Use the outbox pattern when a database write and a message publish must stay in
sync. Store the message during the transaction, then dispatch pending messages
after commit.

## Middleware

Use middleware for cross-cutting request concerns such as auth, request IDs,
logging context, idempotency checks, and feature flags.

## Retry

Use the `RetryPolicy` interface with a concrete policy such as
`ExponentialBackoffRetryPolicy`. Keep retries explicit at the call site so
writes can require idempotency keys.
