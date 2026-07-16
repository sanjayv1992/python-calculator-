"""Fertilizer advisor: stage-wise nutrient recommendations from indexed manuals.

Run:
    python examples/agromanch/fertilizer_advisor.py \
        --crop wheat --stage "crown root initiation" \
        --soil "N low, P medium, K medium, pH 7.8"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch fertilizer advisor")
    parser.add_argument("--crop", default="wheat")
    parser.add_argument("--stage", default="crown root initiation (21 days after sowing)")
    parser.add_argument(
        "--soil", default="soil test: N low, P medium, K medium, pH 7.8"
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        answer = await ctx.chat.ask_template(
            ctx.notebook.id,
            "fertilizer_advisor",
            crop=args.crop,
            stage=args.stage,
            soil_context=args.soil,
        )
        print(answer.to_markdown())

        # Keep an audit trail inside the notebook itself.
        await ctx.chat.save_as_note(
            ctx.notebook.id, answer, title=f"Fertilizer advisory: {args.crop}"
        )


if __name__ == "__main__":
    asyncio.run(main())
