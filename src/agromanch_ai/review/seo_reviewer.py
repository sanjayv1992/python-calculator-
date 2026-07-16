"""SEO review agent."""

from __future__ import annotations

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.review.base import Reviewer


def seo_reviewer(engine: TextEngine) -> Reviewer:
    return Reviewer("seo_reviewer", engine)
