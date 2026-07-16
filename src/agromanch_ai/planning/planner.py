"""Content Strategy Planner — builds 7 / 30 / 90-day plans.

Deterministic: given the same start date, region and inputs, it always produces
the same plan. Combines seasonal intelligence, the crop calendar, active
campaigns, and (optionally) the knowledge catalog and performance history.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, timedelta
from typing import Any

from agromanch_ai.planning.campaign import Campaign, active_campaigns
from agromanch_ai.utils.angles import ANGLES
from agromanch_ai.utils.seasonal import season_info

_PLATFORMS = ("instagram", "youtube_shorts", "whatsapp", "facebook", "telegram")


@dataclass(slots=True)
class PlanItem:
    date: str
    topic: str
    crop: str
    target_audience: str
    goal: str
    platform: str
    content_format: str
    best_cta: str
    campaign: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _topic_pool(today: date) -> list[tuple[str, str]]:
    """(crop, topic) candidates derived from the season, most-timely first."""
    info = season_info(today)
    crops = [c.strip() for c in info.crops.split(",") if c.strip()]
    pests = [p.strip() for p in info.pests.split(",") if p.strip()]
    activities = [a.strip() for a in info.activities.split(",") if a.strip()]
    pool: list[tuple[str, str]] = []
    # Pest/disease pressure is the most timely, actionable content.
    for pest in pests:
        crop = crops[0] if crops else "your crop"
        pool.append((crop, f"{pest} — identify and manage in {crop}"))
    for act in activities:
        crop = crops[0] if crops else ""
        pool.append((crop, f"{act.capitalize()} the right way this {info.season.split()[0]}"))
    for crop in crops:
        pool.append((crop, f"Key practices for a healthy {crop} crop now"))
    return pool or [("", "Seasonal farming tips")]


class ContentPlanner:
    """Builds a day-by-day content plan."""

    def __init__(self, persona: str = "small_farmer") -> None:
        self._persona = persona

    def build_plan(
        self, days: int, *, start: date | None = None, region: str = ""
    ) -> list[PlanItem]:
        start = start or date.today()
        campaigns = active_campaigns(start) or list(active_campaigns(start))
        plan: list[PlanItem] = []

        for i in range(days):
            day = start + timedelta(days=i)
            pool = _topic_pool(day)
            crop, base_topic = pool[i % len(pool)]
            # Differentiate when the pool repeats across a long horizon.
            angle = ANGLES[i % len(ANGLES)]
            topic = base_topic if i < len(pool) else f"{base_topic} ({angle})"

            campaign: Campaign | None = campaigns[i % len(campaigns)] if campaigns else None
            assets = campaign.recommended_assets if campaign else ("instagram_carousel",)
            plan.append(
                PlanItem(
                    date=day.isoformat(),
                    topic=topic,
                    crop=crop,
                    target_audience=(campaign.target_farmer if campaign else "Small Farmer"),
                    goal=(campaign.goal if campaign else "educate and grow reach"),
                    platform=_PLATFORMS[i % len(_PLATFORMS)],
                    content_format=assets[i % len(assets)],
                    best_cta="message AgroManch on WhatsApp for personalised advice",
                    campaign=(campaign.name if campaign else ""),
                )
            )
        return plan

    def plan_7_day(self, **kw) -> list[PlanItem]:
        return self.build_plan(7, **kw)

    def plan_30_day(self, **kw) -> list[PlanItem]:
        return self.build_plan(30, **kw)

    def plan_90_day(self, **kw) -> list[PlanItem]:
        return self.build_plan(90, **kw)
