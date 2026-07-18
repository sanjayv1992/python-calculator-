"""Podcast generator: farmer-education podcast SCRIPT from verified context.

In the current architecture the podcast is a Gemini-written script (host +
expert dialogue) grounded in the knowledge base, plus a voiceover script ready
for TTS. Turning the script into audio (a TTS provider, or NotebookLM's optional
Audio Overview) is a documented publishing step, not part of the core path.

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
        context = await ctx.generator.get_context(ctx.notebook.id, args.topic)

        script = await ctx.content.generate(
            ctx.notebook.id, "podcast_script", args.topic, context=context
        )
        script_path = ctx.content.save(script)
        print(f"Podcast script saved: {script_path}\n")
        print(script.to_markdown())

        voiceover = await ctx.content.generate(
            ctx.notebook.id, "voiceover_script", args.topic, context=context
        )
        vo_path = ctx.content.save(voiceover)
        print(f"\nVoiceover script saved: {vo_path}")


if __name__ == "__main__":
    asyncio.run(main())
