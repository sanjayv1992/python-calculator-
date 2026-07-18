"""NotebookLM authentication: reusable session verification + expiry detection.

What is actually supported (honestly): Google exposes **no public OAuth API for
NotebookLM**, so authentication is a **reusable authenticated session** managed
by `notebooklm-py` and stored on disk (``storage_state.json``). It is created
once via any of three real flows:

1. **Interactive browser login** — ``notebooklm login`` (opens Google sign-in).
2. **Browser cookie reuse** — ``notebooklm login --browser-cookies chrome``
   (imports cookies from an existing logged-in browser; no Playwright needed).
3. **Master token** — ``notebooklm login --master-token --account you@example.com``
   (mints fresh session cookies on demand; suited to headless servers/CI).

After login the stored session is reused by every run (``NotebookLMClient
.from_storage()``); ``notebooklm auth refresh`` keeps it alive on schedules.
This module verifies the session with a **real API call** and converts an
expired/broken session into a clear, actionable error. Credentials are never
printed or logged.
"""

from __future__ import annotations

import sys
from pathlib import Path

LOGIN_HELP = """\
No NotebookLM authentication found.

Create the reusable session once with the notebooklm-py CLI:

    pip install "notebooklm-py[browser]"   # or: uv tool install "notebooklm-py[browser]"
    notebooklm login                        # opens a Google sign-in browser window
    notebooklm auth check --test            # verify it works

Headless server? Use `notebooklm login --browser-cookies chrome` to import
cookies from a logged-in browser, or `notebooklm login --master-token` for
unattended environments. Then re-run this command. See docs/setup.md.
"""

EXPIRED_HELP = (
    "NotebookLM session is expired or invalid (Google rejected the stored "
    "cookies). Re-authenticate with `notebooklm login` (or `notebooklm auth "
    "refresh` if you use a master token), then retry. See docs/setup.md."
)


class NotebookLMAuthError(RuntimeError):
    """Missing or expired NotebookLM session, with an actionable message."""


def storage_path(profile: str | None = None) -> Path:
    """Path of the stored session for a profile (may not exist)."""
    from notebooklm import paths

    return Path(paths.get_storage_path(profile))


def has_stored_session(profile: str | None = None) -> bool:
    return storage_path(profile).exists()


def require_stored_session(profile: str | None = None) -> Path:
    """Return the session path or raise :class:`NotebookLMAuthError`."""
    path = storage_path(profile)
    if not path.exists():
        raise NotebookLMAuthError(LOGIN_HELP)
    return path


async def verify_notebooklm_auth(profile: str | None = None) -> int:
    """Verify the stored session with a REAL API call.

    Opens a client from storage and lists notebooks. Returns the notebook count
    on success. Raises :class:`NotebookLMAuthError` when the session is missing
    or expired (detected via the library's auth errors), so callers always get a
    clear, actionable message instead of a stack trace.
    """
    require_stored_session(profile)
    from notebooklm import AuthError, NotebookLMClient
    from notebooklm.exceptions import AuthExtractionError

    try:
        async with NotebookLMClient.from_storage(profile=profile) as client:
            notebooks = await client.notebooks.list()
            return len(notebooks)
    except (AuthError, AuthExtractionError) as exc:
        raise NotebookLMAuthError(EXPIRED_HELP) from exc


def ensure_authenticated(profile: str | None = None) -> Path:
    """Exit with a helpful message unless stored NotebookLM auth exists.

    Kept for example scripts (prints instead of raising). Returns the
    storage-state path when a stored session is present. Note this checks
    presence only; :func:`verify_notebooklm_auth` performs the live check.
    """
    try:
        return require_stored_session(profile)
    except NotebookLMAuthError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
