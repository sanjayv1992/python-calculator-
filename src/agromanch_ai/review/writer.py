"""Writer agent — rewrites content to fix reviewer weaknesses.

This is a thin adapter over the same Gemini engine used to generate content (no
new model). It regenerates content grounded in the verified context, applying the
Quality Manager's aggregated notes.
"""

from __future__ import annotations

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.prompts.review_prompts import REWRITE_SPEC


class WriterAgent:
    """Rewrites a piece of content given reviewer notes."""

    def __init__(self, engine: TextEngine) -> None:
        self._engine = engine

    async def rewrite(
        self, *, kind: str, content: str, context_block: str, notes: str
    ) -> str:
        system, user = REWRITE_SPEC.render(
            kind=kind, content=content, context_block=context_block, notes=notes
        )
        return await self._engine.generate(
            system_instruction=system, prompt=user, temperature=REWRITE_SPEC.temperature
        )
