from python_core.exceptions import IdempotencyError
from python_core.reliability.idempotency_checker import IdempotencyChecker
from python_core.reliability.idempotency_key import IdempotencyKey


def test_idempotency_key_uses_prefix() -> None:
    key = IdempotencyKey.generate(prefix="order")

    assert key.value.startswith("order-")
    assert key.as_header() == {"Idempotency-Key": key.value}


def test_idempotency_checker_adds_key_once() -> None:
    checker = IdempotencyChecker()
    key = checker.create_key(prefix="order")

    assert checker.check_and_add(key) is True
    assert checker.check_and_add(key) is False
    assert checker.has_seen(key) is True


def test_idempotency_checker_remembers_result() -> None:
    checker = IdempotencyChecker()
    key = IdempotencyKey.generate(prefix="order")

    assert checker.check_and_add(key, result="created:123") is True

    assert checker.result_for(key) == "created:123"


def test_idempotency_checker_can_raise_for_duplicate() -> None:
    checker = IdempotencyChecker()
    key = IdempotencyKey.generate(prefix="order")
    checker.check_and_add(key)

    try:
        checker.require_new(key)
    except IdempotencyError:
        return

    raise AssertionError("expected IdempotencyError")
