"""Autonomous Content Operations — decide what/when/why/where/how.

Deterministic, JSON-backed planning that sits on top of the Content Factory:
strategy planner, editorial calendar, campaign engine, publishing queue, content
gap analyzer, evergreen classifier, and a recommendation layer. No LLM, no network.
"""

from agromanch_ai.planning.calendar import CalendarEntry, EditorialCalendar
from agromanch_ai.planning.campaign import CAMPAIGNS, Campaign, active_campaigns
from agromanch_ai.planning.evergreen import classify_asset
from agromanch_ai.planning.gaps import GapReport, analyze_gaps
from agromanch_ai.planning.planner import ContentPlanner, PlanItem
from agromanch_ai.planning.queue import build_publishing_queue
from agromanch_ai.planning.recommend import Recommendation, recommend

__all__ = [
    "ContentPlanner",
    "PlanItem",
    "EditorialCalendar",
    "CalendarEntry",
    "Campaign",
    "CAMPAIGNS",
    "active_campaigns",
    "build_publishing_queue",
    "analyze_gaps",
    "GapReport",
    "classify_asset",
    "recommend",
    "Recommendation",
]
