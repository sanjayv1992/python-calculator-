"""Research-to-podcast: add sources, generate an Audio Overview, download MP3.

Prerequisites (one-time):
    pip install "notebooklm-py[browser]"
    notebooklm login

Run:
    python examples/research_to_podcast.py
"""

import asyncio
import sys
from pathlib import Path

from notebooklm import NotebookLMClient, paths

SOURCES = [
    "https://en.wikipedia.org/wiki/Precision_agriculture",
    "https://en.wikipedia.org/wiki/Drip_irrigation",
]


def ensure_login() -> None:
    if not Path(paths.get_storage_path()).exists():
        sys.exit("No NotebookLM auth found. Run `notebooklm login` first.")


async def main() -> None:
    ensure_login()
    async with NotebookLMClient.from_storage() as client:
        notebook = await client.notebooks.create("Podcast Demo")
        print(f"Created notebook: {notebook.id}")

        for url in SOURCES:
            src = await client.sources.add_url(notebook.id, url, wait=True)
            print(f"Indexed: {src.title}")

        status = await client.artifacts.generate_audio(
            notebook.id,
            instructions="Make it engaging and beginner-friendly.",
        )
        print(f"Generating audio (task {status.task_id})... this takes a few minutes")
        await client.artifacts.wait_for_completion(
            notebook.id, status.task_id, timeout=600
        )

        path = await client.artifacts.download_audio(notebook.id, "podcast.mp3")
        print(f"Podcast saved to {path}")


if __name__ == "__main__":
    asyncio.run(main())
