"""Text helpers: citation extraction, filenames, markdown."""

from __future__ import annotations

import re
from typing import Any

from agromanch_ai.models import SourceRef

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


def safe_filename(name: str, max_length: int = 80) -> str:
    """Turn an arbitrary title into a filesystem-safe file stem."""
    cleaned = _UNSAFE.sub("_", name.strip()).strip("_")
    return (cleaned or "untitled")[:max_length]


def references_from_ask_result(
    ask_result: Any, titles_by_source_id: dict[str, str] | None = None
) -> list[SourceRef]:
    """Convert notebooklm-py ``AskResult.references`` into :class:`SourceRef`.

    De-duplicates by source, keeping the first citation number and snippet
    seen for each source document.
    """
    titles = titles_by_source_id or {}
    seen: dict[str, SourceRef] = {}
    for ref in getattr(ask_result, "references", None) or []:
        source_id = getattr(ref, "source_id", None)
        if not source_id or source_id in seen:
            continue
        cited = getattr(ref, "cited_text", None)
        seen[source_id] = SourceRef(
            source_id=source_id,
            citation_number=getattr(ref, "citation_number", None),
            title=titles.get(source_id),
            cited_text=cited[:200] if cited else None,
        )
    return sorted(
        seen.values(), key=lambda r: (r.citation_number is None, r.citation_number or 0)
    )
