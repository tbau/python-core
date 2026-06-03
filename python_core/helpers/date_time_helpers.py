"""Date, time, and timezone helper functions.

Prefer timezone-aware UTC datetimes at system boundaries, then convert to local
time only for display. These helpers make that convention easy to repeat.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, date, datetime, time, timedelta, tzinfo
from zoneinfo import ZoneInfo


def utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime for storage or APIs."""

    return datetime.now(UTC)


def today_utc() -> date:
    """Return today's calendar date according to UTC."""

    return utc_now().date()


def get_timezone(name: str) -> ZoneInfo:
    """Return an IANA timezone by name, such as ``America/Chicago``."""

    return ZoneInfo(name)


def parse_iso_datetime(value: str, default_tz: tzinfo | None = UTC) -> datetime:
    """Parse an ISO datetime string and apply a default timezone when missing.

    The common ``Z`` suffix is treated as UTC. Pass ``default_tz=None`` when
    naive input should stay naive.
    """

    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None and default_tz is not None:
        return parsed.replace(tzinfo=default_tz)
    return parsed


def ensure_timezone(value: datetime, timezone_value: tzinfo | str = UTC) -> datetime:
    """Attach or convert a datetime to the requested timezone.

    Naive datetimes are assumed to already be in the target timezone. Aware
    datetimes are converted with ``astimezone``.
    """

    target = get_timezone(timezone_value) if isinstance(timezone_value, str) else timezone_value
    if value.tzinfo is None:
        return value.replace(tzinfo=target)
    return value.astimezone(target)


def to_timezone(value: datetime, timezone_name: str) -> datetime:
    """Convert a datetime to an IANA timezone by name."""

    return ensure_timezone(value, timezone_name)


def start_of_day(value: date | datetime, timezone_value: tzinfo | None = None) -> datetime:
    """Return midnight at the start of the provided day."""

    day = value.date() if isinstance(value, datetime) else value
    tz = value.tzinfo if isinstance(value, datetime) else timezone_value
    return datetime.combine(day, time.min, tzinfo=tz)


def end_of_day(value: date | datetime, timezone_value: tzinfo | None = None) -> datetime:
    """Return the final microsecond of the provided day."""

    day = value.date() if isinstance(value, datetime) else value
    tz = value.tzinfo if isinstance(value, datetime) else timezone_value
    return datetime.combine(day, time.max, tzinfo=tz)


def month_bounds(value: date | datetime) -> tuple[datetime, datetime]:
    """Return inclusive start and end datetimes for the calendar month."""

    day = value.date() if isinstance(value, datetime) else value
    tz = value.tzinfo if isinstance(value, datetime) else None
    start = datetime(day.year, day.month, 1, tzinfo=tz)
    if day.month == 12:
        next_month = datetime(day.year + 1, 1, 1, tzinfo=tz)
    else:
        next_month = datetime(day.year, day.month + 1, 1, tzinfo=tz)
    return start, next_month - timedelta(microseconds=1)


def date_range(
    start: date,
    end: date,
    *,
    inclusive: bool = True,
    step_days: int = 1,
) -> list[date]:
    """Return dates between ``start`` and ``end``.

    Set ``inclusive=False`` to exclude the end date, or use ``step_days`` to
    generate every Nth date.
    """

    if step_days <= 0:
        raise ValueError("step_days must be positive")
    current = start
    result: list[date] = []
    comparator = (lambda left, right: left <= right) if inclusive else (lambda left, right: left < right)
    while comparator(current, end):
        result.append(current)
        current += timedelta(days=step_days)
    return result


def seconds_between(start: datetime, end: datetime) -> float:
    """Return signed seconds from ``start`` to ``end``."""

    return (end - start).total_seconds()


def format_duration(total_seconds: float) -> str:
    """Format seconds as a compact duration like ``2d 4h 3m``."""

    sign = "-" if total_seconds < 0 else ""
    remaining = int(abs(total_seconds))
    days, remaining = divmod(remaining, 86_400)
    hours, remaining = divmod(remaining, 3_600)
    minutes, seconds = divmod(remaining, 60)
    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    return sign + " ".join(parts)


def age_on(born_on: date, as_of: date | None = None) -> int:
    """Return age in full years on a given date."""

    current = as_of or today_utc()
    years = current.year - born_on.year
    birthday_passed = (current.month, current.day) >= (born_on.month, born_on.day)
    return years if birthday_passed else years - 1


def is_business_day(value: date, weekend_days: Iterable[int] = (5, 6)) -> bool:
    """Return whether a date is not in the configured weekend days.

    Python weekdays are ``0`` for Monday through ``6`` for Sunday.
    """

    return value.weekday() not in set(weekend_days)


def add_business_days(
    start: date,
    business_days: int,
    *,
    weekend_days: Iterable[int] = (5, 6),
    holidays: Iterable[date] = (),
) -> date:
    """Add or subtract business days while skipping weekends and holidays."""

    holiday_set = set(holidays)
    weekend_set = set(weekend_days)
    direction = 1 if business_days >= 0 else -1
    remaining = abs(business_days)
    current = start
    while remaining:
        current += timedelta(days=direction)
        if current.weekday() not in weekend_set and current not in holiday_set:
            remaining -= 1
    return current
