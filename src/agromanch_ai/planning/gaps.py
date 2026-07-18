"""Content Gap Analyzer — what should we create next?

Compares the Knowledge Library, editorial calendar, performance history and
campaign goals to surface missing crops, categories, regions and personas, and
recommends next topics. Deterministic; no LLM.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from agromanch_ai.knowledge.schema import Category
from agromanch_ai.personas import PERSONAS
from agromanch_ai.planning.calendar import EditorialCalendar

# Priority crops for the target region we want covered.
PRIORITY_CROPS = ("rice", "wheat", "maize", "sugarcane", "mustard", "potato",
                  "pigeonpea", "vegetables")


@dataclass(slots=True)
class GapReport:
    missing_categories: list[str] = field(default_factory=list)
    missing_crops: list[str] = field(default_factory=list)
    missing_personas: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "missing_categories": self.missing_categories,
            "missing_crops": self.missing_crops,
            "missing_personas": self.missing_personas,
            "recommendations": self.recommendations,
        }


def analyze_gaps(
    catalog_entries: list[dict],
    calendar: EditorialCalendar | None = None,
    *,
    covered_personas: set[str] | None = None,
) -> GapReport:
    """Find coverage gaps across categories, crops and personas."""
    covered_categories = {e.get("category", "") for e in catalog_entries}
    missing_categories = [c for c in Category.folders() if c not in covered_categories]

    covered_crops = {(e.get("crop") or "").lower() for e in catalog_entries}
    if calendar:
        covered_crops |= {(e.crop or "").lower() for e in calendar.entries}
    missing_crops = [c for c in PRIORITY_CROPS if c not in covered_crops]

    covered_personas = covered_personas or set()
    missing_personas = [p for p in PERSONAS if p not in covered_personas]

    recommendations: list[str] = []
    for cat in missing_categories[:5]:
        recommendations.append(f"Add knowledge + content for category: {cat}")
    for crop in missing_crops[:5]:
        recommendations.append(f"Create a content package for crop: {crop}")
    for persona in missing_personas[:3]:
        recommendations.append(f"Produce a package targeting persona: {persona}")

    return GapReport(
        missing_categories=missing_categories,
        missing_crops=missing_crops,
        missing_personas=missing_personas,
        recommendations=recommendations,
    )
