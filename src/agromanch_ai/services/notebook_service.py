"""Notebook lifecycle and source management for the knowledge base."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger

if TYPE_CHECKING:  # pragma: no cover - typing only
    from notebooklm import Notebook, NotebookLMClient, Source

logger = get_logger("notebook")

# File types the bulk importer knows how to hand to NotebookLM.
_TEXT_SUFFIXES = {".md", ".txt"}
_UPLOAD_SUFFIXES = {".pdf", ".docx", ".pptx", ".csv"}


class NotebookService:
    """Find/create the AgroManch notebook and manage its sources."""

    def __init__(self, client: "NotebookLMClient", settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def get_or_create(self) -> "Notebook":
        """Resolve the knowledge-base notebook.

        Priority: pinned ``AGROMANCH_NOTEBOOK_ID`` → existing notebook with
        the configured title → create a new one.
        """
        if self._settings.notebook_id:
            nb = await self._client.notebooks.get(self._settings.notebook_id)
            logger.info("Using pinned notebook %s (%s)", nb.title, nb.id)
            return nb

        title = self._settings.notebook_name
        for nb in await self._client.notebooks.list():
            if nb.title == title:
                logger.info("Found existing notebook %s (%s)", nb.title, nb.id)
                return nb

        nb = await self._client.notebooks.create(title)
        logger.info("Created notebook %s (%s)", nb.title, nb.id)
        return nb

    async def add_url(self, notebook_id: str, url: str, *, wait: bool = True) -> "Source":
        logger.info("Adding URL source: %s", url)
        return await self._client.sources.add_url(
            notebook_id, url, wait=wait, wait_timeout=self._settings.source_wait_timeout
        )

    async def add_file(self, notebook_id: str, path: str | Path, *, wait: bool = True) -> "Source":
        logger.info("Uploading file source: %s", path)
        return await self._client.sources.add_file(
            notebook_id, path, wait=wait, wait_timeout=self._settings.source_wait_timeout
        )

    async def add_text(
        self, notebook_id: str, title: str, content: str, *, wait: bool = True
    ) -> "Source":
        logger.info("Adding text source: %s", title)
        return await self._client.sources.add_text(
            notebook_id,
            title,
            content,
            wait=wait,
            wait_timeout=self._settings.source_wait_timeout,
        )

    async def list_sources(self, notebook_id: str) -> list["Source"]:
        return await self._client.sources.list(notebook_id)

    async def source_titles(self, notebook_id: str) -> dict[str, str]:
        """Map source_id → title, used to label citations."""
        return {s.id: s.title for s in await self.list_sources(notebook_id)}

    async def import_knowledge_dir(
        self, notebook_id: str, root: str | Path, *, skip_names: frozenset[str] = frozenset({"README.md"})
    ) -> list["Source"]:
        """Bulk-import a ``knowledge/`` tree into the notebook.

        - ``.md``/``.txt`` files become text sources (title = relative path)
        - ``.pdf``/office files are uploaded as file sources
        - any ``urls.txt`` file is read line-by-line as URL sources
        - README.md files (folder descriptions) are skipped

        Files whose title already exists as a source are skipped, so re-runs
        are idempotent.
        """
        root = Path(root)
        existing = {s.title for s in await self.list_sources(notebook_id)}
        added: list[Source] = []

        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.name in skip_names:
                continue
            rel = path.relative_to(root).as_posix()

            if path.name == "urls.txt":
                for line in path.read_text(encoding="utf-8").splitlines():
                    url = line.strip()
                    if not url or url.startswith("#") or url in existing:
                        continue
                    added.append(await self.add_url(notebook_id, url))
                    existing.add(url)
            elif path.suffix.lower() in _TEXT_SUFFIXES:
                if rel in existing:
                    logger.info("Skipping already-imported source: %s", rel)
                    continue
                content = path.read_text(encoding="utf-8")
                added.append(await self.add_text(notebook_id, rel, content))
                existing.add(rel)
            elif path.suffix.lower() in _UPLOAD_SUFFIXES:
                if path.name in existing:
                    logger.info("Skipping already-imported source: %s", path.name)
                    continue
                added.append(await self.add_file(notebook_id, path))
                existing.add(path.name)
            else:
                logger.debug("Ignoring unsupported file: %s", rel)

        logger.info("Imported %d new sources from %s", len(added), root)
        return added
