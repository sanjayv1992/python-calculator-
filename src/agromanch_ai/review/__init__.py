"""Multi-agent content review (Gemini-only) with an automatic rewrite loop.

Workflow: Writer (the existing generator) -> Scientific Fact Checker -> Marketing
Reviewer -> SEO Reviewer -> Farmer Readability Reviewer -> Quality Manager -> Final
Output. Each reviewer is a Gemini call returning structured JSON; the Quality
Manager aggregates 8 categories into an overall 0-100 and rewrites (up to 3 times)
until the content scores >= 95, else returns the highest-scoring version.
"""

from agromanch_ai.review.quality_manager import (
    QualityManager,
    ReviewOutcome,
    ReviewReport,
)

__all__ = ["QualityManager", "ReviewReport", "ReviewOutcome"]
