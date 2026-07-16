"""AI Editorial Calendar — a persisted schedule of planned content.

Maintains data/editorial_calendar.json, avoids duplicate topics, and reports
crop/format balance. Deterministic; no LLM.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

STATUSES = ("planned", "generated", "published", "completed")


@dataclass(slots=True)
class CalendarEntry:
    date: str
    topic: str
    crop: str = ""
    region: str = ""
    priority: int = 3  # 1 (highest) .. 5
    campaign: str = ""
    content_format: str = ""
    status: str = "planned"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EditorialCalendar:
    path: Path = field(default_factory=lambda: Path("data/editorial_calendar.json"))
    entries: list[CalendarEntry] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path | str = "data/editorial_calendar.json") -> "EditorialCalendar":
        path = Path(path)
        cal = cls(path=path)
        if path.exists():
            cal.entries = [CalendarEntry(**e) for e in json.loads(path.read_text("utf-8"))]
        return cal

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([e.to_dict() for e in self.entries], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def has_topic(self, topic: str) -> bool:
        t = topic.strip().lower()
        return any(e.topic.strip().lower() == t for e in self.entries)

    def add(self, entry: CalendarEntry) -> bool:
        """Add an entry unless its topic already exists (dedup). Returns added?"""
        if self.has_topic(entry.topic):
            return False
        self.entries.append(entry)
        return True

    def set_status(self, topic: str, status: str) -> bool:
        if status not in STATUSES:
            raise ValueError(f"status must be one of {STATUSES}")
        for e in self.entries:
            if e.topic.strip().lower() == topic.strip().lower():
                e.status = status
                return True
        return False

    def crop_balance(self) -> dict[str, int]:
        return dict(Counter(e.crop for e in self.entries if e.crop))

    def format_balance(self) -> dict[str, int]:
        return dict(Counter(e.content_format for e in self.entries if e.content_format))

    def by_status(self, status: str) -> list[CalendarEntry]:
        return [e for e in self.entries if e.status == status]
