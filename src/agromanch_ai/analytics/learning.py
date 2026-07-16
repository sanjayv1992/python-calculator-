"""Learning engine: derive best-performing styles from history (deterministic)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from agromanch_ai.analytics.history import PerformanceRecord

# Content dimensions we learn preferences for.
_DIMENSIONS = (
    "hook_style",
    "cta",
    "carousel_structure",
    "hashtags_count",
    "video_pacing",
    "caption_style",
)


@dataclass(slots=True)
class Preferences:
    """Best-performing value per content dimension (empty if no data)."""

    hook_style: str = ""
    cta: str = ""
    carousel_structure: str = ""
    hashtags_count: str = ""
    video_pacing: str = ""
    caption_style: str = ""
    sample_size: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _best_value(records: list[PerformanceRecord], dim: str) -> str:
    """Value of ``dim`` with the highest mean performance score.

    Ties break deterministically by value string so results are reproducible.
    """
    buckets: dict[str, list[float]] = {}
    for r in records:
        value = getattr(r, dim)
        if value in ("", 0, None):
            continue
        buckets.setdefault(str(value), []).append(r.performance_score())
    if not buckets:
        return ""
    means = {v: sum(s) / len(s) for v, s in buckets.items()}
    best = max(means.items(), key=lambda kv: (kv[1], kv[0]))
    return best[0]


def learn(records: list[PerformanceRecord]) -> Preferences:
    """Compute preferred styles from performance history."""
    prefs = Preferences(sample_size=len(records))
    for dim in _DIMENSIONS:
        setattr(prefs, dim, _best_value(records, dim))
    return prefs


def learning_directive(prefs: Preferences) -> str:
    """Prompt block nudging generation toward higher-performing styles."""
    if prefs.sample_size == 0:
        return (
            "LEARNING: no performance history yet — use best-practice defaults and "
            "vary style to gather signal."
        )
    parts = []
    if prefs.hook_style:
        parts.append(f"prefer '{prefs.hook_style}' style hooks")
    if prefs.cta:
        parts.append(f"prefer '{prefs.cta}' style CTAs")
    if prefs.carousel_structure:
        parts.append(f"prefer the '{prefs.carousel_structure}' carousel structure")
    if prefs.hashtags_count:
        parts.append(f"use around {prefs.hashtags_count} hashtags")
    if prefs.video_pacing:
        parts.append(f"use '{prefs.video_pacing}' video pacing")
    if prefs.caption_style:
        parts.append(f"use a '{prefs.caption_style}' caption style")
    body = "; ".join(parts) if parts else "use best-practice defaults"
    return (
        f"LEARNING (from {prefs.sample_size} past posts) — {body}. These styles "
        "performed best historically; apply them unless the topic calls for a change."
    )
