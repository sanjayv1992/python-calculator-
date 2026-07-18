"""Quality Manager — runs reviewers, aggregates, and drives the rewrite loop."""

from __future__ import annotations

from dataclasses import dataclass, field

from agromanch_ai.ai.engine import TextEngine
from agromanch_ai.logging import get_logger
from agromanch_ai.prompts.review_prompts import ALL_CATEGORIES
from agromanch_ai.review.base import Reviewer, ReviewResult
from agromanch_ai.review.fact_checker import fact_checker
from agromanch_ai.review.marketing_reviewer import marketing_reviewer
from agromanch_ai.review.readability_reviewer import readability_reviewer
from agromanch_ai.review.seo_reviewer import seo_reviewer
from agromanch_ai.review.writer import WriterAgent

logger = get_logger("quality_manager")

PASS_THRESHOLD = 95.0
MAX_REWRITES = 3


@dataclass(slots=True)
class ReviewReport:
    kind: str
    overall: float  # 0-100
    category_scores: dict[str, float] = field(default_factory=dict)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    attempts: int = 1

    @property
    def recommendation(self) -> str:
        if self.overall >= PASS_THRESHOLD:
            return "Ready for Publishing"
        if self.overall >= 80:
            return "Good — minor polish optional"
        return "Needs Revision"

    def render(self) -> str:
        lines = [
            "=" * 32,
            "CONTENT REVIEW REPORT (internal only)",
            "=" * 32,
            f"Asset: {self.kind}",
            f"Overall Score: {self.overall:.0f}/100",
            "",
        ]
        for cat in ALL_CATEGORIES:
            score = self.category_scores.get(cat)
            if score is not None:
                lines.append(f"{cat}: {score:.1f}/10")
        lines += [
            "",
            f"Rewrite attempts: {self.attempts}",
            f"Recommendation: {self.recommendation}",
        ]
        if self.weaknesses:
            lines += ["", "Top notes:"] + [f"- {w}" for w in self.weaknesses[:5]]
        lines += ["=" * 32, ""]
        return "\n".join(lines)


@dataclass(slots=True)
class ReviewOutcome:
    content: str
    report: ReviewReport


class QualityManager:
    """Reviews content with all agents and rewrites until it passes (or best-of)."""

    def __init__(self, engine: TextEngine) -> None:
        self._reviewers: list[Reviewer] = [
            fact_checker(engine),
            marketing_reviewer(engine),
            seo_reviewer(engine),
            readability_reviewer(engine),
        ]
        self._writer = WriterAgent(engine)

    async def _assess(self, kind: str, content: str, context_block: str) -> tuple[
        dict[str, float], list[str], list[str], list[str]
    ]:
        scores: dict[str, float] = {}
        strengths: list[str] = []
        weaknesses: list[str] = []
        suggestions: list[str] = []
        for reviewer in self._reviewers:
            result: ReviewResult = await reviewer.review(
                kind=kind, content=content, context_block=context_block
            )
            scores.update(result.scores)
            strengths += result.strengths
            weaknesses += result.weaknesses
            suggestions += result.rewrite_suggestions
        return scores, strengths, weaknesses, suggestions

    @staticmethod
    def _overall(scores: dict[str, float]) -> float:
        present = [scores[c] for c in ALL_CATEGORIES if c in scores]
        return round(10 * sum(present) / len(present), 1) if present else 0.0

    async def review(
        self, *, kind: str, content: str, context_block: str
    ) -> ReviewOutcome:
        """Review + rewrite loop. Returns the best content and its report."""
        best_content = content
        best_scores, best_str, best_weak, suggestions = await self._assess(
            kind, content, context_block
        )
        best_overall = self._overall(best_scores)
        attempt = 1

        while best_overall < PASS_THRESHOLD and attempt <= MAX_REWRITES:
            notes = "\n".join(f"- {w}" for w in (best_weak + suggestions)) or "improve quality"
            rewritten = await self._writer.rewrite(
                kind=kind, content=best_content, context_block=context_block, notes=notes
            )
            scores, strengths, weaknesses, suggestions = await self._assess(
                kind, rewritten, context_block
            )
            overall = self._overall(scores)
            attempt += 1
            if overall > best_overall:
                best_content, best_scores = rewritten, scores
                best_str, best_weak = strengths, weaknesses
                best_overall = overall
            if best_overall >= PASS_THRESHOLD:
                break

        report = ReviewReport(
            kind=kind,
            overall=best_overall,
            category_scores=best_scores,
            strengths=best_str,
            weaknesses=best_weak,
            attempts=attempt,
        )
        logger.info("Reviewed %s: %.0f/100 after %d attempt(s)", kind, best_overall, attempt)
        return ReviewOutcome(content=best_content, report=report)
