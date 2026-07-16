"""Weather-based crop advisory from indexed agromet bulletins.

Run:
    python examples/agromanch/weather_crop_advisor.py \
        --region "Vidarbha, Maharashtra" \
        --crop-stage "cotton at flowering" \
        --weather "heavy rain (60-80mm) expected over the next 3 days"
"""

from __future__ import annotations

import argparse
import asyncio

from _common import agromanch_session


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch weather advisor")
    parser.add_argument("--region", default="Vidarbha, Maharashtra")
    parser.add_argument("--crop-stage", default="cotton at flowering stage")
    parser.add_argument(
        "--weather",
        default="heavy rain (60-80 mm) expected over the next 3 days, "
        "followed by high humidity",
    )
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        answer = await ctx.chat.ask_template(
            ctx.notebook.id,
            "weather_advisory",
            region=args.region,
            crop_stage=args.crop_stage,
            weather_context=args.weather,
        )
        print(answer.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
