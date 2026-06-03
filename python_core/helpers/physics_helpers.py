"""Common physics calculation helpers.

Values use SI units unless the function name says otherwise.
"""

from __future__ import annotations

GRAVITY_EARTH_M_S2 = 9.80665
SPEED_OF_LIGHT_M_S = 299_792_458.0


def force_newtons(mass_kg: float, acceleration_m_s2: float) -> float:
    """Return force in newtons using ``F = mass * acceleration``."""

    return mass_kg * acceleration_m_s2


def weight_newtons(mass_kg: float, gravity_m_s2: float = GRAVITY_EARTH_M_S2) -> float:
    """Return weight force for a mass under gravity."""

    return mass_kg * gravity_m_s2


def kinetic_energy_joules(mass_kg: float, velocity_m_s: float) -> float:
    """Return kinetic energy in joules using ``0.5 * mass * velocity^2``."""

    return 0.5 * mass_kg * velocity_m_s**2


def potential_energy_joules(
    mass_kg: float,
    height_m: float,
    gravity_m_s2: float = GRAVITY_EARTH_M_S2,
) -> float:
    """Return gravitational potential energy in joules."""

    return mass_kg * gravity_m_s2 * height_m


def momentum_kg_m_s(mass_kg: float, velocity_m_s: float) -> float:
    """Return linear momentum using ``mass * velocity``."""

    return mass_kg * velocity_m_s


def density_kg_m3(mass_kg: float, volume_m3: float) -> float:
    """Return density in kilograms per cubic meter."""

    if volume_m3 == 0:
        raise ValueError("volume_m3 cannot be zero")
    return mass_kg / volume_m3


def pressure_pascals(force_newtons_value: float, area_m2: float) -> float:
    """Return pressure in pascals using ``force / area``."""

    if area_m2 == 0:
        raise ValueError("area_m2 cannot be zero")
    return force_newtons_value / area_m2


def work_joules(force_newtons_value: float, distance_m: float, cos_theta: float = 1.0) -> float:
    """Return work done by a force over a distance.

    ``cos_theta`` accounts for the angle between force and motion. Use ``1``
    when force and motion point in the same direction.
    """

    return force_newtons_value * distance_m * cos_theta


def power_watts(work_joules_value: float, time_seconds: float) -> float:
    """Return power in watts using ``work / time``."""

    if time_seconds == 0:
        raise ValueError("time_seconds cannot be zero")
    return work_joules_value / time_seconds


def wave_speed_m_s(frequency_hz: float, wavelength_m: float) -> float:
    """Return wave speed using ``frequency * wavelength``."""

    return frequency_hz * wavelength_m


def frequency_hz(wave_speed_m_s_value: float, wavelength_m: float) -> float:
    """Return wave frequency using ``speed / wavelength``."""

    if wavelength_m == 0:
        raise ValueError("wavelength_m cannot be zero")
    return wave_speed_m_s_value / wavelength_m


def mass_energy_joules(mass_kg: float) -> float:
    """Return rest energy using ``E = mc^2``."""

    return mass_kg * SPEED_OF_LIGHT_M_S**2
