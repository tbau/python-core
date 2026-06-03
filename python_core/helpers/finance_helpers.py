"""Finance and business calculation helpers.

Rates are decimals, so pass ``0.05`` for five percent. These helpers are for
planning and examples, not regulatory financial advice.
"""

from __future__ import annotations


def simple_interest(principal: float, annual_rate: float, years: float) -> float:
    """Return interest earned using ``principal * annual_rate * years``."""

    return principal * annual_rate * years


def compound_interest(principal: float, annual_rate: float, periods_per_year: int, years: float) -> float:
    """Return ending balance after compounding interest."""

    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    return principal * (1 + annual_rate / periods_per_year) ** (periods_per_year * years)


def future_value(present_value: float, rate_per_period: float, periods: int) -> float:
    """Return future value for a lump sum after repeated growth periods."""

    return present_value * (1 + rate_per_period) ** periods


def present_value(future_value_amount: float, rate_per_period: float, periods: int) -> float:
    """Return today's value of a future lump sum discounted by rate."""

    return future_value_amount / (1 + rate_per_period) ** periods


def amortized_payment(principal: float, annual_rate: float, years: int, payments_per_year: int = 12) -> float:
    """Return recurring payment for an amortized loan."""

    periods = years * payments_per_year
    if periods <= 0:
        raise ValueError("loan must have at least one payment period")
    rate = annual_rate / payments_per_year
    if rate == 0:
        return principal / periods
    return principal * rate * (1 + rate) ** periods / ((1 + rate) ** periods - 1)


def gross_margin_percent(revenue: float, cost: float) -> float:
    """Return gross margin percentage using ``(revenue - cost) / revenue``."""

    if revenue == 0:
        raise ValueError("revenue cannot be zero")
    return (revenue - cost) / revenue * 100


def markup_percent(cost: float, price: float) -> float:
    """Return markup percentage using ``(price - cost) / cost``."""

    if cost == 0:
        raise ValueError("cost cannot be zero")
    return (price - cost) / cost * 100


def break_even_units(fixed_costs: float, price_per_unit: float, variable_cost_per_unit: float) -> float:
    """Return units required to cover fixed costs."""

    contribution_margin = price_per_unit - variable_cost_per_unit
    if contribution_margin <= 0:
        raise ValueError("price_per_unit must exceed variable_cost_per_unit")
    return fixed_costs / contribution_margin


def annual_rate_to_period_rate(annual_rate: float, periods_per_year: int) -> float:
    """Convert an annual rate into a per-period rate."""

    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    return annual_rate / periods_per_year
