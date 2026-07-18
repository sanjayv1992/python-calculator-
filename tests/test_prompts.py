import pytest

from agromanch_ai.prompts import (
    ADVISORY_SPECS,
    CONTENT_SPECS,
    SPECS,
    PromptSpec,
    get_spec,
    list_templates,
    render,
    required_fields,
)


def test_registry_merges_both_groups():
    assert set(list_templates()) == set(ADVISORY_SPECS) | set(CONTENT_SPECS)


def test_the_15_bundle_items_exist():
    for name in (
        "research_summary", "instagram_carousel", "carousel_image_prompts",
        "facebook_post", "whatsapp_broadcast", "youtube_shorts_script",
        "veo_video_prompt", "voiceover_script", "subtitle_srt", "seo_keywords",
        "blog", "podcast_script", "thumbnail_prompt", "story_prompt", "cta",
    ):
        assert name in CONTENT_SPECS


def test_extra_creative_specs_exist():
    for name in ("hook", "image_prompt", "reel_video_prompts"):
        assert name in CONTENT_SPECS


def test_advisory_specs_exist():
    for name in ("crop_doctor", "pesticide_label", "govt_scheme", "farmer_qa"):
        assert name in ADVISORY_SPECS


_AUTO = dict(
    context_block="VERIFIED CONTEXT: rice needs water",
    language_name="English",
    brand_guide="BRAND GUIDE: pillars Emotional Hook, Practical Value, Local Context",
    language_directive="natural Hindi",
    target_region="Purvanchal and Bihar",
    seasonal_context="SEASONAL CONTEXT: July, Kharif",
    persona_directive="AUDIENCE PERSONA: Small Farmer",
    content_angle="CONTENT ANGLE: Save Money",
    competitor_inspiration="COMPETITOR INSPIRATION: borrow structure",
    learning_directive="LEARNING: prefer number hooks",
)


def test_render_returns_system_and_user():
    system, user = render("instagram_carousel", topic="rice irrigation", **_AUTO)
    assert "AgroManch" in system or "BRAND GUIDE" in system
    assert "rice irrigation" in user
    assert "Save Money" in user  # angle injected
    assert "{" not in system and "{" not in user


def test_render_missing_field_raises():
    with pytest.raises(ValueError):
        render("crop_doctor", topic="x", language_name="English", context_block="c")


def test_get_spec_unknown_raises():
    with pytest.raises(KeyError):
        get_spec("nope")


@pytest.mark.parametrize("name", sorted(SPECS))
def test_every_spec_renders_with_dummy_fields(name):
    fields = {f: f"<{f}>" for f in required_fields(name)}
    system, user = render(name, **fields)
    assert system and user
    assert "{" not in system and "{" not in user


@pytest.mark.parametrize("name", sorted(CONTENT_SPECS))
def test_content_specs_need_context_topic_language(name):
    assert {"context_block", "topic", "language_name"} <= required_fields(name)


@pytest.mark.parametrize("name", sorted(CONTENT_SPECS))
def test_content_specs_embed_brand_and_quality_fields(name):
    # The permanent brand system + season + angle are wired into every content spec.
    assert {"brand_guide", "language_directive", "target_region",
            "seasonal_context", "content_angle"} <= required_fields(name)


def test_brand_guide_carries_pillars():
    from agromanch_ai.prompts.brand import BRAND_GUIDE

    for pillar in ("Emotional Hook", "Practical Value", "Scientific Accuracy",
                   "Local Context", "Clear CTA", "Shareability", "Saveability"):
        assert pillar in BRAND_GUIDE


def test_promptspec_temperature_carried():
    assert isinstance(get_spec("hook"), PromptSpec)
    assert get_spec("research_summary").temperature == 0.3
