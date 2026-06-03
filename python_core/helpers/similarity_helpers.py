"""String and vector similarity helpers.

Use these helpers for small in-memory matching tasks such as typo-tolerant
lookup, duplicate detection, command matching, and simple vector comparison.
They are intentionally dependency-free; use a search engine or vector database
when you need ranking over large datasets.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Iterable, Sequence
import re


def tokenize(value: str) -> list[str]:
    """Return lowercase alphanumeric word tokens.

    Punctuation and whitespace are treated as separators, so
    ``"Customer API!"`` becomes ``["customer", "api"]``.
    """

    return re.findall(r"[a-z0-9]+", value.lower())


def levenshtein_distance(left: str, right: str) -> int:
    """Return the number of single-character edits needed to transform text.

    Levenshtein distance counts insertions, deletions, and substitutions. A
    distance of ``0`` means the strings are identical; smaller values mean the
    strings are more similar.
    """

    if left == right:
        return 0
    if not left:
        return len(right)
    if not right:
        return len(left)

    # Dynamic programming stores only the previous row so memory grows with the
    # shorter side of the comparison instead of the full matrix.
    previous = list(range(len(right) + 1))
    for left_index, left_char in enumerate(left, start=1):
        current = [left_index]
        for right_index, right_char in enumerate(right, start=1):
            insert_cost = current[right_index - 1] + 1
            delete_cost = previous[right_index] + 1
            replace_cost = previous[right_index - 1] + (left_char != right_char)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]


def damerau_levenshtein_distance(left: str, right: str) -> int:
    """Return edit distance where swapped adjacent characters count as one edit.

    This is useful for human typos like ``"teh"`` versus ``"the"`` where two
    neighboring letters are accidentally transposed.
    """

    distances: dict[tuple[int, int], int] = {}
    left_length = len(left)
    right_length = len(right)
    for left_index in range(-1, left_length + 1):
        distances[(left_index, -1)] = left_index + 1
    for right_index in range(-1, right_length + 1):
        distances[(-1, right_index)] = right_index + 1

    for left_index in range(left_length):
        for right_index in range(right_length):
            cost = 0 if left[left_index] == right[right_index] else 1
            distances[(left_index, right_index)] = min(
                distances[(left_index - 1, right_index)] + 1,
                distances[(left_index, right_index - 1)] + 1,
                distances[(left_index - 1, right_index - 1)] + cost,
            )
            if (
                left_index
                and right_index
                and left[left_index] == right[right_index - 1]
                and left[left_index - 1] == right[right_index]
            ):
                distances[(left_index, right_index)] = min(
                    distances[(left_index, right_index)],
                    distances[(left_index - 2, right_index - 2)] + cost,
                )
    return distances[(left_length - 1, right_length - 1)]


def normalized_levenshtein_similarity(left: str, right: str) -> float:
    """Return Levenshtein similarity normalized from ``0.0`` to ``1.0``.

    ``1.0`` means exact match and ``0.0`` means the edit distance is as large
    as the longer string.
    """

    longest = max(len(left), len(right))
    if longest == 0:
        return 1.0
    return 1 - levenshtein_distance(left, right) / longest


def jaccard_similarity(left: Iterable[str], right: Iterable[str]) -> float:
    """Return set overlap similarity for tokens or tags.

    Jaccard similarity is ``intersection / union``. It ignores duplicate items,
    which makes it useful for comparing tag sets or normalized token sets.
    """

    left_set = set(left)
    right_set = set(right)
    if not left_set and not right_set:
        return 1.0
    union = left_set | right_set
    return len(left_set & right_set) / len(union)


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    """Return cosine similarity for numeric vectors.

    Cosine similarity measures direction rather than magnitude. ``1.0`` points
    in the same direction, ``0.0`` is orthogonal, and negative values point in
    opposite directions.
    """

    if len(left) != len(right):
        raise ValueError("vectors must have the same length")
    numerator = sum(left_value * right_value for left_value, right_value in zip(left, right, strict=True))
    left_norm = sum(value**2 for value in left) ** 0.5
    right_norm = sum(value**2 for value in right) ** 0.5
    if left_norm == 0 or right_norm == 0:
        raise ValueError("cosine similarity requires non-zero vectors")
    return numerator / (left_norm * right_norm)


def token_cosine_similarity(left: str, right: str) -> float:
    """Return cosine similarity after converting strings into token counts.

    This rewards strings that share repeated important words, while still
    ignoring punctuation and letter case.
    """

    left_counts = Counter(tokenize(left))
    right_counts = Counter(tokenize(right))
    vocabulary = sorted(set(left_counts) | set(right_counts))
    if not vocabulary:
        return 1.0
    if not left_counts or not right_counts:
        return 0.0
    return cosine_similarity(
        [float(left_counts[token]) for token in vocabulary],
        [float(right_counts[token]) for token in vocabulary],
    )


def token_sort_ratio(left: str, right: str) -> float:
    """Return edit similarity after sorting tokens alphabetically.

    This makes word order less important, so ``"api customer"`` and
    ``"customer api"`` score as an exact token-sort match.
    """

    return normalized_levenshtein_similarity(
        " ".join(sorted(tokenize(left))),
        " ".join(sorted(tokenize(right))),
    )


def token_set_ratio(left: str, right: str) -> float:
    """Return token-set overlap after normalizing text into words.

    Duplicates and word order are ignored. Prefer this for tags, labels, and
    short search phrases where shared terms matter more than exact spelling.
    """

    return jaccard_similarity(tokenize(left), tokenize(right))


def fuzzy_score(left: str, right: str) -> float:
    """Return a forgiving fuzzy-search score from ``0.0`` to ``1.0``.

    The score is the best of exact edit similarity, token-order-insensitive
    similarity, token-set overlap, and token-count cosine similarity.
    """

    return max(
        normalized_levenshtein_similarity(left.lower(), right.lower()),
        token_sort_ratio(left, right),
        token_set_ratio(left, right),
        token_cosine_similarity(left, right),
    )


def best_match(
    query: str,
    choices: Iterable[str],
    *,
    scorer: Callable[[str, str], float] = fuzzy_score,
    minimum_score: float = 0.0,
) -> tuple[str, float] | None:
    """Return the highest-scoring choice for a query.

    The returned tuple is ``(choice, score)``. ``None`` is returned when there
    are no choices or when the best score is below ``minimum_score``.
    """

    best_choice: str | None = None
    best_score = float("-inf")
    for choice in choices:
        score = scorer(query, choice)
        if score > best_score:
            best_choice = choice
            best_score = score
    if best_choice is None or best_score < minimum_score:
        return None
    return best_choice, best_score
