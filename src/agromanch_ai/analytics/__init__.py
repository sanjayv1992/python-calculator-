"""Performance Learning System — deterministic, local-JSON, no external APIs.

Records content performance, learns which hook/CTA/structure/hashtags/pacing/
caption styles perform best, and emits a ``learning_directive`` injected into
prompts so future generations prefer higher-performing styles.
"""

from agromanch_ai.analytics.history import HistoryStore, PerformanceRecord
from agromanch_ai.analytics.learning import Preferences, learn, learning_directive
from agromanch_ai.analytics.performance import PerformanceTracker

__all__ = [
    "PerformanceRecord",
    "HistoryStore",
    "Preferences",
    "learn",
    "learning_directive",
    "PerformanceTracker",
]
