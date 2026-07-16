import json
from datetime import date

from agromanch_ai.analytics.learning import Preferences
from agromanch_ai.planning import (
    ContentPlanner,
    active_campaigns,
    analyze_gaps,
    build_publishing_queue,
    classify_asset,
    recommend,
)
from agromanch_ai.planning.calendar import CalendarEntry, EditorialCalendar
from agromanch_ai.planning.evergreen import GOVT_UPDATE, WEATHER_ALERT

JULY = date(2026, 7, 15)


# --- Planner ---------------------------------------------------------------
def test_plan_lengths_and_determinism():
    planner = ContentPlanner()
    p1 = planner.build_plan(30, start=JULY)
    p2 = planner.build_plan(30, start=JULY)
    assert len(p1) == 30
    assert [i.topic for i in p1] == [i.topic for i in p2]  # deterministic
    assert len(planner.plan_7_day(start=JULY)) == 7
    assert len(planner.plan_90_day(start=JULY)) == 90


def test_plan_is_seasonal_in_july():
    plan = ContentPlanner().build_plan(7, start=JULY)
    joined = " ".join(i.topic.lower() for i in plan)
    assert "armyworm" in joined or "paddy" in joined or "maize" in joined
    assert all(i.best_cta for i in plan)


# --- Campaigns -------------------------------------------------------------
def test_active_campaigns_seasonal():
    names = {c.key for c in active_campaigns(JULY)}
    assert "rice_season" in names          # active Jun-Sep
    assert "wheat_season" not in names     # Oct-Mar only


# --- Editorial calendar ----------------------------------------------------
def test_calendar_dedup_and_status(tmp_path):
    cal = EditorialCalendar(path=tmp_path / "cal.json")
    assert cal.add(CalendarEntry(date="2026-07-15", topic="FAW in maize", crop="maize",
                                 content_format="instagram_carousel"))
    assert not cal.add(CalendarEntry(date="2026-07-16", topic="FAW in maize"))  # dup
    assert cal.set_status("FAW in maize", "published")
    cal.save()
    reloaded = EditorialCalendar.load(tmp_path / "cal.json")
    assert reloaded.entries[0].status == "published"
    assert reloaded.crop_balance() == {"maize": 1}


# --- Publishing queue ------------------------------------------------------
def test_queue_prioritises_and_writes(tmp_path):
    plan = ContentPlanner().build_plan(10, start=JULY)
    q = build_publishing_queue(plan, path=tmp_path / "q.json")
    assert len(q) == 10
    scores = [e["priority_score"] for e in q]
    assert scores == sorted(scores, reverse=True)  # sorted by priority
    assert all(e["recommend_platforms"] for e in q)
    assert json.loads((tmp_path / "q.json").read_text())


# --- Gap analyzer ----------------------------------------------------------
def test_gap_analyzer_finds_missing():
    catalog = [{"category": "crops", "crop": "rice"}]
    report = analyze_gaps(catalog)
    assert "weather" in report.missing_categories
    assert "wheat" in report.missing_crops
    assert report.recommendations


# --- Evergreen classifier --------------------------------------------------
def test_classify_asset():
    assert classify_asset("PM-KISAN scheme benefits") == GOVT_UPDATE
    assert classify_asset("Heavy rain alert for paddy") == WEATHER_ALERT


# --- Recommendation layer --------------------------------------------------
def test_recommendation_uses_learning_and_season():
    rec = recommend("Fall Armyworm control", prefs=Preferences(hook_style="number", sample_size=3), today=JULY)
    assert rec.best_format == "reel_video_prompts"  # pest → short video
    assert rec.best_hook_style == "number"
    assert rec.platforms
