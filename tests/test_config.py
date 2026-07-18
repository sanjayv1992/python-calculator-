import os
from pathlib import Path

import pytest

from agromanch_ai.config import DEFAULT_NOTEBOOK_NAME, Settings


def test_defaults():
    settings = Settings()
    assert settings.notebook_name == DEFAULT_NOTEBOOK_NAME
    assert settings.language == "hi"  # AgroManch audience is Indian farmers
    assert "Hindi" in settings.language_name
    assert "Purvanchal" in settings.region
    assert settings.notebook_id is None


def test_rejects_bad_language():
    with pytest.raises(ValueError):
        Settings(language="fr")


def test_from_env(monkeypatch):
    monkeypatch.setenv("AGROMANCH_NOTEBOOK_NAME", "My KB")
    monkeypatch.setenv("AGROMANCH_LANGUAGE", "hi")
    monkeypatch.setenv("AGROMANCH_NOTEBOOK_ID", "nb-123")
    monkeypatch.setenv("AGROMANCH_SOURCE_WAIT_TIMEOUT", "90")
    settings = Settings.from_env()
    assert settings.notebook_name == "My KB"
    assert settings.language == "hi"
    assert "Hindi" in settings.language_name
    assert settings.notebook_id == "nb-123"
    assert settings.source_wait_timeout == 90.0


def test_from_env_blank_falls_back(monkeypatch):
    monkeypatch.setenv("AGROMANCH_NOTEBOOK_NAME", "   ")
    monkeypatch.setenv("AGROMANCH_LANGUAGE", "")
    settings = Settings.from_env()
    assert settings.notebook_name == DEFAULT_NOTEBOOK_NAME
    assert settings.language == "hi"


def test_bad_float_env_raises(monkeypatch):
    monkeypatch.setenv("AGROMANCH_ARTIFACT_TIMEOUT", "soon")
    with pytest.raises(ValueError):
        Settings.from_env()


def test_gemini_defaults():
    settings = Settings()
    assert settings.gemini_model == "gemini-2.5-pro"  # max quality by default
    assert settings.gemini_timeout == 120.0
    assert settings.require_grounding is True
    assert settings.gemini_api_key is None


def test_env_file_loaded_by_from_env(monkeypatch, tmp_path):
    env = tmp_path / ".env"
    env.write_text('GEMINI_API_KEY="file-key"\nGEMINI_MODEL=gemini-2.5-flash\n')
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    settings = Settings.from_env()
    assert settings.gemini_api_key == "file-key"
    assert settings.gemini_model == "gemini-2.5-flash"


def test_env_file_does_not_override_environment(monkeypatch, tmp_path):
    (tmp_path / ".env").write_text("GEMINI_API_KEY=file-key\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", "env-key")
    assert Settings.from_env().gemini_api_key == "env-key"


def test_load_env_file_parsing(tmp_path, monkeypatch):
    from agromanch_ai.config import load_env_file

    env = tmp_path / "x.env"
    env.write_text(
        "# comment\n\nexport A_TEST_VAR='quoted value'\nB_TEST_VAR=plain\nBADLINE\n"
    )
    monkeypatch.delenv("A_TEST_VAR", raising=False)
    monkeypatch.delenv("B_TEST_VAR", raising=False)
    assert load_env_file(env) == 2
    import os

    assert os.environ["A_TEST_VAR"] == "quoted value"
    assert os.environ["B_TEST_VAR"] == "plain"
    monkeypatch.delenv("A_TEST_VAR")
    monkeypatch.delenv("B_TEST_VAR")


def test_mask_secret_never_reveals():
    from agromanch_ai.config import mask_secret

    assert mask_secret(None) == "(not set)"
    assert mask_secret("short") == "****"
    masked = mask_secret("AIzaSyFakeExampleKey12345")
    assert masked.startswith("AIza") and masked.endswith("45")
    assert "FakeExample" not in masked


def test_gemini_from_env(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-pro")
    monkeypatch.setenv("GEMINI_TEMPERATURE", "0.9")
    monkeypatch.setenv("AGROMANCH_REQUIRE_GROUNDING", "false")
    settings = Settings.from_env()
    assert settings.gemini_api_key == "test-key"
    assert settings.gemini_model == "gemini-2.5-pro"
    assert settings.gemini_temperature == 0.9
    assert settings.require_grounding is False


def test_bhojpuri_is_supported():
    settings = Settings(language="bho")
    assert "Bhojpuri" in settings.language_name


def test_language_directive_distinct_per_language():
    hi = Settings(language="hi").language_directive()
    bho = Settings(language="bho").language_directive()
    en = Settings(language="en").language_directive()
    assert hi != bho != en
    assert "Sanskritized" in hi  # natural, not textbook Hindi
    # Bhojpuri keeps SEO/blog searchable in Hindi/Hinglish
    assert "Hindi" in bho and "SEO" in bho


def test_region_from_env(monkeypatch):
    monkeypatch.setenv("AGROMANCH_REGION", "Marathwada")
    assert Settings.from_env().region == "Marathwada"


def test_gemini_google_api_key_fallback(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)  # isolate from any real .env in the repo root
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GOOGLE_API_KEY", "fallback-key")
    assert Settings.from_env().gemini_api_key == "fallback-key"


def test_ensure_output_dir(tmp_path):
    target = tmp_path / "out"
    settings = Settings(output_dir=target)
    result = settings.ensure_output_dir()
    assert result == target
    assert target.is_dir()
