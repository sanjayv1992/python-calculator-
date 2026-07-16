"""Build a searchable catalog over the knowledge/ library.

Scans markdown docs, parses frontmatter, scores each, detects duplicates and
outdated docs, and emits `knowledge/catalog.json` — the searchable metadata index
that gates what feeds the Content Factory.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from agromanch_ai.knowledge.quality import band, is_outdated, score_document
from agromanch_ai.knowledge.schema import KnowledgeDocument

_SKIP_NAMES = {"README.md"}


@dataclass(slots=True)
class CatalogSummary:
    total: int = 0
    by_category: dict[str, int] = field(default_factory=dict)
    duplicates: list[str] = field(default_factory=list)
    outdated: list[str] = field(default_factory=list)
    low_quality: list[str] = field(default_factory=list)
    invalid: list[str] = field(default_factory=list)
    avg_score: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "total": self.total,
            "by_category": self.by_category,
            "duplicates": self.duplicates,
            "outdated": self.outdated,
            "low_quality": self.low_quality,
            "invalid": self.invalid,
            "avg_score": round(self.avg_score, 1),
        }


def scan_documents(root: str | Path) -> list[KnowledgeDocument]:
    """Load every KB markdown doc (skipping folder READMEs) with frontmatter."""
    root = Path(root)
    docs: list[KnowledgeDocument] = []
    for path in sorted(root.rglob("*.md")):
        if path.name in _SKIP_NAMES:
            continue
        doc = KnowledgeDocument.from_file(path)
        # Default category from the parent folder if not set in frontmatter.
        if not doc.category:
            doc.category = path.parent.name
        docs.append(doc)
    return docs


def build_catalog(
    root: str | Path,
    *,
    today: date | None = None,
    write: bool = True,
    min_quality: int = 50,
) -> tuple[list[dict], CatalogSummary]:
    """Score + dedup + flag docs and (optionally) write ``catalog.json``.

    Returns (catalog entries, summary). Entries include searchable metadata and
    per-doc flags so the indexer can skip duplicate/outdated/low-quality docs.
    """
    today = today or date.today()
    root = Path(root)
    docs = scan_documents(root)

    seen_keys: dict[str, str] = {}
    seen_hashes: dict[str, str] = {}
    summary = CatalogSummary(total=len(docs))
    entries: list[dict] = []
    score_sum = 0

    for doc in docs:
        doc.quality_score = score_document(doc, today)
        score_sum += doc.quality_score
        rel = doc.path
        summary.by_category[doc.category] = summary.by_category.get(doc.category, 0) + 1

        problems = doc.validate()
        if problems:
            summary.invalid.append(f"{rel}: {', '.join(problems)}")

        key, chash = doc.dedup_key(), doc.content_hash()
        is_dup = key in seen_keys or chash in seen_hashes
        if is_dup:
            summary.duplicates.append(rel)
        else:
            seen_keys[key] = rel
            seen_hashes[chash] = rel

        outdated = is_outdated(doc, today)
        if outdated:
            summary.outdated.append(rel)
        if doc.quality_score < min_quality:
            summary.low_quality.append(rel)

        entries.append(
            {
                "path": rel,
                "title": doc.title,
                "category": doc.category,
                "crop": doc.crop,
                "season": doc.season,
                "state": doc.state,
                "district": doc.district,
                "language": doc.language,
                "source_org": doc.source_org,
                "publication_date": doc.publication_date,
                "last_verified_date": doc.last_verified_date,
                "quality_score": doc.quality_score,
                "quality_band": band(doc.quality_score),
                "search_terms": doc.search_terms(),
                "summary": doc.summary,
                "duplicate": is_dup,
                "outdated": outdated,
                "usable": (not is_dup) and (not outdated)
                and doc.quality_score >= min_quality and not problems,
            }
        )

    summary.avg_score = score_sum / len(docs) if docs else 0.0

    if write:
        (root / "catalog.json").write_text(
            json.dumps(
                {"summary": summary.to_dict(), "documents": entries},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    return entries, summary


def load_catalog(root: str | Path) -> dict:
    """Load a previously built ``catalog.json`` (or {} if absent)."""
    path = Path(root) / "catalog.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
