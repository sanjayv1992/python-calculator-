"""Record a published asset's performance and refresh learned preferences.

Metrics come from the AgroManch app / operator — there are no social-media API
calls. Everything persists to local JSON (data/history.json, data/learning.json).

Run:
    python scripts/record_performance.py --topic "FAW in maize" \
        --platform instagram --content-type carousel --hook-style number \
        --reach 5000 --shares 120 --comments 40 --engagement-rate 0.06
"""

from __future__ import annotations

import argparse

from agromanch_ai.analytics import PerformanceRecord, PerformanceTracker


def main() -> None:
    p = argparse.ArgumentParser(description="Record content performance")
    p.add_argument("--topic", required=True)
    p.add_argument("--hook", default="")
    p.add_argument("--hook-style", default="")
    p.add_argument("--platform", default="")
    p.add_argument("--content-type", default="")
    p.add_argument("--publish-date", default="")
    p.add_argument("--views", type=int, default=0)
    p.add_argument("--reach", type=int, default=0)
    p.add_argument("--shares", type=int, default=0)
    p.add_argument("--comments", type=int, default=0)
    p.add_argument("--watch-time", type=float, default=0.0)
    p.add_argument("--ctr", type=float, default=0.0)
    p.add_argument("--save-rate", type=float, default=0.0)
    p.add_argument("--engagement-rate", type=float, default=0.0)
    p.add_argument("--cta", default="")
    p.add_argument("--carousel-structure", default="")
    p.add_argument("--hashtags-count", type=int, default=0)
    p.add_argument("--video-pacing", default="")
    p.add_argument("--caption-style", default="")
    args = p.parse_args()

    record = PerformanceRecord(
        topic=args.topic, hook=args.hook, hook_style=args.hook_style,
        platform=args.platform, content_type=args.content_type,
        publish_date=args.publish_date, views=args.views, reach=args.reach,
        shares=args.shares, comments=args.comments, watch_time=args.watch_time,
        ctr=args.ctr, save_rate=args.save_rate, engagement_rate=args.engagement_rate,
        cta=args.cta, carousel_structure=args.carousel_structure,
        hashtags_count=args.hashtags_count, video_pacing=args.video_pacing,
        caption_style=args.caption_style,
    )
    tracker = PerformanceTracker()
    tracker.record(record)
    prefs = tracker.preferences()
    print("Recorded. Learned preferences now:")
    print(f"  hook_style        : {prefs.hook_style or '-'}")
    print(f"  cta               : {prefs.cta or '-'}")
    print(f"  carousel_structure: {prefs.carousel_structure or '-'}")
    print(f"  hashtags_count    : {prefs.hashtags_count or '-'}")
    print(f"  video_pacing      : {prefs.video_pacing or '-'}")
    print(f"  caption_style     : {prefs.caption_style or '-'}")
    print(f"  sample_size       : {prefs.sample_size}")


if __name__ == "__main__":
    main()
