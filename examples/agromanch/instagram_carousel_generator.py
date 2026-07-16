"""Instagram carousel generator: 7 grounded slides + hashtags on a topic.

Run:
    python examples/agromanch/instagram_carousel_generator.py \
        --topic "drip irrigation benefits for vegetable farmers"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch Instagram carousel")
    parser.add_argument(
        "--topic", default="drip irrigation benefits for vegetable farmers"
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        carousel = await ctx.content.generate(
            ctx.notebook.id, "instagram_carousel", args.topic
        )
        path = ctx.content.save(carousel)
        print(carousel.to_markdown())
        print(f"\nSaved to {path}")


if __name__ == "__main__":
    asyncio.run(main())
