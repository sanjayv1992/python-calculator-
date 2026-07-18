"""Build the AgroManch Knowledge Library catalog and print a health report.

Scans knowledge/, scores every document, detects duplicates and outdated docs,
and writes knowledge/catalog.json (searchable metadata index).

Run from the repository root:
    python scripts/build_catalog.py [--root knowledge]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from agromanch_ai.knowledge.catalog import build_catalog


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the knowledge catalog")
    parser.add_argument("--root", default="knowledge")
    parser.add_argument("--min-quality", type=int, default=50)
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        raise SystemExit(f"Knowledge folder not found: {root} (run from repo root)")

    entries, summary = build_catalog(root, min_quality=args.min_quality)

    print("=" * 44)
    print("AgroManch Knowledge Library — Health Report")
    print("=" * 44)
    print(f"Documents scanned : {summary.total}")
    print(f"Average quality   : {summary.avg_score:.1f}/100")
    print(f"Usable documents  : {sum(1 for e in entries if e['usable'])}")
    print(f"Duplicates        : {len(summary.duplicates)}")
    print(f"Outdated          : {len(summary.outdated)}")
    print(f"Low quality       : {len(summary.low_quality)}")
    print(f"Invalid metadata  : {len(summary.invalid)}")
    print("\nBy category:")
    for cat, n in sorted(summary.by_category.items()):
        print(f"  {cat:22s} {n}")
    if summary.invalid:
        print("\nMetadata problems:")
        for p in summary.invalid:
            print(f"  - {p}")
    print(f"\nWrote {root / 'catalog.json'}")


if __name__ == "__main__":
    main()
