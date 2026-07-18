"""AgroManch AI Content Factory — the flagship workflow.

For one topic, retrieves verified context from NotebookLM once, generates the
full 15-item content bundle with Gemini, and publishes it into per-platform
folders + manifest.json ready for one-click publishing across Instagram,
Facebook, YouTube Shorts, WhatsApp, and Telegram.

Run:
    python examples/agromanch/content_factory.py --topic "Fall Armyworm control in maize"
    python examples/agromanch/content_factory.py --topic "..." --no-grounding
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch AI Content Factory")
    parser.add_argument("--topic", default="Fall Armyworm control in maize")
    parser.add_argument(
        "--no-grounding",
        action="store_true",
        help="Generate even without verified context (output marked UNVERIFIED)",
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        bundle = await ctx.factory.produce(
            ctx.notebook.id,
            args.topic,
            require_grounding=not args.no_grounding,
        )
        root = ctx.factory.publish(bundle)

        print(f"\nProduced {len(bundle.items)} assets for: {args.topic}")
        print(f"Grounded in {len(bundle.context.references)} verified source(s)")
        print(f"Published to: {root}\n")
        print("Publishing map:")
        for platform, kinds in bundle.publishing_map().items():
            print(f"  {platform:15s} <- {', '.join(kinds)}")

        print("\n--- Research summary preview ---\n")
        summary = bundle.get("research_summary")
        if summary:
            print(summary.body[:800])


if __name__ == "__main__":
    asyncio.run(main())
