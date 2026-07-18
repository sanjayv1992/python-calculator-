"""The unified generator: verified retrieval → Gemini generation.

Both content and advisory go through :meth:`AgroManchGenerator.run` — the single
AI path in AgroManch. NotebookLM only retrieves; Gemini only generates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger
from agromanch_ai.models import GeneratedContent, VerifiedContext
from agromanch_ai.prompts import get_spec, render
from agromanch_ai.prompts.brand import BRAND_GUIDE
from agromanch_ai.utils.angles import angle_directive, select_angle
from agromanch_ai.utils.seasonal import seasonal_context

if TYPE_CHECKING:  # pragma: no cover - typing only
    from agromanch_ai.services.retrieval_service import RetrievalService

logger = get_logger("generator")


class GroundingError(RuntimeError):
    """Raised when grounding is required but no verified context was retrieved."""


class AgroManchGenerator:
    """Retrieve verified context once, then generate any task with Gemini."""

    def __init__(
        self,
        retrieval: "RetrievalService",
        gemini: TextEngine,
        settings: Settings,
    ) -> None:
        self._retrieval = retrieval
        self._gemini = gemini
        self._settings = settings

    @property
    def engine(self) -> TextEngine:
        """The Gemini text engine (reused by the review agents — no new model)."""
        return self._gemini

    async def get_context(
        self, notebook_id: str, query: str, *, source_ids: list[str] | None = None
    ) -> VerifiedContext:
        return await self._retrieval.get_context(
            notebook_id, query, source_ids=source_ids
        )

    async def run(
        self,
        task: str,
        *,
        topic: str,
        notebook_id: str | None = None,
        context: VerifiedContext | None = None,
        require_grounding: bool | None = None,
        **fields: str,
    ) -> GeneratedContent:
        """Generate output for ``task`` about ``topic``.

        Retrieves verified context from NotebookLM (unless ``context`` is passed
        for reuse across a bundle). If grounding is required and no context is
        available, raises :class:`GroundingError` unless ``require_grounding`` is
        explicitly ``False`` (the ``--no-grounding`` override), which produces
        clearly-marked unverified output.
        """
        require = (
            self._settings.require_grounding
            if require_grounding is None
            else require_grounding
        )

        if context is None:
            if notebook_id is None:
                raise ValueError("run() needs either notebook_id or a context")
            context = await self.get_context(notebook_id, topic)

        if context.is_empty:
            if require:
                raise GroundingError(
                    f"No verified context found for {topic!r}. Index the knowledge "
                    "base (scripts/index_knowledge.py) or pass require_grounding="
                    "False / --no-grounding to generate unverified content."
                )
            logger.warning("Generating UNVERIFIED %s for %r (no context)", task, topic)

        spec = get_spec(task)
        # Auto-injected quality fields — the permanent brand system, language
        # style, region, seasonal intelligence, and a fresh marketing angle are
        # applied to every generation by default. Caller-supplied fields win
        # (e.g. advisory crop/region, or a package-wide fixed content_angle).
        auto_fields: dict[str, str] = {
            "context_block": context.to_prompt_block(),
            "topic": topic,
            "language_name": self._settings.language_name,
            "brand_guide": BRAND_GUIDE,
            "language_directive": self._settings.language_directive(),
            "target_region": self._settings.region,
            "persona_directive": self._settings.persona_directive(),
            "seasonal_context": seasonal_context(),
            "content_angle": angle_directive(select_angle()),
            # Enriched by the factory (Phase 2 intelligence + learning); safe
            # defaults keep single-asset generation working.
            "competitor_inspiration": "",
            "learning_directive": "",
        }
        auto_fields.update(fields)
        system, user = render(task, **auto_fields)
        body = await self._gemini.generate(
            system_instruction=system, prompt=user, temperature=spec.temperature
        )
        grounded = not context.is_empty
        logger.info("Generated %s for %r (grounded=%s)", task, topic, grounded)
        return GeneratedContent(
            kind=task,
            topic=topic,
            body=body,
            language=self._settings.language,
            references=list(context.references),
            grounded=grounded,
        )
