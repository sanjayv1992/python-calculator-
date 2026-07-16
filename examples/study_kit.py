"""Study kit: generate a quiz and flashcards from sources, download both.

Prerequisites (one-time):
    pip install "notebooklm-py[browser]"
    notebooklm login

Run:
    python examples/study_kit.py
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
        notebook = await client.notebooks.create("Study Kit Demo")
        await client.sources.add_url(
            notebook.id,
            "https://en.wikipedia.org/wiki/Integrated_pest_management",
            wait=True,
        )
        print(f"Notebook ready: {notebook.id}")

        quiz_status = await client.artifacts.generate_quiz(
            notebook.id, instructions="Focus on practical field decisions."
        )
        cards_status = await client.artifacts.generate_flashcards(notebook.id)

        for label, status in (("quiz", quiz_status), ("flashcards", cards_status)):
            print(f"Waiting for {label} (task {status.task_id})...")
            await client.artifacts.wait_for_completion(
                notebook.id, status.task_id, timeout=600
            )

        quiz_path = await client.artifacts.download_quiz(
            notebook.id, "quiz.md", output_format="markdown"
        )
        cards_path = await client.artifacts.download_flashcards(
            notebook.id, "flashcards.csv", output_format="csv"
        )
        print(f"Quiz: {quiz_path}\nFlashcards: {cards_path}")


if __name__ == "__main__":
    asyncio.run(main())
