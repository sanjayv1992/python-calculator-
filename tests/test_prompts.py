import pytest

from agromanch_ai.prompts import PROMPTS, list_templates, render, required_fields
from agromanch_ai.prompts.advisory_prompts import ADVISORY_PROMPTS
from agromanch_ai.prompts.content_prompts import CONTENT_PROMPTS


def test_registry_merges_both_groups():
    assert set(list_templates()) == set(ADVISORY_PROMPTS) | set(CONTENT_PROMPTS)


def test_expected_templates_present():
    for name in ("crop_doctor", "pesticide_dose", "instagram_carousel",
                 "whatsapp_broadcast", "youtube_shorts_script", "faq"):
        assert name in PROMPTS


def test_render_fills_fields():
    out = render(
        "crop_doctor",
        crop="tomato",
        region="Maharashtra",
        symptoms="leaf curl",
        language_name="English",
    )
    assert "tomato" in out and "Maharashtra" in out and "leaf curl" in out
    assert "{" not in out  # no unresolved placeholders


def test_render_missing_field_raises():
    with pytest.raises(ValueError):
        render("crop_doctor", crop="tomato")


def test_render_unknown_template_raises():
    with pytest.raises(KeyError):
        render("does_not_exist", topic="x")


@pytest.mark.parametrize("name", sorted(PROMPTS))
def test_every_template_renders_with_dummy_fields(name):
    fields = {f: f"<{f}>" for f in required_fields(name)}
    out = render(name, **fields)
    assert out
    assert "{" not in out


@pytest.mark.parametrize("name", sorted(CONTENT_PROMPTS))
def test_content_templates_require_topic_and_language(name):
    assert {"topic", "language_name"} <= required_fields(name)
