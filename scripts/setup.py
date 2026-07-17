"""Guided production setup for the AgroManch AI Content Factory.

Walks through: 1) enter Gemini API key -> 2) verify it with a real call ->
3) authenticate NotebookLM (reusable session) -> 4) choose a notebook ->
5) save configuration to .env (0600, never echoed) -> 6) run full validation.

Security: input is hidden (getpass), values are masked everywhere, nothing is
logged or committed. Run from the repo root:

    python scripts/setup.py
"""

from __future__ import annotations

import asyncio
import getpass
import os
import subprocess
import sys
from pathlib import Path

from agromanch_ai.config import Settings, load_env_file, mask_secret

ENV_PATH = Path(".env")


def _say(step: str, text: str) -> None:
    print(f"\n=== Step {step}: {text} ===")


# ---------------------------------------------------------------- step 1 + 2
def get_and_verify_key() -> tuple[str, str]:
    """Prompt for the key (hidden input) and verify it with a real API call."""
    _say("1", "Gemini API key")
    load_env_file(ENV_PATH)
    existing = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if existing:
        keep = input(
            f"A key is already configured ({mask_secret(existing)}). Keep it? [Y/n] "
        ).strip().lower()
        key = existing if keep in ("", "y", "yes") else ""
    else:
        key = ""
    while not key:
        key = getpass.getpass(
            "Paste your Gemini API key (input hidden; get one at "
            "https://aistudio.google.com/apikey): "
        ).strip()

    _say("2", "Verify Gemini API")
    os.environ["GEMINI_API_KEY"] = key
    from agromanch_ai.ai.engine import (
        GeminiConfigurationError,
        GeminiEngine,
        GeminiQuotaError,
    )

    while True:
        try:
            engine = GeminiEngine(Settings.from_env())
            model = asyncio.run(engine.validate())
            print(f"  Key OK ({mask_secret(key)}); model: {model}")
            return key, model
        except (GeminiConfigurationError, GeminiQuotaError) as exc:
            print(f"  Verification failed: {exc}")
            key = getpass.getpass("Paste a working Gemini API key (hidden): ").strip()
            os.environ["GEMINI_API_KEY"] = key


# -------------------------------------------------------------------- step 3
def authenticate_notebooklm(profile: str | None) -> None:
    _say("3", "Authenticate NotebookLM")
    from agromanch_ai.utils.authcheck import (
        NotebookLMAuthError,
        has_stored_session,
        verify_notebooklm_auth,
    )

    while True:
        if has_stored_session(profile):
            try:
                count = asyncio.run(verify_notebooklm_auth(profile))
                print(f"  Session OK — {count} notebook(s) visible.")
                return
            except NotebookLMAuthError as exc:
                print(f"  {str(exc).strip().splitlines()[0]}")
        else:
            print("  No stored NotebookLM session found.")
        choice = input(
            "  Run `notebooklm login` now (opens a Google sign-in browser)? [Y/n] "
        ).strip().lower()
        if choice in ("", "y", "yes"):
            try:
                subprocess.run(["notebooklm", "login"], check=True)
            except FileNotFoundError:
                sys.exit(
                    "  `notebooklm` CLI not found. Install it first:\n"
                    '    pip install "notebooklm-py[browser]"\n'
                    "  then re-run python scripts/setup.py. See docs/setup.md."
                )
            except subprocess.CalledProcessError as exc:
                print(f"  Login exited with {exc.returncode}; trying verification anyway.")
        else:
            sys.exit(
                "  NotebookLM authentication is required (retrieval layer). "
                "Run `notebooklm login` and re-run setup. See docs/setup.md."
            )


# -------------------------------------------------------------------- step 4
def choose_notebook(settings: Settings) -> tuple[str, str]:
    """List real notebooks and let the user pick; returns (id, title)."""
    _say("4", "Choose the knowledge-base notebook")
    from notebooklm import NotebookLMClient

    async def _list():
        async with NotebookLMClient.from_storage(profile=settings.profile) as client:
            return await client.notebooks.list()

    notebooks = asyncio.run(_list())
    if not notebooks:
        print(
            "  No notebooks yet. Setup will use the default name; run "
            "`python scripts/index_knowledge.py` afterwards to create and fill it."
        )
        return "", settings.notebook_name
    for i, nb in enumerate(notebooks, 1):
        print(f"  {i}. {nb.title}  ({nb.id})")
    print(f"  0. Create later with the default name {settings.notebook_name!r}")
    while True:
        raw = input(f"  Pick [0-{len(notebooks)}]: ").strip()
        if raw.isdigit() and 0 <= int(raw) <= len(notebooks):
            n = int(raw)
            if n == 0:
                return "", settings.notebook_name
            nb = notebooks[n - 1]
            return nb.id, nb.title


# -------------------------------------------------------------------- step 5
def save_config(key: str, model: str, notebook_id: str) -> None:
    _say("5", "Save configuration to .env")
    managed = ("GEMINI_API_KEY", "GEMINI_MODEL", "AGROMANCH_NOTEBOOK_ID")

    def _key_of(line: str) -> str:
        name = line.split("=", 1)[0].strip()
        return name[len("export "):].strip() if name.startswith("export ") else name

    lines: list[str] = []
    if ENV_PATH.exists():
        lines = [
            l for l in ENV_PATH.read_text(encoding="utf-8").splitlines()
            if _key_of(l) not in managed
        ]
    lines += [f"GEMINI_API_KEY={key}", f"GEMINI_MODEL={model}"]
    if notebook_id:
        lines.append(f"AGROMANCH_NOTEBOOK_ID={notebook_id}")
    ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(ENV_PATH, 0o600)
    print(f"  Wrote {ENV_PATH} (mode 600). Key stored as {mask_secret(key)} — "
          "never commit this file (.gitignore already excludes it).")


def main() -> None:
    print("AgroManch AI Content Factory — production setup")
    key, model = get_and_verify_key()
    settings = Settings.from_env()
    authenticate_notebooklm(settings.profile)
    notebook_id, title = choose_notebook(settings)
    print(f"  Using notebook: {title!r}" + (f" ({notebook_id})" if notebook_id else ""))
    save_config(key, model, notebook_id)

    _say("6", "Run full validation")
    result = subprocess.run([sys.executable, "scripts/check_environment.py"])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
