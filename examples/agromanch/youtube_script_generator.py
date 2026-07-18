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
        # Retrieve verified context once, reuse it across the whole YouTube pack.
        context = await ctx.generator.get_context(ctx.notebook.id, args.topic)
        script = None
        for kind in ("youtube_shorts_script", "thumbnail_prompt", "seo_keywords"):
            content = await ctx.content.generate(
                ctx.notebook.id, kind, args.topic, context=context
            )
            path = ctx.content.save(content)
            print(f"Saved {kind}: {path}")
            if kind == "youtube_shorts_script":
                script = content
        if script:
            print("\n--- Shorts script preview ---\n")
            print(script.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
