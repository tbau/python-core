"""Retry with exponential backoff and a no-sleep demo."""

from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy
from python_core.reliability.retry import retry_sync


class FlakyDependency:
    """Dependency that fails once before succeeding."""

    def __init__(self) -> None:
        self.calls = 0

    def call(self) -> str:
        """Return a result after one retryable failure."""
        self.calls += 1
        if self.calls == 1:
            raise TimeoutError("temporary timeout")
        return "ok"


def main() -> None:
    """Run the retry example without sleeping during the demo."""
    dependency = FlakyDependency()
    result = retry_sync(
        dependency.call,
        policy=ExponentialBackoffRetryPolicy(
            attempts=4,
            base_delay=0.2,
            backoff=2.0,
            max_delay=3.0,
            jitter=0.1,
        ),
        retry_on=(TimeoutError,),
        sleeper=lambda _delay: None,
    )
    print(f"result={result}; calls={dependency.calls}")


if __name__ == "__main__":
    main()
