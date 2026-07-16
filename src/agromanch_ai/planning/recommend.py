"""Intelligent Recommendation Layer — pre-generation recommendations.

Combines Seasonal Intelligence, Performance Learning and active campaigns to
recommend the best format, hook style, publishing time, CTA, hashtag count and
campaign for a topic. Deterministic; no LLM.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from typing import Any

from agromanch_ai.analytics.learning import Preferences
from agromanch_ai.planning.campaign import active_campaigns
from agromanch_ai.planning.queue import recommend_platforms
from agromanch_ai.utils.seasonal import season_info

# Farmer-active windows for publishing.
_MORNING = "06:30-08:00 (before farmers head to the field)"
_EVENING = "19:00-21:00 (after the day's work)"


@dataclass(slots=True)
class Recommendation:
    topic: str
    best_format: str
    best_hook_style: str
    best_publishing_time: str
    best_cta: str
    best_hashtags_count: int
    best_campaign: str
    platforms: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def recommend(
    topic: str,
    *,
    prefs: Preferences | None = None,
    today: date | None = None,
) -> Recommendation:
    today = today or date.today()
    prefs = prefs or Preferences()
    info = season_info(today)

    # Timely pest/scheme/weather topics do best as short video/broadcast.
    t = topic.lower()
    if any(w in t for w in ("armyworm", "blight", "borer", "pest", "disease")):
        best_format = "reel_video_prompts"
    elif any(w in t for w in ("scheme", "subsidy", "yojana")):
        best_format = "whatsapp_broadcast"
    else:
        best_format = "instagram_carousel"

    best_hook_style = prefs.hook_style or "curiosity + local proof"
    best_cta = prefs.cta or "message AgroManch on WhatsApp for personalised advice"
    best_hashtags = int(prefs.hashtags_count) if str(prefs.hashtags_count).isdigit() else 18

    # Pick the most relevant active campaign for the topic.
    campaigns = active_campaigns(today)
    best_campaign = ""
    for c in campaigns:
        if any(cat in t for cat in ("rice",) if c.key == "rice_season"):
            best_campaign = c.name
            break
    if not best_campaign and campaigns:
        best_campaign = campaigns[0].name

    publishing_time = _EVENING if best_format in ("reel_video_prompts", "youtube_shorts_script") else _MORNING

    return Recommendation(
        topic=topic,
        best_format=best_format,
        best_hook_style=best_hook_style,
        best_publishing_time=publishing_time,
        best_cta=best_cta,
        best_hashtags_count=best_hashtags,
        best_campaign=best_campaign,
        platforms=recommend_platforms(best_format),
    )
