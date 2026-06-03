from python_core.auth.bearer_token_credentials import BearerTokenCredentials
from python_core.auth.oauth_authorization_url_builder import OAuthAuthorizationUrlBuilder
from python_core.auth.oauth_client_config import OAuthClientConfig
from python_core.auth.permission import Permission
from python_core.auth.scrypt_password_hasher import ScryptPasswordHasher
from python_core.data.page import Page
from python_core.data.query_spec import QuerySpec
from python_core.exceptions import OutboxError, ValidationError
from python_core.files.excel_profile import ExcelProfile
from python_core.files.excel_reader import ExcelReader
from python_core.outbox.memory_outbox import MemoryOutbox
from python_core.patterns.reliability.bulkhead import Bulkhead
from python_core.patterns.reliability.circuit_breaker import CircuitBreaker
from python_core.redis.redis_cache import RedisCache


def test_bearer_credentials_reject_malformed_header() -> None:
    try:
        BearerTokenCredentials.from_authorization_header("Bearer")
    except ValueError:
        return

    raise AssertionError("expected ValueError")


def test_permission_parse_rejects_malformed_value() -> None:
    try:
        Permission.parse("users")
    except ValueError:
        return

    raise AssertionError("expected ValueError")


def test_oauth_authorization_url_builder_preserves_existing_query() -> None:
    config = OAuthClientConfig(
        client_id="client",
        client_secret=None,
        authorization_url="https://auth.example/authorize?prompt=login",
        token_url="https://auth.example/token",
        redirect_uri="https://app.example/callback",
        scopes=("openid", "profile"),
    )

    url = OAuthAuthorizationUrlBuilder(config).build(state="state")

    assert url.startswith("https://auth.example/authorize?")
    assert "prompt=login" in url
    assert "client_id=client" in url


def test_scrypt_verify_returns_false_for_malformed_hash() -> None:
    assert ScryptPasswordHasher(n=2**14).verify("password", "not-a-hash") is False


class EmptySheet:
    def iter_rows(self, **_kwargs: object) -> object:
        return iter(())


def test_excel_reader_headers_raise_validation_error_when_header_row_is_missing() -> None:
    reader = ExcelReader(ExcelProfile(sheet_name="Sheet1"))

    try:
        reader._headers(EmptySheet())
    except ValidationError:
        return

    raise AssertionError("expected ValidationError")


def test_memory_outbox_raises_domain_error_for_unknown_message() -> None:
    try:
        MemoryOutbox().mark_sent("missing")
    except OutboxError:
        return

    raise AssertionError("expected OutboxError")


def test_page_rejects_invalid_pagination() -> None:
    try:
        Page([], total=0, limit=0, offset=0)
    except ValueError:
        return

    raise AssertionError("expected ValueError")


def test_query_spec_rejects_invalid_pagination() -> None:
    try:
        QuerySpec(limit=10, offset=-1)
    except ValueError:
        return

    raise AssertionError("expected ValueError")


def test_bulkhead_rejects_zero_capacity() -> None:
    try:
        Bulkhead(0)
    except ValueError:
        return

    raise AssertionError("expected ValueError")


def test_circuit_breaker_rejects_zero_failure_limit() -> None:
    try:
        CircuitBreaker(failure_limit=0)
    except ValueError:
        return

    raise AssertionError("expected ValueError")


class FakeRedisClient:
    def set(self, _key: str, _value: bytes) -> None:
        pass

    def setex(self, _key: str, _ttl_seconds: int, _value: bytes) -> None:
        pass


def test_redis_cache_rejects_non_positive_ttl() -> None:
    try:
        RedisCache(FakeRedisClient()).set("key", b"value", ttl_seconds=0)
    except ValueError:
        return

    raise AssertionError("expected ValueError")
