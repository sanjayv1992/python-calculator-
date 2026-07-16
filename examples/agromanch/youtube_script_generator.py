"""YouTube content pack: Shorts script + description + SEO keywords on one topic.

All three drafts are grounded in the knowledge base and saved to the output
directory with their source citations attached.

Run:
    python examples/agromanch/youtube_script_generator.py \
        --topic "Fall Armyworm control in maize"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch YouTube pack")
    parser.add_argument("--topic", default="Fall Armyworm control in maize")
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        pack = await ctx.content.generate_bundle(
            ctx.notebook.id,
            ["youtube_shorts_script", "youtube_description", "seo_keywords"],
            args.topic,
        )
        for content in pack:
            path = ctx.content.save(content)
            print(f"Saved {content.kind}: {path}")
        print("\n--- Shorts script preview ---\n")
        print(pack[0].to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
