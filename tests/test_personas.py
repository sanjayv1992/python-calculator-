from agromanch_ai.config import Settings
from agromanch_ai.personas import PERSONAS, get_persona, persona_directive


def test_all_expected_personas_present():
    for key in ("small_farmer", "large_farmer", "dairy_farmer", "vegetable_grower",
                "sugarcane_farmer", "organic_farmer", "dealer", "input_shop",
                "village_entrepreneur"):
        assert key in PERSONAS


def test_get_persona_falls_back_to_default():
    assert get_persona("nonexistent").key == "small_farmer"
    assert get_persona(None).key == "small_farmer"


def test_persona_directive_adapts():
    dairy = persona_directive("dairy_farmer")
    assert "Dairy Farmer" in dairy
    assert "milk" in dairy.lower()
    veg = persona_directive("vegetable_grower")
    assert dairy != veg


def test_settings_persona_directive_wired():
    s = Settings(persona="dairy_farmer")
    assert "Dairy Farmer" in s.persona_directive()


def test_settings_persona_from_env(monkeypatch):
    monkeypatch.setenv("AGROMANCH_PERSONA", "Organic_Farmer")
    assert Settings.from_env().persona == "organic_farmer"
