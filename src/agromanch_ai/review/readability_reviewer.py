"""Farmer Readability review agent (Farmer Readability, Language Quality)."""

from __future__ import annotations

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.review.base import Reviewer


def readability_reviewer(engine: TextEngine) -> Reviewer:
    return Reviewer("readability_reviewer", engine)
