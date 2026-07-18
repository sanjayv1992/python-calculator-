"""Trusted agricultural source priority for the Knowledge Library.

Only documents from verifiable official sources belong in the KB. ``source_rank``
returns a 1-based priority (1 = most trusted) used by the quality scorer; unknown
sources rank lowest.
"""

from __future__ import annotations

# Priority order (1 = highest trust). Matching is case-insensitive substring.
TRUSTED_SOURCES: tuple[str, ...] = (
    "ICAR",
    "State Agricultural University",
    "KVK",
    "Government Department",
    "IMD",
    "Agmarknet",
    "eNAM",
    "Official Product Label",
    "NABARD",
    "FSSAI",
)

# Aliases → canonical trusted source (helps match real-world naming).
_ALIASES = {
    "krishi vigyan kendra": "KVK",
    "kvk": "KVK",
    "sau": "State Agricultural University",
    "agricultural university": "State Agricultural University",
    "india meteorological department": "IMD",
    "ministry of agriculture": "Government Department",
    "department of agriculture": "Government Department",
    "cib&rc": "Official Product Label",
    "pesticide label": "Official Product Label",
    "fertilizer label": "Official Product Label",
    "e-nam": "eNAM",
}

_UNRANKED = len(TRUSTED_SOURCES) + 1


def source_rank(source_org: str | None) -> int:
    """1-based trust rank for a source string (lower = more trusted)."""
    if not source_org:
        return _UNRANKED
    text = source_org.strip().lower()
    for alias, canonical in _ALIASES.items():
        if alias in text:
            return TRUSTED_SOURCES.index(canonical) + 1
    for i, trusted in enumerate(TRUSTED_SOURCES):
        if trusted.lower() in text:
            return i + 1
    return _UNRANKED


def is_trusted(source_org: str | None) -> bool:
    return source_rank(source_org) <= len(TRUSTED_SOURCES)
