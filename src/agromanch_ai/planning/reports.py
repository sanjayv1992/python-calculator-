"""Internal planning reports (text). For internal review only."""

from __future__ import annotations

from datetime import date

from agromanch_ai.planning.calendar import EditorialCalendar
from agromanch_ai.planning.campaign import active_campaigns
from agromanch_ai.planning.gaps import GapReport
from agromanch_ai.planning.planner import PlanItem


def strategy_report(plan: list[PlanItem], *, today: date | None = None) -> str:
    today = today or date.today()
    lines = ["=" * 40, "AGROMANCH STRATEGY REPORT (internal)", "=" * 40,
             f"Horizon: {len(plan)} days from {today.isoformat()}",
             f"Active campaigns: {', '.join(c.name for c in active_campaigns(today)) or '-'}", ""]
    for item in plan[:14]:
        lines.append(f"{item.date}  [{item.platform:13s}] {item.content_format:22s} {item.topic}")
    if len(plan) > 14:
        lines.append(f"... (+{len(plan) - 14} more days)")
    lines.append("=" * 40)
    return "\n".join(lines)


def editorial_report(calendar: EditorialCalendar) -> str:
    lines = ["=" * 40, "EDITORIAL CALENDAR REPORT (internal)", "=" * 40,
             f"Entries: {len(calendar.entries)}"]
    for status in ("planned", "generated", "published", "completed"):
        lines.append(f"  {status:10s}: {len(calendar.by_status(status))}")
    lines.append("\nCrop balance:")
    for crop, n in sorted(calendar.crop_balance().items()):
        lines.append(f"  {crop:16s} {n}")
    lines.append("\nFormat balance:")
    for fmt, n in sorted(calendar.format_balance().items()):
        lines.append(f"  {fmt:22s} {n}")
    lines.append("=" * 40)
    return "\n".join(lines)


def gap_report(report: GapReport) -> str:
    lines = ["=" * 40, "CONTENT GAP REPORT (internal)", "=" * 40,
             f"Missing categories: {', '.join(report.missing_categories) or 'none'}",
             f"Missing crops     : {', '.join(report.missing_crops) or 'none'}",
             f"Missing personas  : {', '.join(report.missing_personas) or 'none'}",
             "", "Recommended next:"]
    lines += [f"  - {r}" for r in report.recommendations] or ["  - (fully covered)"]
    lines.append("=" * 40)
    return "\n".join(lines)


def campaign_report(*, today: date | None = None) -> str:
    today = today or date.today()
    lines = ["=" * 40, "CAMPAIGN REPORT (internal)", "=" * 40]
    for c in active_campaigns(today):
        lines += [
            f"\n{c.name}",
            f"  Goal      : {c.goal}",
            f"  Audience  : {c.target_farmer}",
            f"  KPIs      : {', '.join(c.kpis)}",
            f"  Assets    : {', '.join(c.recommended_assets)}",
            f"  Frequency : {c.publishing_frequency}",
        ]
    lines.append("\n" + "=" * 40)
    return "\n".join(lines)
