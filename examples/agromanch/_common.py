"""Shared bootstrap for AgroManch examples.

Requires the package to be installed first:

    pip install -e ".[dev]"        # from the repository root
    notebooklm login               # one-time Google authentication

Each example opens the shared AgroManch knowledge-base notebook (configured
via AGROMANCH_* env vars, see .env.example). Run
``python scripts/index_knowledge.py`` once to load the knowledge/ folder
into it.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, AsyncIterator

from agromanch_ai.config import Settings
from agromanch_ai.logging import configure_logging
from agromanch_ai.services import (
    ArtifactService,
    ChatService,
    ContentService,
    NotebookService,
)
from agromanch_ai.utils import ensure_authenticated

if TYPE_CHECKING:  # pragma: no cover - typing only
    from notebooklm import Notebook, NotebookLMClient


@dataclass(slots=True)
class AgroManchContext:
    """Everything an example needs: client, notebook, and services."""

    client: "NotebookLMClient"
    notebook: "Notebook"
    settings: Settings
    notebooks: NotebookService
    chat: ChatService
    content: ContentService
    artifacts: ArtifactService


@asynccontextmanager
async def agromanch_session() -> AsyncIterator[AgroManchContext]:
    """Open an authenticated session on the AgroManch knowledge notebook."""
    from notebooklm import NotebookLMClient

    settings = Settings.from_env()
    configure_logging()
    ensure_authenticated(settings.profile)

    async with NotebookLMClient.from_storage(profile=settings.profile) as client:
        notebooks = NotebookService(client, settings)
        notebook = await notebooks.get_or_create()
        chat = ChatService(client, settings)
        yield AgroManchContext(
            client=client,
            notebook=notebook,
            settings=settings,
            notebooks=notebooks,
            chat=chat,
            content=ContentService(chat, settings),
            artifacts=ArtifactService(client, settings),
        )
