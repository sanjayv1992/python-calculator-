"""Livestock assistant: animal husbandry answers from indexed guides.

Run:
    python examples/agromanch/livestock_assistant.py --animal "dairy cow" \
        --question "Milk yield dropped and the animal is eating less. What should I check?"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch livestock assistant")
    parser.add_argument("--animal", default="dairy cow (crossbred, 4 years)")
    parser.add_argument(
        "--question",
        default="Milk yield dropped over the last week and the animal is "
        "eating less. What should I check and do?",
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        answer = await ctx.chat.ask_template(
            ctx.notebook.id,
            "livestock",
            animal=args.animal,
            question=args.question,
        )
        print(answer.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
