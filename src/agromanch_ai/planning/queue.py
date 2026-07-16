"""Intelligent Publishing Queue — prioritise what to publish next.

Deterministic priority scoring from seasonal urgency, government/weather alerts,
viral potential, and knowledge confidence; recommends platforms per item.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agromanch_ai.planning.planner import PlanItem

_ALERT_WORDS = ("alert", "warning", "urgent", "scheme", "deadline", "weather", "rain", "frost")
_PEST_WORDS = ("armyworm", "blight", "borer", "aphid", "disease", "pest", "blast")

# Which platforms suit which content format.
_FORMAT_PLATFORMS = {
    "instagram_carousel": ["instagram", "facebook"],
    "reel_video_prompts": ["instagram", "youtube_shorts"],
    "youtube_shorts_script": ["youtube_shorts", "instagram"],
    "whatsapp_broadcast": ["whatsapp", "telegram"],
    "facebook_post": ["facebook"],
    "blog": ["telegram", "facebook"],
    "story_prompt": ["instagram"],
    "cta": ["whatsapp", "instagram"],
}


def _score(item: PlanItem, knowledge_confidence: float) -> int:
    topic = item.topic.lower()
    score = 40  # base
    if any(w in topic or w in item.campaign.lower() for w in _ALERT_WORDS):
        score += 30  # government/weather urgency
    if any(w in topic for w in _PEST_WORDS):
        score += 20  # timely pest pressure = viral potential
    score += int(20 * max(0.0, min(1.0, knowledge_confidence)))  # grounding confidence
    # Higher-priority calendar items rise.
    return min(100, score)


def recommend_platforms(content_format: str) -> list[str]:
    return _FORMAT_PLATFORMS.get(content_format, ["instagram", "whatsapp"])


def build_publishing_queue(
    items: list[PlanItem],
    *,
    knowledge_confidence: float = 1.0,
    path: Path | str | None = "data/publishing_queue.json",
) -> list[dict[str, Any]]:
    """Score + sort items into a publishing queue; optionally write JSON."""
    scored = []
    for item in items:
        scored.append(
            {
                "date": item.date,
                "topic": item.topic,
                "crop": item.crop,
                "campaign": item.campaign,
                "content_format": item.content_format,
                "priority_score": _score(item, knowledge_confidence),
                "recommend_platforms": recommend_platforms(item.content_format),
            }
        )
    scored.sort(key=lambda e: (-e["priority_score"], e["date"]))
    if path is not None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(scored, ensure_ascii=False, indent=2), encoding="utf-8")
    return scored
