"""AgroManch Knowledge Management System.

A structured, verifiable agricultural knowledge library that continuously powers
the Content Factory. Each document carries rich metadata (frontmatter); the
catalog scores, de-duplicates, flags outdated docs, and produces a searchable
index. This layer is additive — it does not change the AI pipeline, only what
knowledge feeds it.
"""

from agromanch_ai.knowledge.catalog import CatalogSummary, build_catalog
from agromanch_ai.knowledge.schema import Category, KnowledgeDocument
from agromanch_ai.knowledge.sources import TRUSTED_SOURCES, source_rank

__all__ = [
    "Category",
    "KnowledgeDocument",
    "build_catalog",
    "CatalogSummary",
    "TRUSTED_SOURCES",
    "source_rank",
]
