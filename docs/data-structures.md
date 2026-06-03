# Data Structures Guide

## Intent

Data structures should be boring, typed, and easy to pass between services.

## Included Concepts

- `Page`: simple pagination result with `has_more`.
- `Repository`: persistence boundary for entities.
- `Cache`: async cache boundary with optional TTL.
- `Serializer`: bytes conversion boundary.

## Rules

- Keep structures immutable when practical.
- Avoid framework-specific base classes in core structures.
- Prefer explicit fields over loosely shaped dictionaries for domain models.
- Use dictionaries at parsing and transport boundaries only when the shape is
  intentionally dynamic.
