"""Scientific Fact Checker review agent."""

from __future__ import annotations

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.review.base import Reviewer


def fact_checker(engine: TextEngine) -> Reviewer:
    """Reviewer scoring Scientific Accuracy against the verified context."""
    return Reviewer("fact_checker", engine)
