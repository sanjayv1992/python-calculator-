"""Viral Content Angle Selector.

Every content package gets a fresh marketing angle so the same crop never yields
repetitive content. Deterministic when a seeded ``random.Random`` is passed
(tests); otherwise picks at random.

In Phase 2 the Competitor Intelligence engine builds on this list; here it is the
lightweight selector the generator uses by default.
"""

from __future__ import annotations

import random

ANGLES: tuple[str, ...] = (
    "Biggest Mistake Farmers Make",
    "Save Money",
    "Increase Yield",
    "Scientific Method",
    "Desi Jugaad",
    "Government Recommendation",
    "ICAR Recommended Practice",
    "Before vs After",
    "Myth vs Fact",
    "5 Common Mistakes",
    "Hidden Secret",
    "Expert Tips",
    "Warning",
    "Urgent Alert",
    "Step-by-Step Guide",
    "Case Study",
    "Farmer Success Story",
    "Local Problem",
    "Seasonal Opportunity",
)


def select_angle(rng: random.Random | None = None, *, avoid: str | None = None) -> str:
    """Pick one marketing angle. Pass a seeded ``rng`` for deterministic output.

    ``avoid`` excludes a recently-used angle so consecutive packages differ.
    """
    rng = rng or random
    choices = [a for a in ANGLES if a != avoid] or list(ANGLES)
    return rng.choice(choices)


def angle_directive(angle: str) -> str:
    """Instruction injected into prompts telling the model how to frame content."""
    return (
        f"CONTENT ANGLE — frame this whole package as a '{angle}' story. Let this "
        "angle shape the hook, structure and examples so it feels fresh and "
        "distinct, even for a familiar crop."
    )
