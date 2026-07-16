"""Content automation: turn knowledge-base material into channel-ready drafts.

Every generator is a thin wrapper over :class:`ChatService.ask_template` with
a content prompt from ``agromanch_ai.prompts.content_prompts``, so output is
always grounded in notebook sources and carries their citations.
"""

from __future__ import annotations

from pathlib import Path

from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger
from agromanch_ai.models import GeneratedContent
from agromanch_ai.prompts.content_prompts import CONTENT_PROMPTS
from agromanch_ai.services.chat_service import ChatService
from agromanch_ai.utils.text import safe_filename

logger = get_logger("content")


class ContentService:
    """Generate AgroManch social/blog/script content from the notebook."""

    def __init__(self, chat: ChatService, settings: Settings) -> None:
        self._chat = chat
        self._settings = settings

    @staticmethod
    def kinds() -> list[str]:
        """Content types this service can generate."""
        return sorted(CONTENT_PROMPTS)

    async def generate(self, notebook_id: str, kind: str, topic: str) -> GeneratedContent:
        """Generate one piece of content of ``kind`` about ``topic``."""
        if kind not in CONTENT_PROMPTS:
            raise KeyError(f"Unknown content kind {kind!r}. Available: {self.kinds()}")
        logger.info("Generating %s about %r", kind, topic)
        answer = await self._chat.ask_template(notebook_id, kind, topic=topic)
        return GeneratedContent(
            kind=kind,
            topic=topic,
            body=answer.answer,
            language=self._settings.language,
            references=answer.references,
        )

    async def generate_bundle(
        self, notebook_id: str, kinds: list[str], topic: str
    ) -> list[GeneratedContent]:
        """Generate several content types about one topic (e.g. a campaign)."""
        return [await self.generate(notebook_id, kind, topic) for kind in kinds]

    def save(self, content: GeneratedContent) -> Path:
        """Write content (with its Sources section) to the output directory."""
        out_dir = self._settings.ensure_output_dir()
        path = out_dir / f"{safe_filename(content.topic)}__{content.kind}.md"
        path.write_text(content.to_markdown() + "\n", encoding="utf-8")
        logger.info("Saved %s -> %s", content.kind, path)
        return path
