"""NotebookLM retrieval — the ONLY job NotebookLM has in AgroManch.

It pulls verified facts and citations from the indexed trusted documents (ICAR,
KVK, government PDFs, labels) for a topic. Gemini then turns that context into
content or advice. NotebookLM never writes the final output.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger
from agromanch_ai.models import VerifiedContext
from agromanch_ai.utils.text import references_from_ask_result

if TYPE_CHECKING:  # pragma: no cover - typing only
    from notebooklm import NotebookLMClient

logger = get_logger("retrieval")

_NO_CONTEXT = "NO_RELEVANT_CONTEXT"

_RETRIEVAL_QUERY = (
    "From the documents in this notebook, extract every relevant fact, figure, "
    "recommendation, and safety note about the following topic. Present concise, "
    "faithful notes grounded strictly in the documents — do not add outside "
    "knowledge. If the documents do not cover this topic at all, reply with "
    f"exactly '{_NO_CONTEXT}'.\n\nTOPIC: {{topic}}"
)


class RetrievalService:
    """Fetch `VerifiedContext` for a topic from the NotebookLM knowledge base."""

    def __init__(self, client: "NotebookLMClient", settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def get_context(
        self, notebook_id: str, topic: str, *, source_ids: list[str] | None = None
    ) -> VerifiedContext:
        logger.info("Retrieving verified context for %r", topic)
        result = await self._client.chat.ask(
            notebook_id, _RETRIEVAL_QUERY.format(topic=topic), source_ids=source_ids
        )
        answer = (result.answer or "").strip()

        if not answer or _NO_CONTEXT in answer:
            logger.warning("No relevant context found for %r", topic)
            return VerifiedContext(topic=topic, context_text="", references=[], grounded=False)

        titles = {s.id: s.title for s in await self._client.sources.list(notebook_id)}
        references = references_from_ask_result(result, titles)
        logger.info("Retrieved context for %r (%d sources)", topic, len(references))
        return VerifiedContext(
            topic=topic,
            context_text=answer,
            references=references,
            grounded=True,
        )
