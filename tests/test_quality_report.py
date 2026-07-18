from agromanch_ai.config import Settings
from agromanch_ai.models import (
    ContentBundle,
    GeneratedContent,
    SourceRef,
    VerifiedContext,
)
from agromanch_ai.utils.quality_report import build_quality_report


def _bundle(grounded: bool) -> ContentBundle:
    ctx = VerifiedContext(
        topic="rice blb",
        context_text="facts" if grounded else "",
        references=[SourceRef("s1", 1, "Rice BLB")] if grounded else [],
        grounded=grounded,
    )
    bundle = ContentBundle(topic="rice blb", context=ctx, angle="Save Money")
    for kind in ("research_summary", "instagram_carousel", "youtube_shorts_script",
                 "whatsapp_broadcast", "blog", "seo_keywords", "cta", "hook"):
        bundle.items[kind] = GeneratedContent(kind=kind, topic="rice blb", body="x")
    return bundle


def test_report_grounded_sections_and_score():
    report = build_quality_report(_bundle(True), Settings())
    assert "CONTENT QUALITY REPORT" in report
    assert "Grounding Status: Verified" in report
    assert "Verified Sources Used: 1" in report
    for section in ("Scientific Accuracy", "SEO Quality", "Instagram Potential",
                    "WhatsApp Shareability", "YouTube Watch Potential",
                    "Recommended Reel Duration", "Overall Content Score"):
        assert section in report
    # complete + grounded → strong overall
    line = [l for l in report.splitlines() if l.startswith("Overall Content Score")][0]
    score = int(line.split(":")[1].strip().split("/")[0])
    assert 85 <= score <= 100


def test_report_unverified_lower_score():
    report = build_quality_report(_bundle(False), Settings())
    assert "Grounding Status: Unverified" in report
    line = [l for l in report.splitlines() if l.startswith("Overall Content Score")][0]
    score = int(line.split(":")[1].strip().split("/")[0])
    assert score < 85


def test_report_marketing_angle_shown():
    report = build_quality_report(_bundle(True), Settings())
    assert "Save Money" in report
