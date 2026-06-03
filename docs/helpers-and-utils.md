# Helpers And Utils

Use `helpers` for domain calculations and `utils` for application plumbing.
Keep both dependency-light so they can be copied into downstream projects.

## Helper Modules

- `date_time_helpers`: UTC timestamps, timezone conversion, ISO parsing,
  date ranges, business days, age, and duration formatting.
- `geo_helpers`: coordinate validation, haversine distance, bearings,
  midpoint, destination point, bounding box, and distance matrices.
- `math_helpers`: clamp, safe division, interpolation, percentages, compound
  growth, scaling, moving averages, RMS, sigmoid, and quadratic roots.
- `statistics_helpers`: mean, median, modes, variance, standard deviation,
  percentiles, z-scores, covariance, correlation, regression, histograms, and
  summary stats.
- `similarity_helpers`: Levenshtein, Damerau-Levenshtein, Jaccard, cosine,
  token fuzzy scoring, and best-match lookup.
- `physics_helpers`: force, weight, energy, momentum, density, pressure, work,
  power, waves, and mass-energy calculations.
- `chemistry_helpers`: moles, molarity, dilution, ideal gas, pH, percent yield,
  ppm, half-life, and serial dilution calculations.
- `electrical_helpers`: Ohm's law, power, series/parallel resistance, voltage
  dividers, reactance, RC time constants, and RMS/peak voltage.
- `finance_helpers`: interest, present/future value, amortized payments,
  margins, markup, break-even, and period rate conversion.
- `unit_conversion_helpers`: common temperature, distance, mass, length,
  volume, pressure, and speed conversions.

## Utility Modules

- `collection_utils`: chunk, flatten, unique, group, partition, compact, first,
  window, and take helpers.
- `string_utils`: blank checks, whitespace normalization, slugify, case
  conversion, truncation, blank-line stripping, and prefix/suffix helpers.
- `path_utils`: safe root joins, directory creation, filename sanitizing,
  SHA-256 file hashing, and atomic text writes.
- `validation_utils`: small validators that raise `ValidationError`.
- `security_utils`: secure tokens, numeric codes, constant-time comparison,
  SHA-256 hashes, HMAC-SHA256, token masking, and mapping redaction.
- `encryption_utils`: optional Fernet encryption and key-ring rotation helpers.

## Security Notes

Token helpers use `secrets`, comparison helpers use `hmac.compare_digest`, and
encryption helpers wrap `cryptography.fernet`. Do not use these helpers to
store passwords; use the auth password hashers instead.

Install optional encryption support only when needed:

```powershell
python -m pip install -e ".[security]"
```

## Example

```python
from python_core.helpers.geo_helpers import Coordinates, haversine_distance_km
from python_core.helpers.similarity_helpers import best_match
from python_core.utils.security_utils import generate_urlsafe_token, redact_mapping

home = Coordinates(41.8781, -87.6298)
office = Coordinates(40.7128, -74.0060)
distance = haversine_distance_km(home, office)

match = best_match("custmer api", ["customer api", "orders export"])
token = generate_urlsafe_token()
headers = redact_mapping({"Authorization": "Bearer secret", "Accept": "json"})
```
