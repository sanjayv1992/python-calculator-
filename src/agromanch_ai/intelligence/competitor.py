"""Assemble the competitor-inspiration prompt block (structure only).

Maps the chosen marketing angles to viral-format structures from the trend
library and returns a prompt block that tells Gemini to borrow *structure* while
writing entirely original, grounded copy — never copying anyone's wording.
"""

from __future__ import annotations

from agromanch_ai.intelligence.angle_generator import AngleSelection
from agromanch_ai.intelligence.trend_library import VIRAL_FORMATS

# Map marketing angles → the viral format whose structure fits best.
_ANGLE_TO_FORMAT = {
    "Biggest Mistake Farmers Make": "Top Mistakes",
    "5 Common Mistakes": "Top Mistakes",
    "Save Money": "Before vs After",
    "Increase Yield": "Before vs After",
    "Before vs After": "Before vs After",
    "Scientific Method": "Step by Step",
    "Step-by-Step Guide": "Step by Step",
    "Desi Jugaad": "Hidden Secrets",
    "Hidden Secret": "Hidden Secrets",
    "Government Recommendation": "Government Update",
    "ICAR Recommended Practice": "Expert Tips",
    "Expert Tips": "Expert Tips",
    "Myth vs Fact": "Myth vs Fact",
    "Warning": "Warning",
    "Urgent Alert": "Seasonal Alert",
    "Seasonal Opportunity": "Seasonal Alert",
    "Case Study": "Case Study",
    "Farmer Success Story": "Success Story",
    "Local Problem": "Local Farmer Story",
}

_FORMAT_BY_NAME = {f.name: f for f in VIRAL_FORMATS}


def _structure_for(angle: str) -> str:
    fmt_name = _ANGLE_TO_FORMAT.get(angle, "Curiosity")
    fmt = _FORMAT_BY_NAME.get(fmt_name)
    return f"{fmt_name} — {fmt.structure}" if fmt else fmt_name


def competitor_inspiration(angles: AngleSelection) -> str:
    """Prompt block: proven structures to borrow, with a strict no-copy rule."""
    return (
        "COMPETITOR INSPIRATION (borrow STRUCTURE only — never copy any wording; "
        "write 100% original copy grounded in the verified context):\n"
        f"- Primary format: {_structure_for(angles.primary)}\n"
        f"- Secondary format: {_structure_for(angles.secondary)}"
    )
