from datetime import date

from agromanch_ai.utils.seasonal import KHARIF, RABI, season_info, seasonal_context


def test_july_is_kharif_paddy_faw():
    info = season_info(date(2026, 7, 15))
    assert info.season == KHARIF
    assert "paddy" in info.crops.lower()
    assert "armyworm" in info.pests.lower()


def test_october_wheat_prep():
    ctx = seasonal_context(date(2026, 10, 10))
    assert "WHEAT PREPARATION" in ctx or "wheat prep" in ctx.lower()


def test_march_wheat_harvest_rabi():
    info = season_info(date(2026, 3, 20))
    assert info.season == RABI
    assert "harvest" in info.activities.lower()


def test_june_monsoon_prep():
    ctx = seasonal_context(date(2026, 6, 5))
    assert "MONSOON PREPARATION" in ctx or "monsoon" in ctx.lower()


def test_seasonal_context_mentions_month_and_directive():
    ctx = seasonal_context(date(2026, 1, 1))
    assert "January" in ctx
    assert "in-season" in ctx.lower() or "this time of year" in ctx.lower()
