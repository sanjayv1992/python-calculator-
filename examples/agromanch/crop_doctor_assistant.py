"""AgroManch Crop Doctor: diagnose crop problems from symptom descriptions.

The answer is grounded in the disease documents indexed in the knowledge-base
notebook (see knowledge/crop_diseases/) and comes back with source citations —
exactly the flow the AgroManch mobile app will call.

Run:
    python examples/agromanch/crop_doctor_assistant.py \
        --crop rice --region "West Bengal" \
        --symptoms "yellow-orange stripes on leaf tips, drying from the edges"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch Crop Doctor")
    parser.add_argument("--crop", default="rice")
    parser.add_argument("--region", default="West Bengal")
    parser.add_argument(
        "--symptoms",
        default="yellow-orange stripes starting at leaf tips, leaves drying "
        "from the edges, spreading after recent rains",
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        answer = await ctx.advisory.crop_doctor(
            ctx.notebook.id,
            crop=args.crop,
            region=args.region,
            symptoms=args.symptoms,
        )
        print(answer.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
