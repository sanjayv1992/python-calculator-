"""Index the knowledge/ folder into the AgroManch NotebookLM notebook.

Idempotent bulk import: already-imported sources (matched by title) are
skipped, so re-run it whenever documents are added or updated.

- .md / .txt files  -> text sources (title = path relative to knowledge/)
- .pdf / office files -> uploaded file sources
- urls.txt files    -> one URL source per line (lines starting with # are ignored)
- README.md files   -> skipped (they describe the folders, not the knowledge)

Run from the repository root:
    python scripts/index_knowledge.py [--root knowledge]
"""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from agromanch_ai.config import Settings
from agromanch_ai.logging import configure_logging
from agromanch_ai.services import NotebookService
from agromanch_ai.utils import ensure_authenticated


async def main() -> None:
    parser = argparse.ArgumentParser(description="Index knowledge/ into NotebookLM")
    parser.add_argument("--root", default="knowledge", help="Knowledge folder to import")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        raise SystemExit(f"Knowledge folder not found: {root} (run from the repo root)")

    from notebooklm import NotebookLMClient

    settings = Settings.from_env()
    logger = configure_logging()
    ensure_authenticated(settings.profile)

    async with NotebookLMClient.from_storage(profile=settings.profile) as client:
        notebooks = NotebookService(client, settings)
        notebook = await notebooks.get_or_create()
        added = await notebooks.import_knowledge_dir(notebook.id, root)
        logger.info(
            "Done. Notebook %r (%s) gained %d new sources.",
            notebook.title,
            notebook.id,
            len(added),
        )
        print(
            f"\nNotebook ID: {notebook.id}\n"
            f"Pin it for faster runs: export AGROMANCH_NOTEBOOK_ID={notebook.id}"
        )


if __name__ == "__main__":
    asyncio.run(main())
