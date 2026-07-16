"""Prompt specs for the multi-agent review system (Gemini-only reviewers).

Each reviewer returns STRICT JSON so scores parse deterministically. Reviewers
score only their own categories. The writer's rewrite spec regenerates content
from the verified context plus the reviewers' notes.
"""

from __future__ import annotations

from agromanch_ai.prompts.spec import PromptSpec

_REVIEW_SYS = (
    "You are a strict senior {role} reviewing AgroManch agricultural content for "
    "Indian farmers. Judge ONLY against the verified context and best practice. "
    "Return ONLY a JSON object with keys: scores (an object mapping each of these "
    "categories to a number 0-10: {categories}), strengths (array of strings), "
    "weaknesses (array of strings), rewrite_suggestions (array of strings). "
    "No prose, no code fences — JSON only."
)

_REVIEW_USER = (
    "VERIFIED CONTEXT:\n{context_block}\n\n"
    "CONTENT TO REVIEW ({kind}):\n{content}\n\n"
    "Score strictly and give concrete, actionable notes."
)


def reviewer_spec(role: str, categories: str) -> PromptSpec:
    return PromptSpec(
        system_instruction=_REVIEW_SYS,
        user_template=_REVIEW_USER,
        temperature=0.2,
    )


# Category ownership per reviewer (the 8 scoring categories are split across them).
REVIEWER_CATEGORIES = {
    "fact_checker": ["Scientific Accuracy"],
    "marketing_reviewer": ["Marketing Impact", "Emotional Hook", "Virality", "CTA"],
    "seo_reviewer": ["SEO"],
    "readability_reviewer": ["Farmer Readability", "Language Quality"],
}

REVIEWER_ROLES = {
    "fact_checker": "agricultural scientist / fact checker",
    "marketing_reviewer": "social-media marketing strategist",
    "seo_reviewer": "SEO specialist",
    "readability_reviewer": "farmer-communication and language expert",
}

# The rewrite spec used by the Writer agent to improve low-scoring content.
REWRITE_SPEC = PromptSpec(
    system_instruction=(
        "You are the AgroManch senior content writer. Rewrite the content to fix "
        "the reviewer weaknesses while keeping it 100% grounded in the verified "
        "context and in the same format and language. Output ONLY the improved "
        "content — no commentary."
    ),
    user_template=(
        "VERIFIED CONTEXT:\n{context_block}\n\n"
        "ORIGINAL CONTENT ({kind}):\n{content}\n\n"
        "REVIEWER NOTES TO FIX:\n{notes}\n\n"
        "Rewrite now:"
    ),
    temperature=0.7,
)

ALL_CATEGORIES = [
    "Scientific Accuracy", "Marketing Impact", "Farmer Readability", "SEO",
    "Emotional Hook", "Virality", "CTA", "Language Quality",
]
