"""Production-hardening tests for GeminiEngine (fake client, no key/network)."""

from types import SimpleNamespace

import pytest

from agromanch_ai.ai.engine import (
    GeminiConfigurationError,
    GeminiEngine,
    GeminiQuotaError,
)
from agromanch_ai.config import Settings


class FakeAPIError(Exception):
    """Mimics google.genai.errors.APIError: carries an HTTP .code."""

    def __init__(self, code: int):
        self.code = code
        super().__init__(f"HTTP {code}")


class FakeClient:
    """Scriptable stand-in for genai.Client (aio.models.*)."""

    def __init__(self, script=None, count_tokens_script=None):
        self.script = list(script or [])       # per generate_content call
        self.ct_script = list(count_tokens_script or [])
        self.calls: list[str] = []             # models used per generate call
        ns = SimpleNamespace(
            generate_content=self._generate,
            count_tokens=self._count_tokens,
        )
        self.aio = SimpleNamespace(models=ns)

    async def _generate(self, *, model, contents, config):
        self.calls.append(model)
        action = self.script.pop(0) if self.script else "ok"
        if isinstance(action, Exception):
            raise action
        return SimpleNamespace(
            text="generated text",
            usage_metadata=SimpleNamespace(
                prompt_token_count=10, candidates_token_count=20,
                thoughts_token_count=None,
            ),
        )

    async def _count_tokens(self, *, model, contents):
        action = self.ct_script.pop(0) if self.ct_script else "ok"
        if isinstance(action, Exception):
            raise action
        return SimpleNamespace(total_tokens=1)


def make_engine(client, **kw) -> GeminiEngine:
    return GeminiEngine(Settings(gemini_api_key="test-key", **kw), client=client)


def test_missing_key_raises_helpful_error():
    with pytest.raises(GeminiConfigurationError) as e:
        GeminiEngine(Settings(gemini_api_key=None))
    assert "GEMINI_API_KEY is not set" in str(e.value)
    assert "aistudio.google.com" in str(e.value)


async def test_validate_success_and_model():
    engine = make_engine(FakeClient())
    assert await engine.validate() == "gemini-2.5-pro"


async def test_validate_invalid_key_masks_secret():
    engine = make_engine(FakeClient(count_tokens_script=[FakeAPIError(403)]))
    with pytest.raises(GeminiConfigurationError) as e:
        await engine.validate()
    msg = str(e.value)
    assert "invalid" in msg.lower() or "rejected" in msg.lower()
    assert "test-key" not in msg  # never print the secret


async def test_validate_falls_back_to_flash_on_404():
    engine = make_engine(FakeClient(count_tokens_script=[FakeAPIError(404), "ok"]))
    assert await engine.validate() == "gemini-2.5-flash"


async def test_generate_retries_then_succeeds(monkeypatch):
    async def no_sleep(_):
        pass
    monkeypatch.setattr("asyncio.sleep", no_sleep)
    client = FakeClient(script=[FakeAPIError(500), FakeAPIError(429), "ok"])
    engine = make_engine(client)
    out = await engine.generate(system_instruction="s", prompt="p")
    assert out == "generated text"
    assert len(client.calls) == 3  # two retries, then success


async def test_generate_quota_exhausted_raises_quota_error(monkeypatch):
    async def no_sleep(_):
        pass
    monkeypatch.setattr("asyncio.sleep", no_sleep)
    client = FakeClient(script=[FakeAPIError(429)] * 10)
    engine = make_engine(client)
    with pytest.raises(GeminiQuotaError) as e:
        await engine.generate(system_instruction="s", prompt="p")
    assert "quota" in str(e.value).lower()
    assert "billing" in str(e.value).lower()  # actionable fix


async def test_generate_model_fallback_mid_run(monkeypatch):
    async def no_sleep(_):
        pass
    monkeypatch.setattr("asyncio.sleep", no_sleep)
    client = FakeClient(script=[FakeAPIError(404), "ok"])
    engine = make_engine(client)
    out = await engine.generate(system_instruction="s", prompt="p")
    assert out == "generated text"
    assert client.calls == ["gemini-2.5-pro", "gemini-2.5-flash"]


async def test_generate_invalid_key_is_fatal_no_retry():
    client = FakeClient(script=[FakeAPIError(401)])
    engine = make_engine(client)
    with pytest.raises(GeminiConfigurationError):
        await engine.generate(system_instruction="s", prompt="p")
    assert len(client.calls) == 1  # no retries on auth failure
