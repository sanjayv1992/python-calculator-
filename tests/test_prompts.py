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


def test_render_returns_system_and_user():
    system, user = render(
        "instagram_carousel",
        context_block="VERIFIED CONTEXT: rice needs water",
        topic="rice irrigation",
        language_name="English",
    )
    assert "AgroManch" in system
    assert "rice irrigation" in user
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


def test_promptspec_temperature_carried():
    assert isinstance(get_spec("hook"), PromptSpec)
    assert get_spec("research_summary").temperature == 0.3
