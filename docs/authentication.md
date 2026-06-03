# Authentication Guide

## Concepts

- `Identity`: authenticated subject, roles, and claims.
- `Permission`: action plus resource, with canonical `resource:action` names.
- `PermissionSet`: collection of permission names.
- `ResourceOwner`: resource ownership metadata.
- `OwnershipPolicy`: ownership/admin access checks.
- `Authenticator`: converts credentials into an identity.
- `Authorizer`: checks whether an identity can perform an action.
- `TokenIssuer` and `TokenVerifier`: token boundary interfaces.
- `JwtTokenService`: PyJWT-backed HS256 JWT issuing and verification.
- `JwtAuthenticator`: authenticates bearer tokens with a JWT service.
- `ApiKeyAuthenticator`: small API-key authenticator for examples.
- `Argon2idPasswordHasher`: preferred password hasher; requires `python-core[auth]`.
- `ScryptPasswordHasher`: stdlib fallback when Argon2id is unavailable.
- `OAuthClientConfig`, `OAuthAuthorizationUrlBuilder`, `OAuthTokenRequest`, and
  `OAuthToken`: OAuth/OIDC helper models.
- `OAuthStateStore`: one-time state value storage for OAuth examples.

## Rule

Authentication identifies the caller. Authorization decides what the caller may
do. Keep those steps separate.

## JWT

Use `JwtTokenService` through `python-core[auth]`. Keep secrets outside code,
set issuer and audience, and use short expirations.

## OAuth

Use the OAuth helpers to build authorization URLs and token request data. Keep
provider-specific HTTP calls in adapters so services depend on interfaces.

## Ownership

Use `ResourceOwner` and `OwnershipPolicy` when access depends on whether the
caller owns a resource. Keep admin override roles explicit.

## Password Storage

Prefer Argon2id for new projects. Use scrypt when Argon2id is unavailable.
Legacy password KDFs are intentionally not implemented in this template.
