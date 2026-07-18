"""Reusable library of viral content formats (structure, not copy).

This is a curated knowledge structure — the system does NOT scrape social media.
Each format describes the *shape* of high-performing agri content so Gemini can
borrow proven structure while writing 100% original, grounded copy.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ViralFormat:
    name: str
    structure: str  # the shape to borrow, never the wording


VIRAL_FORMATS: tuple[ViralFormat, ...] = (
    ViralFormat("Curiosity", "open a knowledge gap, delay the answer, pay it off"),
    ViralFormat("Before vs After", "show the painful before, then the improved after"),
    ViralFormat("Top Mistakes", "name common mistakes, then the correct practice"),
    ViralFormat("Hidden Secrets", "reveal a lesser-known but proven practice"),
    ViralFormat("Myth vs Fact", "state a common myth, then correct it with evidence"),
    ViralFormat("Step by Step", "a numbered, do-this-then-that walkthrough"),
    ViralFormat("Case Study", "one farmer's specific situation and result"),
    ViralFormat("Expert Tips", "a tight list of expert pointers"),
    ViralFormat("Warning", "flag a risk and the timely action to avoid loss"),
    ViralFormat("Seasonal Alert", "urgent, time-bound action for the current season"),
    ViralFormat("Success Story", "an aspirational local success narrative"),
    ViralFormat("Government Update", "a scheme/benefit explained simply with steps"),
    ViralFormat("Local Farmer Story", "a relatable neighbour-farmer story"),
)

_BY_NAME = {f.name: f for f in VIRAL_FORMATS}


def get_format(name: str) -> ViralFormat | None:
    return _BY_NAME.get(name)
