"""The AgroManch AI Content Factory pipeline.

`ContentFactory.produce` retrieves verified context **once** for a topic, then
generates the full multi-asset bundle from it (so every asset is grounded in the
same sources and stays consistent). `publish` lays the bundle out for one-click
publishing across Instagram, Facebook, YouTube Shorts, WhatsApp, and Telegram.
"""

from __future__ import annotations

import json
from pathlib import Path

from agromanch_ai.ai.generator import AgroManchGenerator
from agromanch_ai.analytics.performance import PerformanceTracker
from agromanch_ai.config import Settings
from agromanch_ai.intelligence.angle_generator import select_angles
from agromanch_ai.intelligence.competitor import competitor_inspiration
from agromanch_ai.logging import get_logger
from agromanch_ai.models import ContentBundle, VerifiedContext
from agromanch_ai.review.quality_manager import QualityManager
from agromanch_ai.utils.angles import angle_directive
from agromanch_ai.utils.quality_report import build_quality_report
from agromanch_ai.utils.text import safe_filename

logger = get_logger("factory")

# The 15-item bundle, in the exact order AgroManch requires, plus the extra
# standalone creative assets (hook, image/reel prompts).
DEFAULT_BUNDLE: tuple[str, ...] = (
    "research_summary",
    "instagram_carousel",
    "carousel_image_prompts",
    "facebook_post",
    "whatsapp_broadcast",
    "youtube_shorts_script",
    "veo_video_prompt",
    "voiceover_script",
    "subtitle_srt",
    "seo_keywords",
    "blog",
    "podcast_script",
    "thumbnail_prompt",
    "story_prompt",
    "cta",
    # Extra creative assets used across channels:
    "hook",
    "image_prompt",
    "reel_video_prompts",
)


class ContentFactory:
    """Produce and publish the full content bundle for a topic."""

    # Asset reviewed by the multi-agent Quality Manager (the package "hero").
    HERO_ASSET = "instagram_carousel"

    def __init__(
        self,
        generator: AgroManchGenerator,
        settings: Settings,
        *,
        tracker: PerformanceTracker | None = None,
    ) -> None:
        self._generator = generator
        self._settings = settings
        self._tracker = tracker

    async def produce(
        self,
        notebook_id: str,
        topic: str,
        *,
        items: tuple[str, ...] = DEFAULT_BUNDLE,
        require_grounding: bool | None = None,
        context: VerifiedContext | None = None,
        review: bool | None = None,
    ) -> ContentBundle:
        """Generate the whole bundle for ``topic`` from one verified context."""
        if context is None:
            logger.info("Retrieving verified context for %r", topic)
            context = await self._generator.get_context(notebook_id, topic)

        bundle = ContentBundle(
            topic=topic, context=context, language=self._settings.language
        )
        # Competitor Intelligence: one fresh primary+secondary angle for the whole
        # package (coherent, yet distinct from other packages on the same crop).
        angles = select_angles()
        bundle.angle = angles.primary
        angle_field = angle_directive(angles.primary)
        competitor_field = competitor_inspiration(angles)
        learning_field = self._tracker.directive() if self._tracker else ""

        for item in items:
            content = await self._generator.run(
                item,
                topic=topic,
                context=context,
                require_grounding=require_grounding,
                content_angle=angle_field,
                competitor_inspiration=competitor_field,
                learning_directive=learning_field,
            )
            bundle.items[item] = content
        logger.info(
            "Produced %d assets for %r (angle=%s)", len(bundle.items), topic, angles.primary
        )

        do_review = self._settings.review if review is None else review
        if do_review and self.HERO_ASSET in bundle.items:
            await self._review(bundle)

        bundle.learning_snapshot = self._learning_snapshot(bundle, angles, learning_field)
        return bundle

    async def _review(self, bundle: ContentBundle) -> None:
        """Multi-agent review + rewrite loop on the hero asset (Gemini-only)."""
        hero = bundle.items[self.HERO_ASSET]
        manager = QualityManager(self._generator.engine)
        outcome = await manager.review(
            kind=self.HERO_ASSET,
            content=hero.body,
            context_block=bundle.context.to_prompt_block(),
        )
        hero.body = outcome.content  # keep the best (possibly rewritten) version
        bundle.review_report = outcome.report.render()

    def _learning_snapshot(self, bundle, angles, learning_field) -> dict:
        """Explain why this package's creative choices were made (internal)."""
        return {
            "topic": bundle.topic,
            "primary_angle": angles.primary,
            "secondary_angle": angles.secondary,
            "why_angle": "selected for freshness vs. recent packages on this crop",
            "hook": "generated to the brand hook formulas for the primary angle",
            "cta": "app/WhatsApp CTA per brand guide",
            "hashtags": "15-20 mixed niche/broad/local per brand guide",
            "caption_style": "conversational village-Hindi, human, non-AI",
            "learning_directive": learning_field or "no performance history yet",
        }

    def publish(self, bundle: ContentBundle) -> Path:
        """Lay out the bundle for one-click multi-platform publishing.

        Writes: a markdown file per asset, per-platform folders linking the
        assets each platform uses, and a ``manifest.json`` handoff. Returns the
        bundle's root directory.
        """
        root = self._settings.ensure_output_dir() / safe_filename(bundle.topic)
        assets_dir = root / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        # One file per asset.
        for kind, content in bundle.items.items():
            (assets_dir / f"{kind}.md").write_text(
                content.to_markdown() + "\n", encoding="utf-8"
            )

        # Per-platform folders with a README pointing at the assets used.
        for platform, kinds in bundle.publishing_map().items():
            if not kinds:
                continue
            pdir = root / platform
            pdir.mkdir(parents=True, exist_ok=True)
            lines = [f"# {platform.replace('_', ' ').title()} — {bundle.topic}", ""]
            for kind in kinds:
                lines.append(f"## {kind.replace('_', ' ').title()}")
                lines.append("")
                lines.append(bundle.items[kind].body)
                lines.append("")
            (pdir / "post.md").write_text("\n".join(lines), encoding="utf-8")

        (root / "manifest.json").write_text(
            json.dumps(bundle.manifest(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # Internal-only reports — NOT placed in any per-platform public post.md.
        (root / "quality_report.txt").write_text(
            build_quality_report(bundle, self._settings), encoding="utf-8"
        )
        if bundle.review_report:
            (root / "review_report.txt").write_text(bundle.review_report, encoding="utf-8")
        if bundle.learning_snapshot is not None:
            (root / "learning_snapshot.json").write_text(
                json.dumps(bundle.learning_snapshot, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        logger.info("Published bundle to %s", root)
        return root
