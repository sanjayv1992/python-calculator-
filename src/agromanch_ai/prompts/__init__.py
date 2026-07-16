"""Prompt template registry.

Every farmer-facing question or content brief sent to NotebookLM goes through
a named template so wording is versioned in one place. Templates are plain
``str.format`` strings; :func:`render` validates that all placeholders are
supplied.

Usage::

    from agromanch_ai.prompts import render
    prompt = render("crop_doctor", crop="tomato", symptoms="curled yellow leaves",
                    region="Maharashtra", language_name="English")
"""

from __future__ import annotations

import string

from agromanch_ai.prompts.advisory_prompts import ADVISORY_PROMPTS
from agromanch_ai.prompts.content_prompts import CONTENT_PROMPTS

PROMPTS: dict[str, str] = {**ADVISORY_PROMPTS, **CONTENT_PROMPTS}


def list_templates() -> list[str]:
    return sorted(PROMPTS)


def required_fields(name: str) -> set[str]:
    """Placeholder names a template needs."""
    template = PROMPTS[name]
    return {
        field
        for _, field, _, _ in string.Formatter().parse(template)
        if field
    }


def render(name: str, **kwargs: str) -> str:
    """Render a template by name, failing loudly on missing placeholders."""
    if name not in PROMPTS:
        raise KeyError(
            f"Unknown prompt template {name!r}. Available: {', '.join(list_templates())}"
        )
    missing = required_fields(name) - kwargs.keys()
    if missing:
        raise ValueError(f"Template {name!r} missing fields: {sorted(missing)}")
    return PROMPTS[name].format(**kwargs)


__all__ = ["PROMPTS", "render", "list_templates", "required_fields"]
