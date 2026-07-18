"""Assisted collection helper — scaffold a KB doc from a trusted source.

Given a URL (or a registry entry name), this fetches the page text and creates a
`knowledge/<category>/<slug>.md` file with prefilled frontmatter for a HUMAN to
verify and complete before it counts as trusted knowledge.

This is deliberately NOT an unattended scraper: agricultural advice must be
human-verified, official sites have terms of use, and outbound access is
governed by the environment's network policy. See docs/knowledge-sources.md.

Run:
    python scripts/fetch_source.py --url https://... --category crops --title "..."
    python scripts/fetch_source.py --list                 # show the source registry
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from agromanch_ai.knowledge.registry import REGISTRY
from agromanch_ai.knowledge.schema import Category
from agromanch_ai.utils.text import safe_filename

_FRONTMATTER = """\
---
title: {title}
category: {category}
crop: ""
season: ""
state: ""
district: ""
source_org: {source_org}
publication_date: ""
last_verified_date: "{today}"
language: hi
scientific_names: []
hindi_names: []
local_names: []
keywords: []
summary: "TODO: one-line summary — VERIFY before use"
important_facts: []
recommended_practices: []
dosage: ""
warnings: []
references:
  - {url}
---

# {title}

> DRAFT — fetched from {url} on {today}. A human MUST verify every fact, fill in
> the metadata above, and confirm the source is authoritative before this
> document is trusted or indexed.

<!-- fetched text below (review, trim, and rewrite as verified notes) -->

{body}
"""


def _fetch_text(url: str) -> str:
    try:
        import urllib.request

        with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8", errors="replace")
        # crude tag strip — this is a scaffold, not a parser
        import re

        text = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:4000]
    except Exception as exc:  # noqa: BLE001
        return f"(could not fetch page: {exc}. Paste verified notes here.)"


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a KB doc from a source")
    parser.add_argument("--list", action="store_true", help="List the source registry")
    parser.add_argument("--url")
    parser.add_argument("--category")
    parser.add_argument("--title")
    parser.add_argument("--source-org", default="")
    parser.add_argument("--root", default="knowledge")
    args = parser.parse_args()

    if args.list:
        for e in REGISTRY:
            print(f"{e.org:32s} {e.url}  [{', '.join(e.categories)}]")
        return

    if not (args.url and args.category and args.title):
        raise SystemExit("Provide --url, --category and --title (or --list).")
    if args.category not in Category.folders():
        raise SystemExit(f"Unknown category folder {args.category!r}. "
                         f"One of: {', '.join(Category.folders())}")

    today = dt.date.today().isoformat()
    body = _fetch_text(args.url)
    out = Path(args.root) / args.category / f"{safe_filename(args.title)}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        _FRONTMATTER.format(
            title=args.title, category=args.category,
            source_org=args.source_org or "TODO: official source org",
            today=today, url=args.url, body=body,
        ),
        encoding="utf-8",
    )
    print(f"Scaffolded {out} — VERIFY and complete the metadata before indexing.")


if __name__ == "__main__":
    main()
