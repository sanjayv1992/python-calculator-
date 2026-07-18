"""Deterministic quality scoring for knowledge documents (0-100)."""

from __future__ import annotations

from datetime import date

from agromanch_ai.knowledge.schema import SCORED_FIELDS, KnowledgeDocument
from agromanch_ai.knowledge.sources import source_rank

# Category-specific freshness windows (years) after which a doc is "outdated".
_FRESHNESS_YEARS = {
    "mandi": 1,
    "weather": 1,
    "government_schemes": 2,
    "pesticides": 3,
    "fertilizers": 3,
    "weed_management": 3,
    "plant_growth_regulators": 3,
}
_DEFAULT_FRESHNESS_YEARS = 6

# Categories where dosage + warnings are expected (agrochemicals).
_SAFETY_CATEGORIES = {"pesticides", "fertilizers", "weed_management", "plant_growth_regulators"}


def _parse_year(value: str) -> int | None:
    value = (value or "").strip()
    if len(value) >= 4 and value[:4].isdigit():
        return int(value[:4])
    return None


def freshness_years(category: str) -> int:
    return _FRESHNESS_YEARS.get(category, _DEFAULT_FRESHNESS_YEARS)


def is_outdated(doc: KnowledgeDocument, today: date | None = None) -> bool:
    """True if the doc's last-verified/publication year is past its window."""
    today = today or date.today()
    year = _parse_year(doc.last_verified_date) or _parse_year(doc.publication_date)
    if year is None:
        return True  # undated docs are treated as needing re-verification
    return (today.year - year) > freshness_years(doc.category)


def score_document(doc: KnowledgeDocument, today: date | None = None) -> int:
    """0-100 quality score from source trust, completeness, references, recency."""
    today = today or date.today()

    # Source trust: up to 40 points (rank 1 → 40, unknown → 0).
    rank = source_rank(doc.source_org)
    from agromanch_ai.knowledge.sources import TRUSTED_SOURCES

    n = len(TRUSTED_SOURCES)
    trust = max(0, round(40 * (n + 1 - rank) / n)) if rank <= n else 0

    # Completeness: up to 30 points across the scored metadata fields.
    filled = 0
    for f in SCORED_FIELDS:
        v = getattr(doc, f, "")
        if (isinstance(v, list) and v) or (isinstance(v, str) and v.strip()):
            filled += 1
    completeness = round(30 * filled / len(SCORED_FIELDS))

    # References present: up to 10.
    refs = 10 if doc.references else 0

    # Recency: up to 20, minus if outdated.
    recency = 0 if is_outdated(doc, today) else 20

    # Safety metadata where the category demands it: penalty if missing.
    penalty = 0
    if doc.category in _SAFETY_CATEGORIES and not (doc.dosage or doc.warnings):
        penalty = 10

    return max(0, min(100, trust + completeness + refs + recency - penalty))


def band(score: int) -> str:
    return "High" if score >= 75 else ("Medium" if score >= 50 else "Low")
