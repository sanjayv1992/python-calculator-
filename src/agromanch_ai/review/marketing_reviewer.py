"""Marketing review agent (Marketing Impact, Emotional Hook, Virality, CTA)."""

from __future__ import annotations

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.review.base import Reviewer


def marketing_reviewer(engine: TextEngine) -> Reviewer:
    return Reviewer("marketing_reviewer", engine)
