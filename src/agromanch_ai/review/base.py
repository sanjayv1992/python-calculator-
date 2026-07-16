"""Shared reviewer plumbing: a Gemini-backed reviewer returning parsed scores."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.logging import get_logger
from agromanch_ai.prompts.review_prompts import (
    REVIEWER_CATEGORIES,
    REVIEWER_ROLES,
    reviewer_spec,
)

logger = get_logger("review")

_JSON_RE = re.compile(r"\{.*\}", re.S)


def parse_review_json(text: str) -> dict:
    """Extract the JSON object from a reviewer reply (tolerant of code fences)."""
    match = _JSON_RE.search(text or "")
    if not match:
        raise ValueError(f"reviewer returned no JSON: {text[:120]!r}")
    return json.loads(match.group(0))


@dataclass(slots=True)
class ReviewResult:
    scores: dict[str, float] = field(default_factory=dict)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    rewrite_suggestions: list[str] = field(default_factory=list)


class Reviewer:
    """One review agent — a Gemini call scoring its own categories."""

    def __init__(self, name: str, engine: TextEngine) -> None:
        self.name = name
        self._engine = engine
        self._categories = REVIEWER_CATEGORIES[name]
        self._role = REVIEWER_ROLES[name]
        self._spec = reviewer_spec(self._role, ", ".join(self._categories))

    @property
    def categories(self) -> list[str]:
        return list(self._categories)

    async def review(self, *, kind: str, content: str, context_block: str) -> ReviewResult:
        system, user = self._spec.render(
            role=self._role,
            categories=", ".join(self._categories),
            kind=kind,
            content=content,
            context_block=context_block,
        )
        raw = await self._engine.generate(
            system_instruction=system, prompt=user, temperature=self._spec.temperature
        )
        try:
            data = parse_review_json(raw)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning("%s review parse failed: %s", self.name, exc)
            return ReviewResult(scores={c: 7.0 for c in self._categories})
        scores = {
            c: float(data.get("scores", {}).get(c, 7.0)) for c in self._categories
        }
        return ReviewResult(
            scores=scores,
            strengths=list(data.get("strengths", [])),
            weaknesses=list(data.get("weaknesses", [])),
            rewrite_suggestions=list(data.get("rewrite_suggestions", [])),
        )
