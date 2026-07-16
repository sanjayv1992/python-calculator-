"""Internal Content Quality & Confidence Report.

Rule-based and deterministic — no extra Gemini call. Reads the finished
``ContentBundle`` and grades it against a transparent rubric so a reviewer can
judge publish-readiness at a glance. Internal only: never placed in the public
per-platform output.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from agromanch_ai.config import Settings

if TYPE_CHECKING:  # pragma: no cover - typing only
    from agromanch_ai.models import ContentBundle

# Assets that signal a complete, publish-ready package.
_KEY_ASSETS = (
    "research_summary", "instagram_carousel", "youtube_shorts_script",
    "whatsapp_broadcast", "blog", "seo_keywords", "cta", "hook",
)


def _band(score: float, high: float, med: float) -> str:
    return "High" if score >= high else ("Medium" if score >= med else "Low")


def _completeness(bundle: "ContentBundle") -> float:
    present = sum(1 for k in _KEY_ASSETS if k in bundle.items and bundle.items[k].body.strip())
    return present / len(_KEY_ASSETS)


def build_quality_report(bundle: "ContentBundle", settings: Settings) -> str:
    """Render the internal quality report for a produced bundle."""
    ctx = bundle.context
    grounded = ctx.grounded and not ctx.is_empty
    n_sources = len(ctx.references)
    completeness = _completeness(bundle)

    # Deterministic 0–10 sub-scores from grounding, sources, and completeness.
    sci = 10.0 if grounded else 4.0
    if grounded and n_sources == 0:
        sci = 7.0
    seo = round(6.0 + 4.0 * completeness, 1)
    readability = "Excellent" if completeness >= 0.8 else ("Good" if completeness >= 0.5 else "Average")

    ig = _band(completeness, 0.8, 0.5)
    fb = _band(completeness, 0.75, 0.45)
    wa = _band(completeness, 0.7, 0.4)
    yt = _band(completeness, 0.8, 0.5)

    # Overall /100: grounding 40, completeness 45, sources 15.
    overall = round(
        (40 if grounded else 15)
        + 45 * completeness
        + min(15, n_sources * 5)
    )

    recommendation = (
        "Ready for Publishing" if overall >= 85 and grounded
        else "Review Before Publishing" if overall >= 65
        else "Needs Grounding / More Work"
    )

    lines = [
        "=" * 40,
        "CONTENT QUALITY REPORT (internal only)",
        "=" * 40,
        f"Topic: {bundle.topic}",
        f"Marketing Angle: {bundle.angle or 'n/a'}",
        f"Language: {settings.language_name}",
        f"Region: {settings.region}",
        "",
        f"Research Confidence: {_band(1.0 if grounded else 0.0, 0.9, 0.4)}",
        f"Verified Sources Used: {n_sources}",
        f"Grounding Status: {'Verified' if grounded else 'Unverified'}",
        f"Scientific Accuracy: {sci:.0f}/10",
        f"SEO Quality: {seo:.1f}/10",
        f"Instagram Potential: {ig}",
        f"Facebook Engagement: {fb}",
        f"WhatsApp Shareability: {wa}",
        f"YouTube Watch Potential: {yt}",
        f"Farmer Readability: {readability}",
        "Target Audience: Small Farmers",
        "",
        "Recommended Publishing Time: 6-8 AM or 7-9 PM (farmer active hours)",
        "Recommended Platforms: Instagram, WhatsApp, YouTube Shorts, Facebook, Telegram",
        "Recommended Thumbnail Style: bold 3-4 word overlay, real farmer, high contrast",
        "Recommended CTA: message AgroManch on WhatsApp for personalised advice",
        "Recommended Hashtags Count: 15-20",
        "Recommended Reel Duration: 20-30 seconds",
        "",
        f"Overall Content Score: {overall}/100",
        f"Recommendation: {recommendation}",
        "=" * 40,
        "",
    ]
    return "\n".join(lines)
