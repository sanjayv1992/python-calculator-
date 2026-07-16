"""Generated artifacts: podcasts, quizzes, flashcards from the knowledge base."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger
from agromanch_ai.utils.text import safe_filename

if TYPE_CHECKING:  # pragma: no cover - typing only
    from notebooklm import GenerationStatus, NotebookLMClient

logger = get_logger("artifacts")


class ArtifactService:
    """Generate and download NotebookLM artifacts for AgroManch content."""

    def __init__(self, client: "NotebookLMClient", settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def _wait(self, notebook_id: str, status: "GenerationStatus") -> "GenerationStatus":
        logger.info("Waiting for task %s (may take several minutes)...", status.task_id)
        return await self._client.artifacts.wait_for_completion(
            notebook_id,
            status.task_id,
            timeout=self._settings.artifact_timeout,
            on_status_change=lambda s: logger.info("Status: %s", s.status),
        )

    async def generate_podcast(
        self,
        notebook_id: str,
        *,
        instructions: str,
        title: str = "agromanch_podcast",
        source_ids: list[str] | None = None,
    ) -> Path:
        """Generate an Audio Overview podcast and download it as MP3."""
        status = await self._client.artifacts.generate_audio(
            notebook_id,
            source_ids=source_ids,
            language=self._settings.language,
            instructions=instructions,
        )
        await self._wait(notebook_id, status)
        out = self._settings.ensure_output_dir() / f"{safe_filename(title)}.mp3"
        path = await self._client.artifacts.download_audio(notebook_id, str(out))
        logger.info("Podcast downloaded: %s", path)
        return Path(path)

    async def generate_quiz(
        self,
        notebook_id: str,
        *,
        instructions: str | None = None,
        title: str = "agromanch_quiz",
        output_format: str = "markdown",
    ) -> Path:
        """Generate a farmer-training quiz and download it."""
        status = await self._client.artifacts.generate_quiz(
            notebook_id, instructions=instructions
        )
        await self._wait(notebook_id, status)
        suffix = "md" if output_format == "markdown" else output_format
        out = self._settings.ensure_output_dir() / f"{safe_filename(title)}.{suffix}"
        path = await self._client.artifacts.download_quiz(
            notebook_id, str(out), output_format=output_format
        )
        logger.info("Quiz downloaded: %s", path)
        return Path(path)

    async def generate_flashcards(
        self,
        notebook_id: str,
        *,
        instructions: str | None = None,
        title: str = "agromanch_flashcards",
        output_format: str = "csv",
    ) -> Path:
        """Generate revision flashcards (e.g. for extension-worker training)."""
        status = await self._client.artifacts.generate_flashcards(
            notebook_id, instructions=instructions
        )
        await self._wait(notebook_id, status)
        out = self._settings.ensure_output_dir() / f"{safe_filename(title)}.{output_format}"
        path = await self._client.artifacts.download_flashcards(
            notebook_id, str(out), output_format=output_format
        )
        logger.info("Flashcards downloaded: %s", path)
        return Path(path)
