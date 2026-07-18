"""Gemini text-generation engine — the central AI of the content factory.

Production-grade wrapper over the `google-genai` SDK:

- Reads ``GEMINI_API_KEY`` from the environment / ``.env`` (never hardcoded).
- Default model ``gemini-2.5-pro`` with automatic fallback to
  ``gemini-2.5-flash`` when the primary model is unavailable to the key.
- :meth:`GeminiEngine.validate` performs a real, cheap API call before first use.
- Helpful, specific errors for missing/invalid keys, exceeded quota, and
  unavailable models; retries with exponential backoff for rate limits (429),
  server errors (5xx) and timeouts; per-request timeout via HTTP options.
- Streaming-ready (:meth:`generate_stream`) and logs token usage per call.
- Secrets are always masked in logs and error messages.

Everything downstream depends only on the small :class:`TextEngine` protocol, so
tests inject a fake engine and run without an API key or network.
"""

from __future__ import annotations

import asyncio
from typing import AsyncIterator, Protocol, runtime_checkable

from agromanch_ai.config import FALLBACK_GEMINI_MODELS, Settings, mask_secret
from agromanch_ai.logging import get_logger

logger = get_logger("gemini")

_MAX_RETRIES = 4
_BACKOFF_CAP = 30.0

KEY_MISSING_HELP = (
    "GEMINI_API_KEY is not set. Get a free key at https://aistudio.google.com/apikey, "
    "then either add GEMINI_API_KEY=... to a .env file in the project root or "
    "export it in your shell. See docs/setup.md."
)
KEY_INVALID_HELP = (
    "Gemini rejected the API key (HTTP {code}). The key is invalid, revoked, or "
    "lacks access. Create a new key at https://aistudio.google.com/apikey and "
    "update GEMINI_API_KEY. Key in use: {masked}. See docs/setup.md."
)
QUOTA_HELP = (
    "Gemini quota/rate limit exceeded (HTTP 429) and retries were exhausted. "
    "Free-tier keys have small per-minute/day limits — wait and retry, lower the "
    "request rate, or enable billing on the key's Google Cloud project. "
    "See docs/setup.md#quota-exceeded."
)
MODEL_UNAVAILABLE_HELP = (
    "Gemini model {model!r} is unavailable to this key (HTTP 404). Set "
    "GEMINI_MODEL to a model your key can access (e.g. gemini-2.5-flash). "
    "See docs/setup.md#supported-models."
)


class GeminiConfigurationError(RuntimeError):
    """Configuration/credential problem with a human-actionable message."""


class GeminiQuotaError(RuntimeError):
    """Quota or rate limit exhausted after retries."""


@runtime_checkable
class TextEngine(Protocol):
    """Minimal async text-generation interface the generator depends on."""

    async def generate(
        self,
        *,
        system_instruction: str,
        prompt: str,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        ...


def _status_code(exc: Exception) -> int | None:
    """HTTP status from a google-genai APIError, else None."""
    return getattr(exc, "code", None) if hasattr(exc, "code") else None


class GeminiEngine:
    """`TextEngine` backed by Google Gemini via the `google-genai` SDK.

    The underlying client is dependency-injectable (``client=``) for tests; in
    production it is built from ``GEMINI_API_KEY`` with a per-request timeout.
    """

    def __init__(self, settings: Settings, *, client: object | None = None) -> None:
        self._settings = settings
        self._model = settings.gemini_model
        self._default_temperature = settings.gemini_temperature
        self._validated = False
        # Models still untried when the current one is unavailable/quota-less.
        self._fallbacks = [m for m in FALLBACK_GEMINI_MODELS if m != self._model]
        if client is not None:
            self._client = client
        else:
            if not settings.gemini_api_key:
                raise GeminiConfigurationError(KEY_MISSING_HELP)
            from google import genai
            from google.genai import types

            self._client = genai.Client(
                api_key=settings.gemini_api_key,
                http_options=types.HttpOptions(
                    timeout=int(settings.gemini_timeout * 1000)  # SDK wants ms
                ),
            )
            logger.info(
                "Gemini client ready (model=%s, timeout=%ss, key=%s)",
                self._model,
                settings.gemini_timeout,
                mask_secret(settings.gemini_api_key),
            )

    @property
    def model(self) -> str:
        """The currently active model (may change after fallback)."""
        return self._model

    def _fall_back(self, reason: str) -> bool:
        """Switch to the next fallback model; False when none remain."""
        if not self._fallbacks:
            return False
        nxt = self._fallbacks.pop(0)
        logger.warning("Model %s %s; falling back to %s", self._model, reason, nxt)
        self._model = nxt
        return True

    # ------------------------------------------------------------------ auth
    async def validate(self) -> str:
        """Validate the key with a real, cheap API call before first use.

        Confirms the key works and the configured model is reachable, falling
        back to :data:`FALLBACK_GEMINI_MODEL` if the primary is unavailable.
        Returns the resolved model name. Raises :class:`GeminiConfigurationError`
        with an actionable message on failure.
        """
        try:
            await self._client.aio.models.count_tokens(
                model=self._model, contents="ping"
            )
            self._validated = True
            logger.info("Gemini key validated (model=%s)", self._model)
            return self._model
        except Exception as exc:  # noqa: BLE001 - mapped below
            code = _status_code(exc)
            if code in (401, 403):
                raise GeminiConfigurationError(
                    KEY_INVALID_HELP.format(
                        code=code, masked=mask_secret(self._settings.gemini_api_key)
                    )
                ) from exc
            if code == 404:
                # Model retired/unavailable to this key — walk the fallback chain.
                if self._fall_back("unavailable (404)"):
                    return await self.validate()
                raise GeminiConfigurationError(
                    MODEL_UNAVAILABLE_HELP.format(model=self._model)
                ) from exc
            if code == 429:
                # Free-tier keys often have zero quota for pro-tier models while
                # a flash model works fine — walk the chain before failing.
                if self._fall_back("quota-limited (429)"):
                    return await self.validate()
                raise GeminiQuotaError(QUOTA_HELP) from exc
            raise

    # ------------------------------------------------------------ generation
    def _config(self, system_instruction: str, temperature: float | None,
                max_output_tokens: int | None):
        from google.genai import types

        return types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=(
                self._default_temperature if temperature is None else temperature
            ),
            max_output_tokens=max_output_tokens,
        )

    @staticmethod
    def _log_usage(response: object, *, model: str) -> None:
        usage = getattr(response, "usage_metadata", None)
        if usage is not None:
            logger.info(
                "Gemini usage (model=%s): prompt=%s output=%s thoughts=%s tokens",
                model,
                getattr(usage, "prompt_token_count", "?"),
                getattr(usage, "candidates_token_count", "?"),
                getattr(usage, "thoughts_token_count", None) or 0,
            )

    def _classify(self, exc: Exception) -> str | Exception:
        """Decide how to handle an API error.

        Returns ``"retry"`` (transient: 429/5xx/timeouts, or a 404 that was just
        resolved by falling back to the flash model), an actionable exception to
        raise immediately (bad key, model truly unavailable), or ``"raise"`` to
        re-raise the original error unchanged.
        """
        code = _status_code(exc)
        if code in (401, 403):
            return GeminiConfigurationError(
                KEY_INVALID_HELP.format(
                    code=code, masked=mask_secret(self._settings.gemini_api_key)
                )
            )
        if code == 404:
            if self._fall_back("unavailable mid-run (404)"):
                return "retry"  # retry immediately with the next fallback model
            return GeminiConfigurationError(
                MODEL_UNAVAILABLE_HELP.format(model=self._model)
            )
        if code == 429 or (code is not None and code >= 500):
            return "retry"
        if code is None:
            return "retry"  # httpx timeouts / transport errors carry no .code
        return "raise"

    async def generate(
        self,
        *,
        system_instruction: str,
        prompt: str,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        config = self._config(system_instruction, temperature, max_output_tokens)
        last_error: Exception | None = None

        for attempt in range(_MAX_RETRIES):
            try:
                response = await self._client.aio.models.generate_content(
                    model=self._model, contents=prompt, config=config
                )
                text = getattr(response, "text", None)
                if not text:
                    raise RuntimeError("Gemini returned an empty response")
                self._log_usage(response, model=self._model)
                return text.strip()
            except Exception as exc:  # noqa: BLE001 - classified below
                verdict = self._classify(exc)
                if isinstance(verdict, Exception):
                    raise verdict from exc
                if verdict == "raise":
                    raise
                last_error = exc
                if attempt < _MAX_RETRIES - 1:
                    wait = min(_BACKOFF_CAP, 2.0 ** (attempt + 1))
                    logger.warning(
                        "Gemini call failed (attempt %d/%d, %s); retrying in %.0fs",
                        attempt + 1,
                        _MAX_RETRIES,
                        type(exc).__name__,
                        wait,
                    )
                    await asyncio.sleep(wait)

        assert last_error is not None
        if _status_code(last_error) == 429:
            raise GeminiQuotaError(QUOTA_HELP) from last_error
        raise last_error

    async def generate_stream(
        self,
        *,
        system_instruction: str,
        prompt: str,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> AsyncIterator[str]:
        """Stream generated text chunk by chunk (same error mapping, no retry
        mid-stream — callers should retry the whole stream)."""
        config = self._config(system_instruction, temperature, max_output_tokens)
        try:
            stream = await self._client.aio.models.generate_content_stream(
                model=self._model, contents=prompt, config=config
            )
            last_chunk = None
            async for chunk in stream:
                last_chunk = chunk
                text = getattr(chunk, "text", None)
                if text:
                    yield text
            if last_chunk is not None:
                self._log_usage(last_chunk, model=self._model)
        except Exception as exc:  # noqa: BLE001
            verdict = self._classify(exc)
            if isinstance(verdict, Exception):
                raise verdict from exc
            if _status_code(exc) == 429:
                raise GeminiQuotaError(QUOTA_HELP) from exc
            raise
