"""Common unit conversion helpers.

Function names state the source and target units so call sites stay readable.
"""

from __future__ import annotations


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""

    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""

    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin."""

    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""

    return kelvin - 273.15


def miles_to_kilometers(miles: float) -> float:
    """Convert miles to kilometers."""

    return miles * 1.609344


def kilometers_to_miles(kilometers: float) -> float:
    """Convert kilometers to miles."""

    return kilometers / 1.609344


def pounds_to_kilograms(pounds: float) -> float:
    """Convert pounds to kilograms."""

    return pounds * 0.45359237


def kilograms_to_pounds(kilograms: float) -> float:
    """Convert kilograms to pounds."""

    return kilograms / 0.45359237


def inches_to_centimeters(inches: float) -> float:
    """Convert inches to centimeters."""

    return inches * 2.54


def centimeters_to_inches(centimeters: float) -> float:
    """Convert centimeters to inches."""

    return centimeters / 2.54


def gallons_to_liters(gallons: float) -> float:
    """Convert US gallons to liters."""

    return gallons * 3.785411784


def liters_to_gallons(liters: float) -> float:
    """Convert liters to US gallons."""

    return liters / 3.785411784


def psi_to_kilopascals(psi: float) -> float:
    """Convert pounds per square inch to kilopascals."""

    return psi * 6.8947572932


def kilopascals_to_psi(kilopascals: float) -> float:
    """Convert kilopascals to pounds per square inch."""

    return kilopascals / 6.8947572932


def miles_per_hour_to_meters_per_second(mph: float) -> float:
    """Convert mph to m/s."""

    return mph * 0.44704


def meters_per_second_to_miles_per_hour(meters_per_second: float) -> float:
    """Convert m/s to mph."""

    return meters_per_second / 0.44704
