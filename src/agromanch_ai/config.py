"""Environment-driven configuration for the AgroManch AI Knowledge Engine.

All runtime knobs come from ``AGROMANCH_*`` environment variables so the same
code can run locally, in CI, or inside a future AgroManch service without
edits. Copy ``.env.example`` to ``.env`` and export it, or set the variables
in your process manager.

No secrets live here: Google authentication is handled entirely by
``notebooklm login`` (see README), which stores its own state.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_NOTEBOOK_NAME = "AgroManch Knowledge Base"
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("en", "hi")

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
}


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got {raw!r}") from exc


@dataclass(slots=True)
class Settings:
    """Runtime settings for AgroManch services.

    Attributes:
        notebook_name: Title of the NotebookLM notebook that holds the
            agricultural knowledge base. Used by
            :class:`~agromanch_ai.services.notebook_service.NotebookService`
            to find or create the notebook when ``notebook_id`` is unset.
        notebook_id: Pin a specific notebook by ID (skips lookup by name).
        language: Answer language for farmer-facing output ("en" or "hi").
        output_dir: Where generated content and downloaded artifacts land.
        profile: Optional notebooklm-py auth profile name (multi-account).
        source_wait_timeout: Seconds to wait for a source to finish indexing.
        artifact_timeout: Seconds to wait for audio/quiz/etc. generation.
    """

    notebook_name: str = DEFAULT_NOTEBOOK_NAME
    notebook_id: str | None = None
    language: str = DEFAULT_LANGUAGE
    output_dir: Path = field(default_factory=lambda: Path("output"))
    profile: str | None = None
    source_wait_timeout: float = 120.0
    artifact_timeout: float = 600.0

    def __post_init__(self) -> None:
        if self.language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"AGROMANCH_LANGUAGE must be one of {SUPPORTED_LANGUAGES}, "
                f"got {self.language!r}"
            )

    @property
    def language_name(self) -> str:
        return LANGUAGE_NAMES[self.language]

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from ``AGROMANCH_*`` environment variables."""
        return cls(
            notebook_name=os.environ.get(
                "AGROMANCH_NOTEBOOK_NAME", DEFAULT_NOTEBOOK_NAME
            ).strip()
            or DEFAULT_NOTEBOOK_NAME,
            notebook_id=os.environ.get("AGROMANCH_NOTEBOOK_ID") or None,
            language=(
                os.environ.get("AGROMANCH_LANGUAGE", DEFAULT_LANGUAGE).strip().lower()
                or DEFAULT_LANGUAGE
            ),
            output_dir=Path(os.environ.get("AGROMANCH_OUTPUT_DIR", "output")),
            profile=os.environ.get("AGROMANCH_PROFILE") or None,
            source_wait_timeout=_env_float("AGROMANCH_SOURCE_WAIT_TIMEOUT", 120.0),
            artifact_timeout=_env_float("AGROMANCH_ARTIFACT_TIMEOUT", 600.0),
        )

    def ensure_output_dir(self) -> Path:
        """Create the output directory if needed and return it."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir
