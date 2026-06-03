"""Collection utility functions.

These are small conveniences for everyday list/iterable transformations.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import islice
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")


def chunked(values: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield lists of a fixed size from an iterable.

    The final chunk may be smaller than ``size``.
    """

    if size <= 0:
        raise ValueError("size must be positive")
    iterator = iter(values)
    while chunk := list(islice(iterator, size)):
        yield chunk


def flatten(values: Iterable[Iterable[T]]) -> list[T]:
    """Flatten one level of nested iterables into a list."""

    return [item for group in values for item in group]


def unique_preserve_order(values: Iterable[T]) -> list[T]:
    """Return unique items in first-seen order."""

    seen: set[T] = set()
    result: list[T] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def group_by(values: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group values into lists by a key function."""

    result: dict[K, list[T]] = {}
    for value in values:
        result.setdefault(key(value), []).append(value)
    return result


def partition(values: Iterable[T], predicate: Callable[[T], bool]) -> tuple[list[T], list[T]]:
    """Split values into ``(matching, non_matching)`` lists."""

    matching: list[T] = []
    non_matching: list[T] = []
    for value in values:
        if predicate(value):
            matching.append(value)
        else:
            non_matching.append(value)
    return matching, non_matching


def compact(values: Iterable[T | None]) -> list[T]:
    """Drop ``None`` values while preserving other falsey values."""

    return [value for value in values if value is not None]


def first_or_none(values: Iterable[T], predicate: Callable[[T], bool] | None = None) -> T | None:
    """Return the first value, optionally matching a predicate."""

    for value in values:
        if predicate is None or predicate(value):
            return value
    return None


def windowed(values: Sequence[T], size: int) -> list[tuple[T, ...]]:
    """Return fixed-size sliding windows over a sequence."""

    if size <= 0:
        raise ValueError("size must be positive")
    return [tuple(values[index : index + size]) for index in range(len(values) - size + 1)]


def take(values: Iterable[T], count: int) -> list[T]:
    """Return the first ``count`` values from an iterable."""

    if count < 0:
        raise ValueError("count cannot be negative")
    return list(islice(values, count))
