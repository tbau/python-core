"""General math and calculation helpers.

These are small, dependency-free formulas that show intent at call sites and
avoid repeated one-off arithmetic throughout application code.
"""

from __future__ import annotations

from collections.abc import Sequence
from math import exp, isclose, sqrt


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp value into the inclusive ``minimum`` to ``maximum`` range."""

    if minimum > maximum:
        raise ValueError("minimum must be less than or equal to maximum")
    return max(minimum, min(value, maximum))


def safe_divide(numerator: float, denominator: float, default: float | None = None) -> float | None:
    """Divide two numbers and return ``default`` when the denominator is zero."""

    if denominator == 0:
        return default
    return numerator / denominator


def lerp(start: float, end: float, amount: float) -> float:
    """Linearly interpolate between ``start`` and ``end``.

    ``amount=0`` returns ``start``, ``amount=1`` returns ``end``, and values
    between them return proportional points.
    """

    return start + (end - start) * amount


def inverse_lerp(start: float, end: float, value: float) -> float:
    """Return where ``value`` sits between ``start`` and ``end`` as a ratio."""

    if isclose(start, end):
        raise ValueError("start and end cannot be equal")
    return (value - start) / (end - start)


def percent(part: float, whole: float, default: float | None = None) -> float | None:
    """Return ``part / whole * 100`` with optional zero-denominator fallback."""

    divided = safe_divide(part, whole, default)
    return None if divided is None else divided * 100


def percent_change(old_value: float, new_value: float, default: float | None = None) -> float | None:
    """Return percentage change from old value to new value."""

    divided = safe_divide(new_value - old_value, old_value, default)
    return None if divided is None else divided * 100


def compound_growth(principal: float, rate: float, periods: int) -> float:
    """Return ``principal * (1 + rate) ** periods``."""

    return principal * (1 + rate) ** periods


def round_to_increment(value: float, increment: float) -> float:
    """Round a value to the nearest increment, such as ``0.05`` or ``15``."""

    if increment <= 0:
        raise ValueError("increment must be positive")
    return round(value / increment) * increment


def normalize(values: Sequence[float]) -> list[float]:
    """Normalize values so their sum is one."""

    total = sum(values)
    if total == 0:
        raise ValueError("cannot normalize values with a zero sum")
    return [value / total for value in values]


def min_max_scale(values: Sequence[float]) -> list[float]:
    """Scale values into the zero-to-one range using min-max scaling."""

    if not values:
        return []
    minimum = min(values)
    maximum = max(values)
    if isclose(minimum, maximum):
        return [0.0 for _ in values]
    return [(value - minimum) / (maximum - minimum) for value in values]


def weighted_average(values: Sequence[float], weights: Sequence[float]) -> float:
    """Return the weighted average for matching values and weights."""

    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("total weight cannot be zero")
    return sum(value * weight for value, weight in zip(values, weights, strict=True)) / total_weight


def moving_average(values: Sequence[float], window_size: int) -> list[float]:
    """Return rolling averages for a fixed-size sliding window."""

    if window_size <= 0:
        raise ValueError("window_size must be positive")
    if window_size > len(values):
        return []
    return [
        sum(values[index : index + window_size]) / window_size
        for index in range(len(values) - window_size + 1)
    ]


def root_mean_square(values: Sequence[float]) -> float:
    """Return root mean square, useful for magnitudes and AC waveforms."""

    if not values:
        raise ValueError("values cannot be empty")
    return sqrt(sum(value**2 for value in values) / len(values))


def sigmoid(value: float) -> float:
    """Return the logistic sigmoid squashed into the ``0`` to ``1`` range."""

    return 1 / (1 + exp(-value))


def quadratic_roots(a: float, b: float, c: float) -> tuple[complex, complex]:
    """Return the two roots for ``a*x^2 + b*x + c = 0``."""

    if a == 0:
        raise ValueError("a cannot be zero")
    discriminant = complex(b**2 - 4 * a * c)
    root = discriminant**0.5
    return ((-b + root) / (2 * a), (-b - root) / (2 * a))
