"""Pest & disease explainer: multi-question conversation about one pest.

Demonstrates conversation continuity (`conversation_id`) so follow-up
questions keep context — e.g. Fall Armyworm identification, then management.

Run:
    python examples/agromanch/pest_disease_chat.py --pest "Fall Armyworm" --crop maize
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="Pest & disease chat")
    parser.add_argument("--pest", default="Fall Armyworm")
    parser.add_argument("--crop", default="maize")
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        overview = await ctx.advisory.pest_disease(
            ctx.notebook.id,
            pest_or_disease=args.pest,
            crop=args.crop,
        )
        print(overview.to_markdown())

        # Follow-up question, grounded the same way.
        follow_up = await ctx.advisory.ask(
            ctx.notebook.id,
            f"For {args.pest} in {args.crop}, what should a farmer check in the "
            "field every week to catch it early? Keep it to 5 short points.",
        )
        print("\n" + follow_up.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
