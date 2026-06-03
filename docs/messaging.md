# Messaging Guide

## Concepts

- `Message`: a small envelope with name, payload, and headers.
- `MessagePublisher`: interface for publishing.
- `MessageHandler`: interface for consuming.
- `InMemoryMessageBus`: local example implementation for tests and demos.

## Queue Adapters

Real projects can add adapters for RabbitMQ, SQS, Azure Service Bus, Kafka, or
Celery without changing services. Services should depend on `MessagePublisher`.

## Naming

Use past-tense event names for facts:

- `user.registered`
- `invoice.created`
- `payment.failed`
