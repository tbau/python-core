"""Small showcase for helpers and utilities."""

from python_core.helpers.geo_helpers import Coordinates, haversine_distance_km
from python_core.helpers.similarity_helpers import best_match
from python_core.helpers.statistics_helpers import describe
from python_core.utils.security_utils import generate_urlsafe_token, redact_mapping


def main() -> None:
    """Run a tiny helper demo."""

    chicago = Coordinates(41.8781, -87.6298)
    new_york = Coordinates(40.7128, -74.0060)

    distance_km = haversine_distance_km(chicago, new_york)
    stats = describe([10, 12, 18, 19, 25])
    match = best_match("custmer api", ["customer api", "orders export", "billing sync"])
    token = generate_urlsafe_token()
    safe_headers = redact_mapping({"Authorization": "Bearer secret", "Accept": "application/json"})

    print(f"Chicago to New York: {distance_km:.1f} km")
    print(f"Stats: {stats}")
    print(f"Best match: {match}")
    print(f"Generated token length: {len(token)}")
    print(f"Safe headers: {safe_headers}")


if __name__ == "__main__":
    main()
