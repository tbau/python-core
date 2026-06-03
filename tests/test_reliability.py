from python_core.exceptions import RetryExhaustedError
from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy
from python_core.reliability.no_retry_policy import NoRetryPolicy
from python_core.reliability.retry import retry_sync
from python_core.reliability.timeout_config import TimeoutConfig


def test_retry_sync_eventually_returns_value() -> None:
    attempts = 0

    def operation() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ValueError("try again")
        return "ok"

    result = retry_sync(
        operation,
        policy=ExponentialBackoffRetryPolicy(attempts=3, base_delay=0, jitter=0),
        retry_on=(ValueError,),
    )

    assert result == "ok"
    assert attempts == 2


def test_retry_sync_raises_when_exhausted() -> None:
    def operation() -> str:
        raise ValueError("nope")

    try:
        retry_sync(
            operation,
            policy=ExponentialBackoffRetryPolicy(attempts=2, base_delay=0, jitter=0),
            retry_on=(ValueError,),
        )
    except RetryExhaustedError:
        return

    raise AssertionError("expected RetryExhaustedError")


def test_retry_sync_reraises_original_error_when_no_retry_policy_is_used() -> None:
    def operation() -> str:
        raise ValueError("nope")

    try:
        retry_sync(operation, policy=NoRetryPolicy(), retry_on=(ValueError,))
    except ValueError:
        return

    raise AssertionError("expected ValueError")


def test_timeout_config_rejects_negative_values() -> None:
    try:
        TimeoutConfig(connect=-1)
    except ValueError:
        return

    raise AssertionError("expected ValueError")
