import json

from agromanch_ai.review.base import parse_review_json
from agromanch_ai.review.quality_manager import QualityManager


class ScriptedEngine:
    """Fake engine returning scripted reviewer JSON / rewrites, in order."""

    def __init__(self, review_score: float, rewrite_score: float | None = None):
        self.review_score = review_score
        self.rewrite_score = rewrite_score
        self.calls = 0
        self.rewrites = 0

    async def generate(self, *, system_instruction, prompt, temperature=None, max_output_tokens=None):
        self.calls += 1
        # Rewrite calls contain "Rewrite now" from the writer spec.
        if "Rewrite now" in prompt:
            self.rewrites += 1
            return "IMPROVED CONTENT"
        # Reviewer call → return JSON scoring all categories at the current level.
        score = (
            self.rewrite_score
            if (self.rewrite_score is not None and self.rewrites > 0)
            else self.review_score
        )
        cats = ["Scientific Accuracy", "Marketing Impact", "Farmer Readability",
                "SEO", "Emotional Hook", "Virality", "CTA", "Language Quality"]
        return json.dumps({
            "scores": {c: score for c in cats},
            "strengths": ["clear"],
            "weaknesses": ["tighten hook"],
            "rewrite_suggestions": ["stronger CTA"],
        })


def test_parse_review_json_tolerates_fences():
    data = parse_review_json('```json\n{"scores": {"SEO": 9}}\n```')
    assert data["scores"]["SEO"] == 9


async def test_high_score_passes_without_rewrite():
    engine = ScriptedEngine(review_score=9.7)
    manager = QualityManager(engine)
    outcome = await manager.review(kind="instagram_carousel", content="X", context_block="ctx")
    assert outcome.report.overall >= 95
    assert outcome.report.attempts == 1
    assert engine.rewrites == 0
    assert "Ready for Publishing" in outcome.report.render()


async def test_low_score_triggers_rewrite_and_improves():
    # First review low (7.0 → 70), rewrites then score high (9.6 → 96).
    engine = ScriptedEngine(review_score=7.0, rewrite_score=9.6)
    manager = QualityManager(engine)
    outcome = await manager.review(kind="instagram_carousel", content="X", context_block="ctx")
    assert engine.rewrites >= 1
    assert outcome.content == "IMPROVED CONTENT"
    assert outcome.report.overall >= 95


async def test_persistently_low_returns_best_after_max_attempts():
    engine = ScriptedEngine(review_score=6.0)  # never improves
    manager = QualityManager(engine)
    outcome = await manager.review(kind="instagram_carousel", content="X", context_block="ctx")
    assert outcome.report.attempts == 4  # 1 initial + 3 rewrites
    assert outcome.report.overall < 95
    assert "Scientific Accuracy" in outcome.report.render()
