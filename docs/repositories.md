# Repositories And Queries Guide

## Repository

Use repositories for persistence operations that are named by intent:

- `get_by_id`
- `save`
- `delete`
- `find_active_users`

## Query

Use query handlers when reads become more complex than simple repository
lookups. Keep query objects immutable and easy to log.

## Facade

Use facades for coarse feature APIs that coordinate repositories, services,
outbox messages, and external APIs.
