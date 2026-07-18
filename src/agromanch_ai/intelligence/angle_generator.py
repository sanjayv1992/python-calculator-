"""Select a fresh primary + secondary marketing angle per content package."""

from __future__ import annotations

import random
from dataclasses import dataclass

from agromanch_ai.utils.angles import ANGLES


@dataclass(frozen=True, slots=True)
class AngleSelection:
    primary: str
    secondary: str


def select_angles(
    rng: random.Random | None = None, *, avoid: str | None = None
) -> AngleSelection:
    """Pick two distinct angles. Seeded ``rng`` → deterministic; ``avoid`` skips a
    recently-used primary so consecutive packages open differently."""
    rng = rng or random
    pool = [a for a in ANGLES if a != avoid] or list(ANGLES)
    primary = rng.choice(pool)
    secondary_pool = [a for a in ANGLES if a != primary] or list(ANGLES)
    secondary = rng.choice(secondary_pool)
    return AngleSelection(primary=primary, secondary=secondary)
