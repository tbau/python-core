"""JWT, OAuth, permissions, and ownership examples."""

from datetime import timedelta

from python_core.auth.identity import Identity
from python_core.auth.jwt_settings import JwtSettings
from python_core.auth.jwt_token_service import JwtTokenService
from python_core.auth.oauth_authorization_url_builder import OAuthAuthorizationUrlBuilder
from python_core.auth.oauth_client_config import OAuthClientConfig
from python_core.auth.ownership_policy import OwnershipPolicy
from python_core.auth.resource_owner import ResourceOwner
from python_core.auth.role_based_authorizer import RoleBasedAuthorizer
from python_core.auth.role_permission_map import RolePermissionMap


def build_token_service() -> JwtTokenService:
    """Create a short-lived JWT service for an application."""
    return JwtTokenService(
        JwtSettings(
            secret="dev-only-secret",
            issuer="example",
            audience="example-api",
            expires_in=timedelta(minutes=5),
        )
    )


def build_oauth_authorization_url() -> str:
    """Build the redirect URL for an OAuth authorization-code flow."""
    oauth_config = OAuthClientConfig(
        client_id="client-id",
        client_secret=None,
        authorization_url="https://auth.example.com/oauth/authorize",
        token_url="https://auth.example.com/oauth/token",
        redirect_uri="https://app.example.com/callback",
        scopes=("openid", "profile", "email"),
    )
    return OAuthAuthorizationUrlBuilder(oauth_config).build(state="state-token")


def main() -> None:
    """Run the auth examples."""
    identity = Identity(subject="user_123", roles={"admin"}, permissions={"orders:read"})
    token_service = build_token_service()
    token = token_service.issue(identity)
    verified_identity = token_service.verify(token)

    authorizer = RoleBasedAuthorizer(RolePermissionMap({"admin": {"orders:*"}}))
    owner = ResourceOwner(resource_type="order", resource_id="ord_123", owner_subject="user_123")

    print(authorizer.can(verified_identity, "write", "orders"))
    print(OwnershipPolicy().can_access(verified_identity, owner))
    print(build_oauth_authorization_url())


if __name__ == "__main__":
    main()
