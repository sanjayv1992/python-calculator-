"""Campaign Engine — predefined agricultural content campaigns."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True, slots=True)
class Campaign:
    key: str
    name: str
    goal: str
    target_farmer: str
    kpis: tuple[str, ...]
    recommended_assets: tuple[str, ...]
    publishing_frequency: str
    months: tuple[int, ...] = field(default=())  # months this campaign is active
    categories: tuple[str, ...] = field(default=())


CAMPAIGNS: dict[str, Campaign] = {
    "rice_season": Campaign(
        "rice_season", "Rice Season", "help farmers grow a healthy paddy crop",
        "Small Farmer", ("reach", "saves", "WhatsApp shares"),
        ("instagram_carousel", "youtube_shorts_script", "whatsapp_broadcast", "reel_video_prompts"),
        "4-5 posts/week", months=(6, 7, 8, 9), categories=("crops", "crop_diseases", "insects")),
    "wheat_season": Campaign(
        "wheat_season", "Wheat Season", "support timely wheat sowing and care",
        "Small Farmer", ("reach", "saves", "watch time"),
        ("instagram_carousel", "blog", "youtube_shorts_script", "whatsapp_broadcast"),
        "4 posts/week", months=(10, 11, 12, 1, 2, 3), categories=("crops", "fertilizers", "weed_management")),
    "crop_doctor_awareness": Campaign(
        "crop_doctor_awareness", "Crop Doctor Awareness",
        "drive farmers to the Crop Doctor for diagnosis",
        "Vegetable Grower", ("WhatsApp messages", "app opens"),
        ("instagram_carousel", "reel_video_prompts", "whatsapp_broadcast", "cta"),
        "3 posts/week", months=tuple(range(1, 13)), categories=("crop_diseases", "insects")),
    "pashu_bazaar": Campaign(
        "pashu_bazaar", "Pashu Bazaar", "grow the livestock/dairy community",
        "Dairy Farmer", ("engagement", "shares"),
        ("instagram_carousel", "facebook_post", "whatsapp_broadcast"),
        "3 posts/week", months=tuple(range(1, 13)), categories=("animal_husbandry", "fisheries")),
    "government_schemes": Campaign(
        "government_schemes", "Government Schemes", "explain schemes and drive applications",
        "Small Farmer", ("saves", "shares", "app opens"),
        ("instagram_carousel", "blog", "whatsapp_broadcast", "cta"),
        "2-3 posts/week", months=tuple(range(1, 13)), categories=("government_schemes",)),
    "weather_alerts": Campaign(
        "weather_alerts", "Weather Alerts", "timely protective advisories",
        "Small Farmer", ("shares", "reach"),
        ("whatsapp_broadcast", "instagram_carousel", "reel_video_prompts"),
        "as needed (urgent)", months=tuple(range(1, 13)), categories=("weather",)),
    "festival_campaigns": Campaign(
        "festival_campaigns", "Festival Campaigns", "seasonal goodwill + reach",
        "Small Farmer", ("reach", "engagement"),
        ("instagram_carousel", "facebook_post", "story_prompt"),
        "around festivals", months=tuple(range(1, 13))),
}


def get_campaign(key: str) -> Campaign | None:
    return CAMPAIGNS.get(key)


def active_campaigns(today: date | None = None) -> list[Campaign]:
    """Campaigns active in the current month (season-driven)."""
    today = today or date.today()
    return [c for c in CAMPAIGNS.values() if not c.months or today.month in c.months]
