"""Pesticide dose calculator: label lookup + offline field math.

Two layers, mirroring the AgroManch app design:
1. NotebookLM answers *what the registered label says* (dose/ha, spray
   volume, PHI, safety) with citations from indexed label documents.
2. Pure-Python math (works offline, unit-tested) converts the label dose to
   this farmer's field size and knapsack tank.

Run the offline math only:
    python examples/agromanch/pesticide_dose_calculator.py --offline \
        --product "Example 5% SG" --crop rice --dose-per-ha 100 --unit g --acres 2.5

Include the knowledge-base label lookup:
    python examples/agromanch/pesticide_dose_calculator.py \
        --product "Example 5% SG" --crop rice --target "stem borer" \
        --dose-per-ha 100 --unit g --acres 2.5
"""

from __future__ import annotations

import argparse
import asyncio

from agromanch_ai.utils.dose import acres_to_hectares, calculate_dose


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AgroManch dose calculator")
    parser.add_argument("--product", default="Example insecticide 5% SG")
    parser.add_argument("--crop", default="rice")
    parser.add_argument("--target", default="yellow stem borer")
    parser.add_argument("--dose-per-ha", type=float, default=100.0,
                        help="Label dose of product per hectare")
    parser.add_argument("--unit", choices=("ml", "g"), default="g")
    parser.add_argument("--acres", type=float, default=2.5, help="Field size in acres")
    parser.add_argument("--spray-volume", type=float, default=500.0,
                        help="Label spray volume, litres of water per hectare")
    parser.add_argument("--tank", type=float, default=15.0,
                        help="Sprayer tank capacity in litres")
    parser.add_argument("--offline", action="store_true",
                        help="Skip the NotebookLM label lookup")
    return parser


async def main() -> None:
    args = build_parser().parse_args()

    plan = calculate_dose(
        product=args.product,
        crop=args.crop,
        dose_per_ha=args.dose_per_ha,
        unit=args.unit,
        area_ha=acres_to_hectares(args.acres),
        spray_volume_per_ha=args.spray_volume,
        tank_capacity_l=args.tank,
    )
    print(plan.to_markdown())

    if args.offline:
        return

    from _common import agromanch_session

    async with agromanch_session() as ctx:
        label_info = await ctx.chat.ask_template(
            ctx.notebook.id,
            "pesticide_dose",
            product=args.product,
            crop=args.crop,
            target=args.target,
        )
        print("\n--- Label information from the knowledge base ---\n")
        print(label_info.to_markdown())


if __name__ == "__main__":
    asyncio.run(main())
