"""Offline agrochemical dose arithmetic.

Pure functions — no network, fully unit-tested — so the AgroManch app can do
dose math even when NotebookLM is unreachable. The *label values* (dose per
hectare, spray volume) should come from a registered product label; the
knowledge base lookup in ``examples/agromanch/pesticide_dose_calculator.py``
shows how to fetch them with citations.
"""

from __future__ import annotations

from agromanch_ai.models import DoseRecommendation

ACRE_TO_HA = 0.4047
BIGHA_TO_HA_DEFAULT = 0.25  # varies by state; overridable by caller


def acres_to_hectares(acres: float) -> float:
    return round(acres * ACRE_TO_HA, 4)


def calculate_dose(
    *,
    product: str,
    crop: str,
    dose_per_ha: float,
    unit: str,
    area_ha: float,
    spray_volume_per_ha: float = 500.0,
    tank_capacity_l: float = 15.0,
) -> DoseRecommendation:
    """Convert a label dose into field totals and per-tank amounts.

    Args:
        product: Trade/common name of the agrochemical.
        crop: Crop being treated (for the printout only).
        dose_per_ha: Label dose of formulated product per hectare.
        unit: "ml" for liquids, "g" for powders/granules.
        area_ha: Field size in hectares (use :func:`acres_to_hectares`).
        spray_volume_per_ha: Label water volume; 500 L/ha is a common
            high-volume knapsack figure for field crops.
        tank_capacity_l: Sprayer tank size (typical knapsack: 15–16 L).

    Raises:
        ValueError: If any numeric input is not positive or unit is unknown.
    """
    if unit not in ("ml", "g"):
        raise ValueError(f"unit must be 'ml' or 'g', got {unit!r}")
    for name, value in (
        ("dose_per_ha", dose_per_ha),
        ("area_ha", area_ha),
        ("spray_volume_per_ha", spray_volume_per_ha),
        ("tank_capacity_l", tank_capacity_l),
    ):
        if value <= 0:
            raise ValueError(f"{name} must be positive, got {value}")

    return DoseRecommendation(
        product=product,
        crop=crop,
        dose_per_ha=dose_per_ha,
        unit=unit,
        area_ha=area_ha,
        spray_volume_per_ha=spray_volume_per_ha,
        tank_capacity_l=tank_capacity_l,
    )
