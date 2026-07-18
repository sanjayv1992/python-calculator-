"""Government scheme assistant: eligibility answers from indexed scheme PDFs.

Run:
    python examples/agromanch/govt_scheme_assistant.py \
        --profile "smallholder with 1.2 ha in Bihar, grows paddy and vegetables" \
        --question "Which income support and insurance schemes can I get, and how do I apply?"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch scheme assistant")
    parser.add_argument(
        "--profile",
        default="smallholder farmer with 1.2 hectares in Bihar, grows paddy "
        "and vegetables, has Aadhaar and a bank account",
    )
    parser.add_argument(
        "--question",
        default="Which income support and crop insurance schemes am I "
        "eligible for, and how do I apply?",
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        answer = await ctx.advisory.govt_scheme(
            ctx.notebook.id,
            farmer_profile=args.profile,
            question=args.question,
        )
        print(answer.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
