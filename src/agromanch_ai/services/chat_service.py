"""Grounded Q&A over the knowledge base, with citations preserved."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger
from agromanch_ai.models import CitedAnswer
from agromanch_ai.prompts import render
from agromanch_ai.utils.text import references_from_ask_result

if TYPE_CHECKING:  # pragma: no cover - typing only
    from notebooklm import NotebookLMClient

logger = get_logger("chat")


class ChatService:
    """Ask questions against the AgroManch notebook and keep citations."""

    def __init__(self, client: "NotebookLMClient", settings: Settings) -> None:
        self._client = client
        self._settings = settings

    async def ask(
        self,
        notebook_id: str,
        question: str,
        *,
        source_ids: list[str] | None = None,
        conversation_id: str | None = None,
    ) -> CitedAnswer:
        """Send a raw question; returns the answer with source references."""
        logger.info("Asking: %.120s", question.replace("\n", " "))
        result = await self._client.chat.ask(
            notebook_id,
            question,
            source_ids=source_ids,
            conversation_id=conversation_id,
        )
        titles = {
            s.id: s.title for s in await self._client.sources.list(notebook_id)
        }
        answer = CitedAnswer(
            question=question,
            answer=result.answer,
            references=references_from_ask_result(result, titles),
            conversation_id=result.conversation_id,
            language=self._settings.language,
        )
        logger.info(
            "Answer received (%d chars, %d cited sources)",
            len(answer.answer),
            len(answer.references),
        )
        return answer

    async def ask_template(
        self,
        notebook_id: str,
        template: str,
        *,
        conversation_id: str | None = None,
        **fields: str,
    ) -> CitedAnswer:
        """Render a named prompt template (see ``agromanch_ai.prompts``) and ask it.

        ``language_name`` is filled from settings automatically.
        """
        fields.setdefault("language_name", self._settings.language_name)
        prompt = render(template, **fields)
        return await self.ask(
            notebook_id, prompt, conversation_id=conversation_id
        )

    async def save_as_note(self, notebook_id: str, answer: CitedAnswer, *, title: str) -> None:
        """Persist an answer into the notebook as a note (audit trail)."""
        # Re-ask is unnecessary: save the rendered markdown as a text note.
        await self._client.notes.create(notebook_id, title, answer.to_markdown())
        logger.info("Saved answer as note: %s", title)
