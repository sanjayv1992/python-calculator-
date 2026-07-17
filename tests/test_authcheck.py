"""NotebookLM auth verification tests (no real session, no network)."""

import pytest

from agromanch_ai.utils.authcheck import (
    NotebookLMAuthError,
    ensure_authenticated,
    has_stored_session,
    require_stored_session,
    verify_notebooklm_auth,
)


@pytest.fixture
def fake_storage(monkeypatch, tmp_path):
    """Point notebooklm's storage path at a temp file we control."""
    path = tmp_path / "storage_state.json"
    monkeypatch.setattr(
        "notebooklm.paths.get_storage_path", lambda profile=None: path
    )
    return path


def test_missing_session_detected(fake_storage):
    assert not has_stored_session()
    with pytest.raises(NotebookLMAuthError) as e:
        require_stored_session()
    assert "notebooklm login" in str(e.value)


def test_present_session_passes_presence_check(fake_storage):
    fake_storage.write_text("{}")
    assert has_stored_session()
    assert require_stored_session() == fake_storage
    assert ensure_authenticated() == fake_storage


def test_ensure_authenticated_exits_cleanly_when_missing(fake_storage, capsys):
    with pytest.raises(SystemExit) as e:
        ensure_authenticated()
    assert e.value.code == 1
    assert "notebooklm login" in capsys.readouterr().err


async def test_verify_raises_clear_error_without_session(fake_storage):
    with pytest.raises(NotebookLMAuthError):
        await verify_notebooklm_auth()


async def test_verify_maps_expired_session_to_clear_error(fake_storage, monkeypatch):
    fake_storage.write_text("{}")
    from notebooklm import AuthError

    class FailingCtx:
        async def __aenter__(self):
            raise AuthError("cookies rejected")
        async def __aexit__(self, *a):
            return False

    monkeypatch.setattr(
        "notebooklm.NotebookLMClient.from_storage",
        staticmethod(lambda profile=None, **kw: FailingCtx()),
    )
    with pytest.raises(NotebookLMAuthError) as e:
        await verify_notebooklm_auth()
    assert "expired" in str(e.value).lower()
    assert "notebooklm login" in str(e.value)
