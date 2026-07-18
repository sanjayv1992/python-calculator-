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
DEFAULT_LANGUAGE = "hi"  # AgroManch audience is Indian farmers
SUPPORTED_LANGUAGES = ("hi", "en", "bho")
DEFAULT_REGION = "Purvanchal (eastern UP) and Bihar"

DEFAULT_GEMINI_MODEL = "gemini-2.5-pro"  # max quality; auto-falls back down the chain
# Tried in order when the configured model is unavailable (404) or has no
# quota (429): 2.5-flash may be retired for new keys, so the alias
# gemini-flash-latest is the last resort that tracks Google's current model.
FALLBACK_GEMINI_MODELS = ("gemini-2.5-flash", "gemini-flash-latest")
FALLBACK_GEMINI_MODEL = FALLBACK_GEMINI_MODELS[0]  # backward-compat alias
DEFAULT_GEMINI_TEMPERATURE = 0.7
DEFAULT_GEMINI_TIMEOUT = 120.0  # seconds per request

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi (हिन्दी)",
    "bho": "Bhojpuri (भोजपुरी)",
}

# Per-language style guidance injected into every prompt so the model writes the
# way farmers actually speak — not literal, textbook translation.
LANGUAGE_DIRECTIVES = {
    "hi": (
        "Write in natural, conversational Hindi as spoken in village India — NOT "
        "literal, Sanskritized, or textbook Hindi. Use the everyday words farmers "
        "use and mix in common Hinglish terms where natural (spray, fertilizer, "
        "dose, mandi rate, WhatsApp). It must sound like a trusted local friend, "
        "never machine-translated."
    ),
    "bho": (
        "Write spoken/social copy (reels, voiceover, WhatsApp, hooks, captions, "
        "carousel) in warm, folksy Bhojpuri (Devanagari) as spoken across "
        "Purvanchal, eastern UP and Bihar — respectful and homely. IMPORTANT: keep "
        "SEO keywords and the blog in Hindi/Hinglish so they stay searchable. "
        "Never sound machine-translated."
    ),
    "en": (
        "Write in clear, simple English using familiar Indian agricultural terms "
        "(kharif, rabi, mandi, KVK). Short sentences a rural reader follows easily."
    ),
}


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got {raw!r}") from exc


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def load_env_file(path: str | Path = ".env", *, override: bool = False) -> int:
    """Load KEY=VALUE pairs from a .env file into os.environ.

    Dependency-free by design. Lines starting with ``#`` and blanks are skipped;
    surrounding quotes are stripped; an optional leading ``export `` is allowed.
    By default existing environment variables win (``override=False``). Returns
    the number of variables set. Values are never logged.
    """
    path = Path(path)
    if not path.is_file():
        return 0
    count = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export "):]
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if not key or (key in os.environ and not override):
            continue
        os.environ[key] = value
        count += 1
    return count


def mask_secret(value: str | None) -> str:
    """Render a secret safely for logs/UI: first 4 + last 2 chars only."""
    if not value:
        return "(not set)"
    if len(value) <= 8:
        return "****"
    return f"{value[:4]}…{value[-2:]}"


@dataclass(slots=True)
class Settings:
    """Runtime settings for AgroManch services.

    Attributes:
        notebook_name: Title of the NotebookLM notebook that holds the
            agricultural knowledge base. Used by
            :class:`~agromanch_ai.services.notebook_service.NotebookService`
            to find or create the notebook when ``notebook_id`` is unset.
        notebook_id: Pin a specific notebook by ID (skips lookup by name).
        language: Output language for farmer-facing content ("hi", "en", "bho").
        region: Target audience region for content (marketing/localisation).
        output_dir: Where generated content and downloaded artifacts land.
        profile: Optional notebooklm-py auth profile name (multi-account).
        source_wait_timeout: Seconds to wait for a source to finish indexing.
        artifact_timeout: Seconds to wait for audio/quiz/etc. generation.
    """

    notebook_name: str = DEFAULT_NOTEBOOK_NAME
    notebook_id: str | None = None
    language: str = DEFAULT_LANGUAGE
    region: str = DEFAULT_REGION
    persona: str = "small_farmer"
    output_dir: Path = field(default_factory=lambda: Path("output"))
    profile: str | None = None
    source_wait_timeout: float = 120.0
    artifact_timeout: float = 600.0
    # Gemini — the central content-generation engine.
    gemini_api_key: str | None = None
    gemini_model: str = DEFAULT_GEMINI_MODEL
    gemini_temperature: float = DEFAULT_GEMINI_TEMPERATURE
    gemini_timeout: float = DEFAULT_GEMINI_TIMEOUT
    # Grounding: require NotebookLM verified context before generating.
    require_grounding: bool = True
    # Multi-agent review pass at publish time (default on).
    review: bool = True

    def __post_init__(self) -> None:
        if self.language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"AGROMANCH_LANGUAGE must be one of {SUPPORTED_LANGUAGES}, "
                f"got {self.language!r}"
            )

    @property
    def language_name(self) -> str:
        return LANGUAGE_NAMES[self.language]

    def language_directive(self) -> str:
        """Per-language writing-style guidance injected into every prompt."""
        return LANGUAGE_DIRECTIVES[self.language]

    def persona_directive(self) -> str:
        """Audience-persona guidance injected into every prompt."""
        from agromanch_ai.personas import persona_directive

        return persona_directive(self.persona)

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from the environment, loading ``.env`` first.

        A ``.env`` file in the working directory is read (existing environment
        variables always win), so ``GEMINI_API_KEY`` etc. can live outside the
        shell profile. Secrets are never logged.
        """
        load_env_file()
        return cls(
            notebook_name=os.environ.get(
                "AGROMANCH_NOTEBOOK_NAME", DEFAULT_NOTEBOOK_NAME
            ).strip()
            or DEFAULT_NOTEBOOK_NAME,
            notebook_id=(
                os.environ.get("AGROMANCH_NOTEBOOK_ID")
                or os.environ.get("NOTEBOOK_ID")
                or None
            ),
            language=(
                os.environ.get("AGROMANCH_LANGUAGE", DEFAULT_LANGUAGE).strip().lower()
                or DEFAULT_LANGUAGE
            ),
            region=os.environ.get("AGROMANCH_REGION", DEFAULT_REGION).strip()
            or DEFAULT_REGION,
            persona=(os.environ.get("AGROMANCH_PERSONA", "small_farmer").strip().lower()
                     or "small_farmer"),
            output_dir=Path(os.environ.get("AGROMANCH_OUTPUT_DIR", "output")),
            profile=os.environ.get("AGROMANCH_PROFILE") or None,
            source_wait_timeout=_env_float("AGROMANCH_SOURCE_WAIT_TIMEOUT", 120.0),
            artifact_timeout=_env_float("AGROMANCH_ARTIFACT_TIMEOUT", 600.0),
            gemini_api_key=(
                os.environ.get("GEMINI_API_KEY")
                or os.environ.get("GOOGLE_API_KEY")
                or None
            ),
            gemini_model=os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()
            or DEFAULT_GEMINI_MODEL,
            gemini_temperature=_env_float(
                "GEMINI_TEMPERATURE", DEFAULT_GEMINI_TEMPERATURE
            ),
            gemini_timeout=_env_float("GEMINI_TIMEOUT", DEFAULT_GEMINI_TIMEOUT),
            require_grounding=_env_bool("AGROMANCH_REQUIRE_GROUNDING", True),
            review=_env_bool("AGROMANCH_REVIEW", True),
        )

    def ensure_output_dir(self) -> Path:
        """Create the output directory if needed and return it."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir
