import pytest

from agromanch_ai.utils.dose import ACRE_TO_HA, acres_to_hectares, calculate_dose


def test_acres_to_hectares():
    assert acres_to_hectares(1) == round(ACRE_TO_HA, 4)
    assert acres_to_hectares(2.5) == round(2.5 * ACRE_TO_HA, 4)


def test_calculate_dose_totals():
    plan = calculate_dose(
        product="Test 5% SG",
        crop="rice",
        dose_per_ha=100.0,  # g/ha
        unit="g",
        area_ha=1.0,
        spray_volume_per_ha=500.0,
        tank_capacity_l=15.0,
    )
    assert plan.total_product == 100.0
    assert plan.total_water_l == 500.0
    # 500 L / 15 L per tank
    assert plan.tanks_needed == round(500 / 15, 2)
    # 100 g/ha over 500 L/ha -> per 15 L tank
    assert plan.product_per_tank == round(100 / 500 * 15, 2)


def test_calculate_dose_scales_with_area():
    plan = calculate_dose(
        product="X", crop="wheat", dose_per_ha=200.0, unit="ml",
        area_ha=2.0, spray_volume_per_ha=400.0, tank_capacity_l=16.0,
    )
    assert plan.total_product == 400.0
    assert plan.total_water_l == 800.0


def test_calculate_dose_rejects_bad_unit():
    with pytest.raises(ValueError):
        calculate_dose(product="X", crop="c", dose_per_ha=1, unit="kg",
                       area_ha=1, spray_volume_per_ha=500, tank_capacity_l=15)


@pytest.mark.parametrize("bad", [0, -1])
def test_calculate_dose_rejects_nonpositive(bad):
    with pytest.raises(ValueError):
        calculate_dose(product="X", crop="c", dose_per_ha=bad, unit="ml",
                       area_ha=1, spray_volume_per_ha=500, tank_capacity_l=15)


def test_dose_markdown_and_dict():
    plan = calculate_dose(product="Neem oil", crop="okra", dose_per_ha=3000,
                          unit="ml", area_ha=0.4, spray_volume_per_ha=500,
                          tank_capacity_l=15)
    assert "Neem oil" in plan.to_markdown()
    d = plan.to_dict()
    assert d["total_product"] == plan.total_product
    assert d["product_per_tank"] == plan.product_per_tank
