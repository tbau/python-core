"""Electrical engineering calculation helpers.

Functions use volts, amps, ohms, farads, henrys, hertz, watts, and seconds
unless the name says otherwise.
"""

from __future__ import annotations

from math import pi, sqrt


def ohms_law_voltage(current_amps: float, resistance_ohms: float) -> float:
    """Return voltage using Ohm's law: ``V = I * R``."""

    return current_amps * resistance_ohms


def ohms_law_current(voltage_volts: float, resistance_ohms: float) -> float:
    """Return current using Ohm's law: ``I = V / R``."""

    if resistance_ohms == 0:
        raise ValueError("resistance_ohms cannot be zero")
    return voltage_volts / resistance_ohms


def ohms_law_resistance(voltage_volts: float, current_amps: float) -> float:
    """Return resistance using Ohm's law: ``R = V / I``."""

    if current_amps == 0:
        raise ValueError("current_amps cannot be zero")
    return voltage_volts / current_amps


def power_from_voltage_current(voltage_volts: float, current_amps: float) -> float:
    """Return electrical power using ``P = V * I``."""

    return voltage_volts * current_amps


def power_from_current_resistance(current_amps: float, resistance_ohms: float) -> float:
    """Return power using ``P = I^2 * R``."""

    return current_amps**2 * resistance_ohms


def power_from_voltage_resistance(voltage_volts: float, resistance_ohms: float) -> float:
    """Return power using ``P = V^2 / R``."""

    if resistance_ohms == 0:
        raise ValueError("resistance_ohms cannot be zero")
    return voltage_volts**2 / resistance_ohms


def series_resistance(resistances_ohms: list[float]) -> float:
    """Return equivalent resistance for resistors in series.

    Series resistances simply add together.
    """

    return sum(resistances_ohms)


def parallel_resistance(resistances_ohms: list[float]) -> float:
    """Return equivalent resistance for resistors in parallel.

    Parallel resistance uses the reciprocal sum. A zero-ohm branch shorts the
    network, so the equivalent resistance is zero.
    """

    if any(resistance == 0 for resistance in resistances_ohms):
        return 0.0
    reciprocal_sum = sum(1 / resistance for resistance in resistances_ohms)
    if reciprocal_sum == 0:
        raise ValueError("parallel resistance cannot be calculated from these values")
    return 1 / reciprocal_sum


def voltage_divider_output(
    input_voltage: float,
    top_resistance_ohms: float,
    bottom_resistance_ohms: float,
) -> float:
    """Return output voltage for a two-resistor divider."""

    total = top_resistance_ohms + bottom_resistance_ohms
    if total == 0:
        raise ValueError("total resistance cannot be zero")
    return input_voltage * bottom_resistance_ohms / total


def capacitive_reactance_ohms(frequency_hz: float, capacitance_farads: float) -> float:
    """Return capacitive reactance using ``1 / (2*pi*f*C)``."""

    if frequency_hz == 0 or capacitance_farads == 0:
        raise ValueError("frequency_hz and capacitance_farads cannot be zero")
    return 1 / (2 * pi * frequency_hz * capacitance_farads)


def inductive_reactance_ohms(frequency_hz: float, inductance_henrys: float) -> float:
    """Return inductive reactance using ``2*pi*f*L``."""

    return 2 * pi * frequency_hz * inductance_henrys


def rc_time_constant_seconds(resistance_ohms: float, capacitance_farads: float) -> float:
    """Return RC circuit time constant using ``R * C``."""

    return resistance_ohms * capacitance_farads


def rms_voltage(peak_voltage: float) -> float:
    """Return RMS voltage for a sine wave from peak voltage."""

    return peak_voltage / sqrt(2)


def peak_voltage(rms_voltage_value: float) -> float:
    """Return peak voltage for a sine wave from RMS voltage."""

    return rms_voltage_value * sqrt(2)
