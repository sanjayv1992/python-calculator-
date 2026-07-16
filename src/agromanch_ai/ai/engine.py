"""Gemini text-generation engine — the central AI of the content factory.

`GeminiEngine` wraps the `google-genai` SDK. Everything downstream depends only
on the small :class:`TextEngine` protocol, so tests inject a fake engine and run
without an API key or network.
"""

from __future__ import annotations

import asyncio
from typing import Protocol, runtime_checkable

from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger

logger = get_logger("gemini")


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


class GeminiEngine:
    """`TextEngine` backed by Google Gemini via the `google-genai` SDK.

    The underlying `genai.Client` is dependency-injectable (`client=`), which is
    how tests substitute a fake. In normal use it is built from
    ``GEMINI_API_KEY``.
    """

    def __init__(self, settings: Settings, *, client: object | None = None) -> None:
        self._settings = settings
        self._model = settings.gemini_model
        self._default_temperature = settings.gemini_temperature
        self._max_retries = 3
        if client is not None:
            self._client = client
        else:
            if not settings.gemini_api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is not set. Export it (see .env.example) to "
                    "use the Gemini content engine."
                )
            from google import genai  # imported lazily so import works without the key

            self._client = genai.Client(api_key=settings.gemini_api_key)

    async def generate(
        self,
        *,
        system_instruction: str,
        prompt: str,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        from google.genai import types

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=(
                self._default_temperature if temperature is None else temperature
            ),
            max_output_tokens=max_output_tokens,
        )

        last_error: Exception | None = None
        for attempt in range(self._max_retries):
            try:
                response = await self._client.aio.models.generate_content(
                    model=self._model, contents=prompt, config=config
                )
                text = getattr(response, "text", None)
                if not text:
                    raise RuntimeError("Gemini returned an empty response")
                return text.strip()
            except Exception as exc:  # noqa: BLE001 - retry transient failures
                last_error = exc
                wait = 2**attempt
                logger.warning(
                    "Gemini call failed (attempt %d/%d): %s; retrying in %ds",
                    attempt + 1,
                    self._max_retries,
                    exc,
                    wait,
                )
                if attempt < self._max_retries - 1:
                    await asyncio.sleep(wait)
        assert last_error is not None
        raise last_error
