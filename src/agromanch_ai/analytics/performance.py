"""Public API to record performance and refresh learned preferences.

Metrics come from the operator / AgroManch app — there are no social-media API
calls here. Everything persists to local JSON and is deterministic.
"""

from __future__ import annotations

import json
from pathlib import Path

from agromanch_ai.analytics.history import HistoryStore, PerformanceRecord
from agromanch_ai.analytics.learning import Preferences, learn, learning_directive
from agromanch_ai.logging import get_logger

logger = get_logger("analytics")


class PerformanceTracker:
    """Record performance and maintain a learned-preferences file."""

    def __init__(
        self,
        history_path: Path | str = "data/history.json",
        learning_path: Path | str = "data/learning.json",
    ) -> None:
        self._store = HistoryStore(Path(history_path))
        self._learning_path = Path(learning_path)

    def record(self, record: PerformanceRecord) -> None:
        self._store.append(record)
        self.refresh()

    def refresh(self) -> Preferences:
        prefs = learn(self._store.load())
        self._learning_path.parent.mkdir(parents=True, exist_ok=True)
        self._learning_path.write_text(
            json.dumps(prefs.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        logger.info("Refreshed learning (%d records)", prefs.sample_size)
        return prefs

    def preferences(self) -> Preferences:
        if self._learning_path.exists():
            data = json.loads(self._learning_path.read_text(encoding="utf-8"))
            return Preferences(**data)
        return learn(self._store.load())

    def directive(self) -> str:
        """The learning directive string for prompt injection."""
        return learning_directive(self.preferences())
