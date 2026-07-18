"""Performance history — append/load records to a local JSON file."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class PerformanceRecord:
    """One published asset's measured performance (supplied by the operator/app)."""

    topic: str
    hook: str = ""
    hook_style: str = ""
    platform: str = ""
    content_type: str = ""
    publish_date: str = ""
    views: int = 0
    reach: int = 0
    shares: int = 0
    comments: int = 0
    watch_time: float = 0.0
    ctr: float = 0.0
    save_rate: float = 0.0
    engagement_rate: float = 0.0
    cta: str = ""
    carousel_structure: str = ""
    hashtags_count: int = 0
    video_pacing: str = ""
    caption_style: str = ""

    def performance_score(self) -> float:
        """Single 0-1 performance metric used for learning.

        Uses engagement_rate when present; otherwise derives one from
        interactions over reach.
        """
        if self.engagement_rate:
            return self.engagement_rate
        if self.reach:
            return min(1.0, (self.shares + self.comments) / self.reach)
        return 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class HistoryStore:
    """Local JSON store of performance records (default: data/history.json)."""

    path: Path = field(default_factory=lambda: Path("data/history.json"))

    def load(self) -> list[PerformanceRecord]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [PerformanceRecord(**r) for r in raw]

    def append(self, record: PerformanceRecord) -> None:
        records = self.load()
        records.append(record)
        self.save(records)

    def save(self, records: list[PerformanceRecord]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([r.to_dict() for r in records], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
