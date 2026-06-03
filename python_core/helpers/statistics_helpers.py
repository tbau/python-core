"""Statistics helpers for small in-memory datasets.

These functions are meant for application-level summaries, validation checks,
simple reports, and examples. For large numeric workloads, prefer NumPy,
SciPy, or pandas in an adapter layer.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True, slots=True)
class LinearRegressionResult:
    """Result of fitting a straight line through paired ``x`` and ``y`` values.

    ``slope`` is the change in ``y`` for each one-unit change in ``x``.
    ``intercept`` is the predicted ``y`` value when ``x`` is zero.
    ``r_value`` is the Pearson correlation coefficient for the fit.
    """

    slope: float
    intercept: float
    r_value: float

    def predict(self, x_value: float) -> float:
        """Predict a ``y`` value from the regression line."""

        return self.slope * x_value + self.intercept


def _require_values(values: Sequence[float]) -> None:
    if not values:
        raise ValueError("values cannot be empty")


def mean(values: Sequence[float]) -> float:
    """Return arithmetic mean, the sum divided by the number of values."""

    _require_values(values)
    return sum(values) / len(values)


def median(values: Sequence[float]) -> float:
    """Return the middle value after sorting.

    When there is an even number of values, the two middle values are averaged.
    """

    _require_values(values)
    sorted_values = sorted(values)
    midpoint = len(sorted_values) // 2
    if len(sorted_values) % 2:
        return sorted_values[midpoint]
    return (sorted_values[midpoint - 1] + sorted_values[midpoint]) / 2


def modes(values: Sequence[float]) -> list[float]:
    """Return all values tied for highest frequency."""

    _require_values(values)
    counts = Counter(values)
    highest = max(counts.values())
    return [value for value, count in counts.items() if count == highest]


def variance(values: Sequence[float], *, sample: bool = True) -> float:
    """Return how spread out values are around the mean.

    Set ``sample=True`` when the values are a sample from a larger population;
    this uses ``n - 1`` in the denominator. Set ``sample=False`` when the values
    are the full population; this uses ``n``.
    """

    _require_values(values)
    if sample and len(values) < 2:
        raise ValueError("sample variance requires at least two values")
    average = mean(values)
    denominator = len(values) - 1 if sample else len(values)
    return sum((value - average) ** 2 for value in values) / denominator


def standard_deviation(values: Sequence[float], *, sample: bool = True) -> float:
    """Return the square root of variance in the original unit of measure."""

    return sqrt(variance(values, sample=sample))


def percentile(values: Sequence[float], percentile_value: float) -> float:
    """Return the requested percentile using linear interpolation.

    ``0`` returns the minimum, ``50`` returns the median-like midpoint, and
    ``100`` returns the maximum.
    """

    _require_values(values)
    if not 0 <= percentile_value <= 100:
        raise ValueError("percentile_value must be between 0 and 100")
    sorted_values = sorted(values)
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (percentile_value / 100) * (len(sorted_values) - 1)
    lower_index = int(rank)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = rank - lower_index
    return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight


def interquartile_range(values: Sequence[float]) -> float:
    """Return the middle-spread measure ``Q3 - Q1``."""

    return percentile(values, 75) - percentile(values, 25)


def z_scores(values: Sequence[float]) -> list[float]:
    """Return each value measured in standard deviations from the mean."""

    deviation = standard_deviation(values, sample=False)
    if deviation == 0:
        return [0.0 for _ in values]
    average = mean(values)
    return [(value - average) / deviation for value in values]


def covariance(left: Sequence[float], right: Sequence[float], *, sample: bool = True) -> float:
    """Return how two datasets move together.

    Positive covariance means the values tend to rise together. Negative
    covariance means one tends to fall as the other rises.
    """

    if len(left) != len(right):
        raise ValueError("left and right must have the same length")
    _require_values(left)
    if sample and len(left) < 2:
        raise ValueError("sample covariance requires at least two values")
    left_mean = mean(left)
    right_mean = mean(right)
    denominator = len(left) - 1 if sample else len(left)
    return sum(
        (left_value - left_mean) * (right_value - right_mean)
        for left_value, right_value in zip(left, right, strict=True)
    ) / denominator


def correlation(left: Sequence[float], right: Sequence[float]) -> float:
    """Return Pearson correlation coefficient from ``-1.0`` to ``1.0``.

    ``1.0`` is a perfect positive linear relationship, ``-1.0`` is a perfect
    negative linear relationship, and ``0.0`` means no linear relationship.
    """

    left_deviation = standard_deviation(left)
    right_deviation = standard_deviation(right)
    if left_deviation == 0 or right_deviation == 0:
        raise ValueError("correlation requires non-zero variance")
    return covariance(left, right) / (left_deviation * right_deviation)


def linear_regression(x_values: Sequence[float], y_values: Sequence[float]) -> LinearRegressionResult:
    """Fit a simple least-squares ``y = slope*x + intercept`` line."""

    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    x_deviation = variance(x_values)
    if x_deviation == 0:
        raise ValueError("x_values must have non-zero variance")
    slope = covariance(x_values, y_values) / x_deviation
    intercept = mean(y_values) - slope * mean(x_values)
    return LinearRegressionResult(slope=slope, intercept=intercept, r_value=correlation(x_values, y_values))


def histogram(values: Sequence[float], bins: int) -> dict[tuple[float, float], int]:
    """Return counts for evenly sized numeric ranges.

    The dictionary keys are ``(lower, upper)`` bin boundaries and values are
    counts. The final bin includes the maximum value.
    """

    _require_values(values)
    if bins <= 0:
        raise ValueError("bins must be positive")
    minimum = min(values)
    maximum = max(values)
    if minimum == maximum:
        return {(minimum, maximum): len(values)}
    width = (maximum - minimum) / bins
    result: dict[tuple[float, float], int] = {}
    for index in range(bins):
        lower = minimum + index * width
        upper = maximum if index == bins - 1 else lower + width
        result[(lower, upper)] = 0
    for value in values:
        index = min(int((value - minimum) / width), bins - 1)
        lower = minimum + index * width
        upper = maximum if index == bins - 1 else lower + width
        result[(lower, upper)] += 1
    return result


def describe(values: Sequence[float]) -> dict[str, float]:
    """Return common summary statistics for quick reporting."""

    _require_values(values)
    return {
        "count": float(len(values)),
        "mean": mean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "std_dev": standard_deviation(values, sample=False),
        "p25": percentile(values, 25),
        "p75": percentile(values, 75),
    }
