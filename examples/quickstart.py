"""Quickstart: create a notebook, add a source, ask a grounded question.

Prerequisites (one-time):
    pip install "notebooklm-py[browser]"
    notebooklm login

Run:
    python examples/quickstart.py
"""

import asyncio
import sys
from pathlib import Path

from notebooklm import NotebookLMClient, paths


def ensure_login() -> None:
    if not Path(paths.get_storage_path()).exists():
        sys.exit("No NotebookLM auth found. Run `notebooklm login` first.")


async def main() -> None:
    ensure_login()
    async with NotebookLMClient.from_storage() as client:
        notebook = await client.notebooks.create("Quickstart Demo")
        print(f"Created notebook: {notebook.title} ({notebook.id})")

        source = await client.sources.add_url(
            notebook.id,
            "https://en.wikipedia.org/wiki/Sustainable_agriculture",
            wait=True,  # block until NotebookLM finishes indexing
        )
        print(f"Source ready: {source.title}")

        result = await client.chat.ask(
            notebook.id, "Summarize the key principles in 5 bullet points."
        )
        print("\n--- Answer ---\n")
        print(result.answer)
        if result.references:
            print(f"\n({len(result.references)} citation(s) returned)")


if __name__ == "__main__":
    asyncio.run(main())
