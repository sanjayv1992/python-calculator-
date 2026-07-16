"""Blog generator: SEO outline first, then a full grounded draft.

Run:
    python examples/agromanch/blog_generator.py \
        --topic "soil testing: why and how for small farmers"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch blog generator")
    parser.add_argument(
        "--topic", default="soil testing: why and how for small farmers"
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        outline = await ctx.content.generate(ctx.notebook.id, "blog_outline", args.topic)
        outline_path = ctx.content.save(outline)
        print(f"Outline saved: {outline_path}\n")
        print(outline.body[:800])

        draft = await ctx.content.generate(ctx.notebook.id, "blog_draft", args.topic)
        draft_path = ctx.content.save(draft)
        print(f"\nDraft saved: {draft_path} "
              f"({len(draft.body.split())} words, {len(draft.references)} cited sources)")


if __name__ == "__main__":
    asyncio.run(main())
