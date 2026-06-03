"""Latitude, longitude, and spherical geography helpers.

These helpers use spherical-earth formulas, which are excellent for most app
features such as sorting by distance or drawing search radii. Use a GIS library
when you need survey-grade ellipsoid calculations.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import asin, atan2, cos, degrees, radians, sin, sqrt

EARTH_RADIUS_KM = 6_371.0088
KM_PER_MILE = 1.609344


@dataclass(frozen=True, slots=True)
class Coordinates:
    """Geographic coordinates in decimal degrees.

    Latitude is north/south and must be between ``-90`` and ``90``. Longitude is
    east/west and must be between ``-180`` and ``180``.
    """

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")


def haversine_distance_km(
    start: Coordinates,
    end: Coordinates,
    *,
    radius_km: float = EARTH_RADIUS_KM,
) -> float:
    """Return great-circle distance between two points in kilometers.

    The haversine formula measures shortest distance over the surface of a
    sphere, which is the usual "as the crow flies" distance between locations.
    """

    lat1 = radians(start.latitude)
    lat2 = radians(end.latitude)
    delta_lat = radians(end.latitude - start.latitude)
    delta_lon = radians(end.longitude - start.longitude)

    haversine = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return 2 * radius_km * asin(sqrt(haversine))


def haversine_distance_miles(start: Coordinates, end: Coordinates) -> float:
    """Return great-circle distance between two points in miles."""

    return haversine_distance_km(start, end) / KM_PER_MILE


def initial_bearing_degrees(start: Coordinates, end: Coordinates) -> float:
    """Return the compass bearing from start to end.

    ``0`` means north, ``90`` east, ``180`` south, and ``270`` west.
    """

    lat1 = radians(start.latitude)
    lat2 = radians(end.latitude)
    delta_lon = radians(end.longitude - start.longitude)
    y = sin(delta_lon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)
    return (degrees(atan2(y, x)) + 360) % 360


def midpoint(start: Coordinates, end: Coordinates) -> Coordinates:
    """Return the midpoint along the great-circle path between two coordinates."""

    lat1 = radians(start.latitude)
    lon1 = radians(start.longitude)
    lat2 = radians(end.latitude)
    delta_lon = radians(end.longitude - start.longitude)

    bx = cos(lat2) * cos(delta_lon)
    by = cos(lat2) * sin(delta_lon)
    lat3 = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1) + bx) ** 2 + by**2))
    lon3 = lon1 + atan2(by, cos(lat1) + bx)
    return Coordinates(degrees(lat3), normalize_longitude(degrees(lon3)))


def destination_point(
    start: Coordinates,
    distance_km: float,
    bearing_degrees: float,
    *,
    radius_km: float = EARTH_RADIUS_KM,
) -> Coordinates:
    """Return the coordinate reached after traveling distance at a bearing."""

    angular_distance = distance_km / radius_km
    bearing = radians(bearing_degrees)
    lat1 = radians(start.latitude)
    lon1 = radians(start.longitude)

    lat2 = asin(
        sin(lat1) * cos(angular_distance)
        + cos(lat1) * sin(angular_distance) * cos(bearing)
    )
    lon2 = lon1 + atan2(
        sin(bearing) * sin(angular_distance) * cos(lat1),
        cos(angular_distance) - sin(lat1) * sin(lat2),
    )
    return Coordinates(degrees(lat2), normalize_longitude(degrees(lon2)))


def bounding_box(center: Coordinates, radius_km: float) -> tuple[Coordinates, Coordinates]:
    """Return southwest and northeast corners around a search radius.

    This is a fast pre-filter for location search. It returns a square-ish box,
    so use ``haversine_distance_km`` afterward when you need an exact radius.
    """

    lat_delta = degrees(radius_km / EARTH_RADIUS_KM)
    lon_delta = degrees(radius_km / (EARTH_RADIUS_KM * max(cos(radians(center.latitude)), 1e-12)))
    southwest = Coordinates(
        max(center.latitude - lat_delta, -90),
        normalize_longitude(center.longitude - lon_delta),
    )
    northeast = Coordinates(
        min(center.latitude + lat_delta, 90),
        normalize_longitude(center.longitude + lon_delta),
    )
    return southwest, northeast


def normalize_longitude(longitude: float) -> float:
    """Normalize any longitude into the ``-180`` to ``180`` range."""

    return ((longitude + 180) % 360) - 180


def distance_matrix(points: list[Coordinates]) -> list[list[float]]:
    """Return a square matrix of pairwise haversine distances in kilometers."""

    return [[haversine_distance_km(left, right) for right in points] for left in points]
