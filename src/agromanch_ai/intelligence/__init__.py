"""Competitor Intelligence — reusable viral-format knowledge (no scraping).

Selects a fresh primary + secondary angle per package and assembles a
"competitor inspiration" block describing viral *structure* (never copy) that is
injected into content prompts.
"""

from agromanch_ai.intelligence.angle_generator import AngleSelection, select_angles
from agromanch_ai.intelligence.competitor import competitor_inspiration
from agromanch_ai.intelligence.trend_library import VIRAL_FORMATS, ViralFormat

__all__ = [
    "AngleSelection",
    "select_angles",
    "competitor_inspiration",
    "VIRAL_FORMATS",
    "ViralFormat",
]
