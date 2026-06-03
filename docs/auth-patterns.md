# Auth Patterns Guide

## Permission Naming

Use `resource:action` names:

- `orders:read`
- `orders:write`
- `orders:*`

## Role Mapping

Use `RolePermissionMap` to map roles to permissions. Keep role names coarse and
permission names specific.

## Ownership

Use ownership checks when roles are not enough:

```python
owner = ResourceOwner("order", "ord_123", owner_subject="user_123")
OwnershipPolicy().can_access(identity, owner)
```

## Token Boundaries

Services should depend on `TokenIssuer` and `TokenVerifier` interfaces. Concrete
JWT/OAuth details belong in adapters or composition roots.

## Passwords

Prefer `Argon2idPasswordHasher` for new projects. Use `ScryptPasswordHasher`
when Argon2id is unavailable. Never store raw passwords.

## OAuth State

Always send and validate an OAuth state value. Use PKCE for public clients.
