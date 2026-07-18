"""Autonomous content planning CLI — plan, queue, gaps, campaigns.

Builds a content plan, a prioritized publishing queue, an editorial calendar,
and internal reports. Deterministic; no API key or network needed.

Run from the repo root:
    python scripts/plan_content.py --days 30
"""

from __future__ import annotations

import argparse
from pathlib import Path

from agromanch_ai.knowledge.catalog import build_catalog
from agromanch_ai.planning import (
    ContentPlanner,
    EditorialCalendar,
    analyze_gaps,
    build_publishing_queue,
)
from agromanch_ai.planning.calendar import CalendarEntry
from agromanch_ai.planning.reports import (
    campaign_report,
    editorial_report,
    gap_report,
    strategy_report,
)


def main() -> None:
    p = argparse.ArgumentParser(description="AgroManch content planner")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--persona", default="small_farmer")
    p.add_argument("--knowledge-root", default="knowledge")
    p.add_argument("--out", default="data")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    plan = ContentPlanner(persona=args.persona).build_plan(args.days)

    # Editorial calendar (dedup topics).
    cal = EditorialCalendar.load(out / "editorial_calendar.json")
    for item in plan:
        cal.add(CalendarEntry(date=item.date, topic=item.topic, crop=item.crop,
                              campaign=item.campaign, content_format=item.content_format))
    cal.save()

    # Publishing queue.
    build_publishing_queue(plan, path=out / "publishing_queue.json")

    # Gap analysis over the knowledge catalog.
    entries, _ = build_catalog(Path(args.knowledge_root), write=False)
    gaps = analyze_gaps(entries, cal)

    # Internal reports.
    (out / "strategy_report.txt").write_text(strategy_report(plan), encoding="utf-8")
    (out / "editorial_report.txt").write_text(editorial_report(cal), encoding="utf-8")
    (out / "gap_report.txt").write_text(gap_report(gaps), encoding="utf-8")
    (out / "campaign_report.txt").write_text(campaign_report(), encoding="utf-8")

    print(strategy_report(plan))
    print(f"\nWrote plan, queue, calendar and reports to {out}/")


if __name__ == "__main__":
    main()
