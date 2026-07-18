"""Evergreen Content Library — classify assets by shelf life / type."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

EVERGREEN = "Evergreen"
SEASONAL = "Seasonal"
BREAKING = "Breaking"
GOVT_UPDATE = "Government Update"
WEATHER_ALERT = "Weather Alert"
EDUCATIONAL = "Educational"
REFERENCE = "Reference Guide"

_WEATHER = ("weather", "rain", "frost", "flood", "monsoon", "heatwave")
_GOVT = ("scheme", "subsidy", "pm-kisan", "pmfby", "government", "yojana")
_SEASONAL = ("season", "sowing", "harvest", "transplant", "nursery", "kharif", "rabi")
_REFERENCE = ("guide", "how to", "step-by-step", "dose", "calendar", "package of practices")


def classify_asset(topic: str, *, category: str = "") -> str:
    """Classify an asset by topic/category for the reusable library."""
    t = f"{topic} {category}".lower()
    if any(w in t for w in _WEATHER):
        return WEATHER_ALERT
    if any(w in t for w in _GOVT):
        return GOVT_UPDATE
    if any(w in t for w in _REFERENCE):
        return REFERENCE
    if any(w in t for w in _SEASONAL):
        return SEASONAL
    if category in ("crops", "soil_health", "irrigation", "organic_farming"):
        return EVERGREEN
    return EDUCATIONAL


def is_reusable(classification: str) -> bool:
    """Evergreen/reference/educational content is reusable across seasons."""
    return classification in (EVERGREEN, REFERENCE, EDUCATIONAL)


@dataclass(slots=True)
class EvergreenStore:
    path: Path = Path("data/evergreen_library.json")

    def add(self, topic: str, classification: str) -> None:
        items = self.load()
        items.append({"topic": topic, "classification": classification})
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text("utf-8"))
