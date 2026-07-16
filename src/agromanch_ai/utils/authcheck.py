"""Friendly pre-flight check for NotebookLM authentication.

`notebooklm-py` stores browser-login state on disk (``notebooklm login``).
Every example calls :func:`ensure_authenticated` first so users get a clear
next step instead of a stack trace when they haven't logged in yet.
"""

from __future__ import annotations

import sys
from pathlib import Path

LOGIN_HELP = """\
No NotebookLM authentication found.

Set it up once with the notebooklm-py CLI:

    pip install "notebooklm-py[browser]"   # or: uv tool install "notebooklm-py[browser]"
    notebooklm login                        # opens a Google sign-in browser window
    notebooklm auth check --test            # verify it works

Headless server? Use `notebooklm login --browser-cookies chrome` to import
cookies from a logged-in browser, or `notebooklm login --master-token` for
unattended environments. Then re-run this script.
"""


def ensure_authenticated(profile: str | None = None) -> Path:
    """Exit with a helpful message unless stored NotebookLM auth exists.

    Returns the storage-state path when authentication is present.
    """
    from notebooklm import paths  # imported lazily to keep startup errors clear

    storage = paths.get_storage_path(profile)
    if not Path(storage).exists():
        print(LOGIN_HELP, file=sys.stderr)
        raise SystemExit(1)
    return Path(storage)
