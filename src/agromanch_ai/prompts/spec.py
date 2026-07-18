"""The PromptSpec dataclass, in its own module to avoid import cycles."""

from __future__ import annotations

import string
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PromptSpec:
    """A Gemini prompt: static system instruction + a user template.

    Both templates are ``str.format`` strings. ``render`` supplies both from one
    field dict (extra fields are ignored, missing fields raise).
    """

    system_instruction: str
    user_template: str
    temperature: float | None = None

    def placeholders(self) -> set[str]:
        fmt = string.Formatter()
        fields: set[str] = set()
        for template in (self.system_instruction, self.user_template):
            fields |= {name for _, name, _, _ in fmt.parse(template) if name}
        return fields

    def render(self, **fields: str) -> tuple[str, str]:
        missing = self.placeholders() - fields.keys()
        if missing:
            raise ValueError(f"Prompt missing fields: {sorted(missing)}")
        return (
            self.system_instruction.format(**fields),
            self.user_template.format(**fields),
        )
