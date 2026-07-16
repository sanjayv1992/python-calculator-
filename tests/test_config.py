import os
from pathlib import Path

import pytest

from agromanch_ai.config import DEFAULT_NOTEBOOK_NAME, Settings


def test_defaults():
    settings = Settings()
    assert settings.notebook_name == DEFAULT_NOTEBOOK_NAME
    assert settings.language == "en"
    assert settings.language_name.startswith("English")
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
    assert settings.language == "en"


def test_bad_float_env_raises(monkeypatch):
    monkeypatch.setenv("AGROMANCH_ARTIFACT_TIMEOUT", "soon")
    with pytest.raises(ValueError):
        Settings.from_env()


def test_ensure_output_dir(tmp_path):
    target = tmp_path / "out"
    settings = Settings(output_dir=target)
    result = settings.ensure_output_dir()
    assert result == target
    assert target.is_dir()
