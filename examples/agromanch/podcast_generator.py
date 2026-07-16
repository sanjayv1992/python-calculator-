"""Podcast generator: farmer-education Audio Overview from the knowledge base.

Uses NotebookLM's audio generation (same engine as the web UI's Audio
Overviews) with AgroManch instructions, then downloads the MP3 — ready for
the AgroManch app or YouTube.

Run:
    python examples/agromanch/podcast_generator.py \
        --topic "integrated pest management for cotton"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch podcast generator")
    parser.add_argument("--topic", default="integrated pest management for cotton")
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        instructions = (
            f"Create a farmer-friendly episode about {args.topic}. Use simple "
            "language for Indian smallholder farmers, include practical field "
            "steps, and keep an encouraging tone."
        )
        path = await ctx.artifacts.generate_podcast(
            ctx.notebook.id,
            instructions=instructions,
            title=f"podcast_{args.topic}",
        )
        print(f"Podcast ready: {path}")


if __name__ == "__main__":
    asyncio.run(main())
