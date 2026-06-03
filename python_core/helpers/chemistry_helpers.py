"""Common chemistry calculation helpers.

These formulas are for common classroom, lab, and application estimates. Keep
units explicit in function names to avoid subtle conversion bugs.
"""

from __future__ import annotations

from math import log10

GAS_CONSTANT_L_ATM = 0.082057366


def moles_from_mass(mass_g: float, molar_mass_g_mol: float) -> float:
    """Return moles using ``mass / molar_mass``."""

    if molar_mass_g_mol == 0:
        raise ValueError("molar_mass_g_mol cannot be zero")
    return mass_g / molar_mass_g_mol


def mass_from_moles(moles: float, molar_mass_g_mol: float) -> float:
    """Return mass in grams using ``moles * molar_mass``."""

    return moles * molar_mass_g_mol


def molarity(moles_solute: float, liters_solution: float) -> float:
    """Return molarity in mol/L using ``moles / liters``."""

    if liters_solution == 0:
        raise ValueError("liters_solution cannot be zero")
    return moles_solute / liters_solution


def moles_from_molarity(molarity_mol_l: float, liters_solution: float) -> float:
    """Return moles from molarity and solution volume."""

    return molarity_mol_l * liters_solution


def dilution_c1v1(
    initial_concentration: float,
    initial_volume: float,
    final_volume: float,
) -> float:
    """Return final concentration using the dilution relationship ``C1V1 = C2V2``."""

    if final_volume == 0:
        raise ValueError("final_volume cannot be zero")
    return initial_concentration * initial_volume / final_volume


def ideal_gas_pressure_atm(moles: float, temperature_k: float, volume_liters: float) -> float:
    """Return ideal gas pressure in atmospheres using ``PV = nRT``."""

    if volume_liters == 0:
        raise ValueError("volume_liters cannot be zero")
    return moles * GAS_CONSTANT_L_ATM * temperature_k / volume_liters


def ideal_gas_volume_liters(moles: float, temperature_k: float, pressure_atm: float) -> float:
    """Return ideal gas volume in liters using ``PV = nRT``."""

    if pressure_atm == 0:
        raise ValueError("pressure_atm cannot be zero")
    return moles * GAS_CONSTANT_L_ATM * temperature_k / pressure_atm


def ph_from_hydrogen_concentration(hydrogen_mol_l: float) -> float:
    """Return pH from hydrogen ion concentration using ``-log10([H+])``."""

    if hydrogen_mol_l <= 0:
        raise ValueError("hydrogen_mol_l must be positive")
    return -log10(hydrogen_mol_l)


def hydrogen_concentration_from_ph(ph_value: float) -> float:
    """Return hydrogen ion concentration from pH using ``10 ** -pH``."""

    return 10**(-ph_value)


def percent_yield(actual_yield: float, theoretical_yield: float) -> float:
    """Return percent yield using ``actual / theoretical * 100``."""

    if theoretical_yield == 0:
        raise ValueError("theoretical_yield cannot be zero")
    return actual_yield / theoretical_yield * 100


def ppm_from_mass(solute_mass_mg: float, solution_mass_kg: float) -> float:
    """Return parts per million as ``mg solute / kg solution``."""

    if solution_mass_kg == 0:
        raise ValueError("solution_mass_kg cannot be zero")
    return solute_mass_mg / solution_mass_kg


def remaining_fraction_after_half_lives(half_lives: float) -> float:
    """Return remaining fraction after radioactive or chemical half-lives."""

    return 0.5**half_lives


def serial_dilution_concentration(
    starting_concentration: float,
    dilution_factor: float,
    steps: int,
) -> float:
    """Return concentration after repeated equal dilution steps."""

    if dilution_factor == 0:
        raise ValueError("dilution_factor cannot be zero")
    return starting_concentration / dilution_factor**steps
