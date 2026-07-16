"""Mandi price research: summarize market trends from indexed price reports.

Optionally pulls a fresh market-report URL into the notebook first, showing
how live mandi bulletins become citable knowledge.

Run:
    python examples/agromanch/mandi_price_research.py --commodity soybean \
        --region "Madhya Pradesh" [--add-source-url URL]
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch mandi research")
    parser.add_argument("--commodity", default="soybean")
    parser.add_argument("--region", default="Madhya Pradesh (Indore, Ujjain mandis)")
    parser.add_argument(
        "--add-source-url",
        default=None,
        help="Optional market-report URL to index before asking",
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        if args.add_source_url:
            src = await ctx.notebooks.add_url(ctx.notebook.id, args.add_source_url)
            print(f"Indexed new market report: {src.title}\n")

        answer = await ctx.chat.ask_template(
            ctx.notebook.id,
            "mandi_research",
            commodity=args.commodity,
            region=args.region,
        )
        print(answer.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
