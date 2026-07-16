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
        context = await ctx.generator.get_context(ctx.notebook.id, args.topic)

        blog = await ctx.content.generate(
            ctx.notebook.id, "blog", args.topic, context=context
        )
        blog_path = ctx.content.save(blog)
        print(f"Blog saved: {blog_path} "
              f"({len(blog.body.split())} words, {len(blog.references)} cited sources)\n")
        print(blog.body[:800])

        seo = await ctx.content.generate(
            ctx.notebook.id, "seo_keywords", args.topic, context=context
        )
        seo_path = ctx.content.save(seo)
        print(f"\nSEO keywords saved: {seo_path}")


if __name__ == "__main__":
    asyncio.run(main())
