"""Authentication and middleware example."""

from python_core.auth.identity import Identity
from python_core.middleware.middleware_chain import MiddlewareChain
from python_core.middleware.middleware_context import MiddlewareContext


class RequireAdmin:
    """Middleware that requires an admin identity."""

    def handle(self, context: MiddlewareContext) -> MiddlewareContext:
        """Reject requests without an admin identity."""
        if context.identity is None or not context.identity.has_role("admin"):
            raise PermissionError("admin role required")
        return context


def main() -> None:
    """Run one authorized request through the chain."""
    chain = MiddlewareChain([RequireAdmin()])
    context = chain.handle(
        MiddlewareContext(request_id="req_123", identity=Identity("u_1", roles={"admin"}))
    )
    print(context.request_id)


if __name__ == "__main__":
    main()
