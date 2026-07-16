"""Shared bootstrap for AgroManch examples (Gemini content factory).

Requires the package installed and both credentials configured:

    pip install -e ".[dev,browser]"
    notebooklm login                 # NotebookLM retrieval (Google sign-in)
    export GEMINI_API_KEY=...         # Gemini generation

Each example opens the AgroManch knowledge-base notebook (AGROMANCH_* env vars,
see .env.example) and wires the unified pipeline:

    NotebookLM retrieval → verified context → Gemini generation → output

Run `python scripts/index_knowledge.py` once to load knowledge/ into the notebook.
"""

from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, AsyncIterator

from agromanch_ai.ai import AgroManchGenerator, ContentFactory, GeminiEngine
from agromanch_ai.analytics import PerformanceTracker
from agromanch_ai.config import Settings
from agromanch_ai.logging import configure_logging
from agromanch_ai.services import (
    AdvisoryService,
    ContentService,
    NotebookService,
    RetrievalService,
)
from agromanch_ai.utils import ensure_authenticated

if TYPE_CHECKING:  # pragma: no cover - typing only
    from notebooklm import Notebook, NotebookLMClient


@dataclass(slots=True)
class AgroManchContext:
    """Everything an example needs: client, notebook, and the unified services."""

    client: "NotebookLMClient"
    notebook: "Notebook"
    settings: Settings
    notebooks: NotebookService
    retrieval: RetrievalService
    generator: AgroManchGenerator
    content: ContentService
    advisory: AdvisoryService
    factory: ContentFactory


@asynccontextmanager
async def agromanch_session() -> AsyncIterator[AgroManchContext]:
    """Open an authenticated, fully-wired AgroManch session."""
    from notebooklm import NotebookLMClient

    settings = Settings.from_env()
    configure_logging()
    ensure_authenticated(settings.profile)

    if not settings.gemini_api_key:
        sys.exit(
            "GEMINI_API_KEY is not set. Export it (see .env.example) — Gemini is "
            "the content-generation engine."
        )

    async with NotebookLMClient.from_storage(profile=settings.profile) as client:
        notebooks = NotebookService(client, settings)
        notebook = await notebooks.get_or_create()
        retrieval = RetrievalService(client, settings)
        gemini = GeminiEngine(settings)
        generator = AgroManchGenerator(retrieval, gemini, settings)
        # Performance learning: reads/writes local JSON; feeds learned style
        # preferences into generation (empty until you record performance).
        tracker = PerformanceTracker()
        yield AgroManchContext(
            client=client,
            notebook=notebook,
            settings=settings,
            notebooks=notebooks,
            retrieval=retrieval,
            generator=generator,
            content=ContentService(generator, settings),
            advisory=AdvisoryService(generator, settings),
            factory=ContentFactory(generator, settings, tracker=tracker),
        )
