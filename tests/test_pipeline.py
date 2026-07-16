import json

from agromanch_ai.ai.generator import AgroManchGenerator
from agromanch_ai.ai.pipeline import DEFAULT_BUNDLE, ContentFactory
from agromanch_ai.config import Settings
from conftest import FakeRetrieval


def make_factory(context, engine, tmp_path):
    settings = Settings(output_dir=tmp_path)
    generator = AgroManchGenerator(FakeRetrieval(context), engine, settings)
    return ContentFactory(generator, settings), settings


async def test_default_bundle_has_15_required_items():
    # The 15 numbered deliverables must all be in DEFAULT_BUNDLE, in order.
    required_order = [
        "research_summary", "instagram_carousel", "carousel_image_prompts",
        "facebook_post", "whatsapp_broadcast", "youtube_shorts_script",
        "veo_video_prompt", "voiceover_script", "subtitle_srt", "seo_keywords",
        "blog", "podcast_script", "thumbnail_prompt", "story_prompt", "cta",
    ]
    assert list(DEFAULT_BUNDLE)[:15] == required_order


async def test_produce_generates_all_items_once(grounded_context, fake_engine, tmp_path):
    factory, _ = make_factory(grounded_context, fake_engine, tmp_path)
    bundle = await factory.produce("nb1", "Fall Armyworm in maize")
    assert set(bundle.items) == set(DEFAULT_BUNDLE)
    # One Gemini call per item; context retrieved once (reused across items).
    assert len(fake_engine.calls) == len(DEFAULT_BUNDLE)


async def test_produce_reuses_single_context(grounded_context, fake_engine, tmp_path):
    retrieval = FakeRetrieval(grounded_context)
    settings = Settings(output_dir=tmp_path)
    factory = ContentFactory(
        AgroManchGenerator(retrieval, fake_engine, settings), settings
    )
    await factory.produce("nb1", "topic")
    assert len(retrieval.calls) == 1  # retrieved exactly once for the whole bundle


async def test_publish_writes_platform_folders_and_manifest(
    grounded_context, fake_engine, tmp_path
):
    factory, _ = make_factory(grounded_context, fake_engine, tmp_path)
    bundle = await factory.produce("nb1", "drip irrigation")
    root = factory.publish(bundle)

    assert (root / "manifest.json").exists()
    assert (root / "assets" / "instagram_carousel.md").exists()
    for platform in ("instagram", "facebook", "youtube_shorts", "whatsapp", "telegram"):
        assert (root / platform / "post.md").exists(), platform

    manifest = json.loads((root / "manifest.json").read_text())
    assert manifest["topic"] == "drip irrigation"
    assert manifest["grounded"] is True
    assert set(manifest["publishing"]) == {
        "instagram", "facebook", "youtube_shorts", "whatsapp", "telegram"
    }
    assert "instagram_carousel" in manifest["items"]


async def test_publishing_map_only_includes_present_items(
    grounded_context, fake_engine, tmp_path
):
    factory, _ = make_factory(grounded_context, fake_engine, tmp_path)
    bundle = await factory.produce("nb1", "t", items=("instagram_carousel", "cta"))
    pmap = bundle.publishing_map()
    assert pmap["instagram"] == ["instagram_carousel", "cta"]
    assert pmap["whatsapp"] == ["cta"]
    assert pmap["youtube_shorts"] == ["cta"]
