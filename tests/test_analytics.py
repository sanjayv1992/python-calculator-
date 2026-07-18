from agromanch_ai.analytics.history import HistoryStore, PerformanceRecord
from agromanch_ai.analytics.learning import learn, learning_directive
from agromanch_ai.analytics.performance import PerformanceTracker


def _rec(hook_style, eng, **kw):
    return PerformanceRecord(topic="t", hook_style=hook_style, engagement_rate=eng, **kw)


def test_history_roundtrip(tmp_path):
    store = HistoryStore(tmp_path / "history.json")
    assert store.load() == []
    store.append(_rec("curiosity", 0.2))
    store.append(_rec("number", 0.5))
    loaded = store.load()
    assert len(loaded) == 2
    assert loaded[1].hook_style == "number"


def test_learn_ranks_best_hook_style():
    records = [
        _rec("Hook A", 0.9), _rec("Hook A", 0.8),
        _rec("Hook B", 0.2), _rec("Hook B", 0.1),
    ]
    prefs = learn(records)
    assert prefs.hook_style == "Hook A"
    assert prefs.sample_size == 4


def test_learning_directive_reflects_preference():
    prefs = learn([_rec("Hook A", 0.9, cta="soft"), _rec("Hook A", 0.8, cta="soft")])
    directive = learning_directive(prefs)
    assert "Hook A" in directive
    assert "soft" in directive


def test_no_history_directive():
    assert "no performance history" in learning_directive(learn([]))


def test_tracker_persists_and_refreshes(tmp_path):
    tracker = PerformanceTracker(
        history_path=tmp_path / "h.json", learning_path=tmp_path / "l.json"
    )
    tracker.record(_rec("Hook A", 0.9))
    tracker.record(_rec("Hook A", 0.8))
    tracker.record(_rec("Hook B", 0.1))
    assert (tmp_path / "l.json").exists()
    assert tracker.preferences().hook_style == "Hook A"
    assert "Hook A" in tracker.directive()


def test_performance_score_fallback_from_reach():
    r = PerformanceRecord(topic="t", reach=100, shares=5, comments=5)
    assert r.performance_score() == 0.1  # (5+5)/100
