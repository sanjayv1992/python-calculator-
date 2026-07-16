"""Prompt registry for the Gemini content engine.

Each task is a :class:`PromptSpec` — a system instruction, a user-message
template, and an optional temperature — versioned in one place so content
quality is tuned centrally. Templates are ``str.format`` strings.

The generator always supplies ``context_block`` (the verified NotebookLM
context) and ``language_name``; callers supply ``topic`` and any task-specific
fields.

Usage::

    from agromanch_ai.prompts import get_spec, render
    system, user = render("instagram_carousel", context_block=ctx,
                          topic="drip irrigation", language_name="English")
"""

from __future__ import annotations

from agromanch_ai.prompts.advisory_prompts import ADVISORY_SPECS
from agromanch_ai.prompts.content_prompts import CONTENT_SPECS
from agromanch_ai.prompts.spec import PromptSpec

SPECS: dict[str, PromptSpec] = {**CONTENT_SPECS, **ADVISORY_SPECS}


def list_templates() -> list[str]:
    return sorted(SPECS)


def get_spec(name: str) -> PromptSpec:
    if name not in SPECS:
        raise KeyError(
            f"Unknown prompt {name!r}. Available: {', '.join(list_templates())}"
        )
    return SPECS[name]


def required_fields(name: str) -> set[str]:
    return get_spec(name).placeholders()


def render(name: str, **fields: str) -> tuple[str, str]:
    """Render a task's (system_instruction, user_prompt)."""
    return get_spec(name).render(**fields)


__all__ = [
    "PromptSpec",
    "SPECS",
    "CONTENT_SPECS",
    "ADVISORY_SPECS",
    "get_spec",
    "render",
    "list_templates",
    "required_fields",
]
