"""Validate the AgroManch production environment end to end.

Checks (PASS/FAIL each, secrets always masked):

  1. GEMINI_API_KEY exists (.env or environment)
  2. Gemini request succeeds (real API call; model fallback exercised)
  3. NotebookLM authentication works (real API call on the stored session)
  4. Notebook exists (AGROMANCH_NOTEBOOK_ID, or by name)
  5. Retrieval succeeds (RetrievalService against the notebook)
  6. Grounded context returned (non-empty context with citations)

On full success prints:  Gemini Connected / NotebookLM Connected /
Grounded Retrieval Working / Factory Ready.  Otherwise explains what failed.

Run from the repo root:
    python scripts/check_environment.py [--topic "..."]
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from agromanch_ai.ai.engine import (
    GeminiConfigurationError,
    GeminiEngine,
    GeminiQuotaError,
)
from agromanch_ai.config import Settings, mask_secret
from agromanch_ai.utils.authcheck import (
    NotebookLMAuthError,
    verify_notebooklm_auth,
)

PASS = "PASS"
FAIL = "FAIL"


def _report(label: str, ok: bool, detail: str = "") -> bool:
    mark = PASS if ok else FAIL
    print(f"[{mark}] {label}" + (f" — {detail}" if detail else ""))
    return ok


async def run_checks(topic: str) -> int:
    settings = Settings.from_env()
    failures: list[str] = []

    # 1. Key exists ---------------------------------------------------------
    ok = bool(settings.gemini_api_key)
    _report(
        "GEMINI_API_KEY exists",
        ok,
        f"key: {mask_secret(settings.gemini_api_key)}" if ok
        else "set it in .env or the environment (see docs/setup.md)",
    )
    if not ok:
        failures.append("GEMINI_API_KEY is missing")

    # 2. Gemini request succeeds -------------------------------------------
    gemini_ok = False
    if settings.gemini_api_key:
        try:
            engine = GeminiEngine(settings)
            model = await engine.validate()
            reply = await engine.generate(
                system_instruction="Reply with exactly: OK",
                prompt="Say OK.",
                temperature=0.0,
                max_output_tokens=64,
            )
            gemini_ok = bool(reply)
            _report("Gemini request succeeds", gemini_ok, f"model: {model}")
        except (GeminiConfigurationError, GeminiQuotaError) as exc:
            _report("Gemini request succeeds", False, str(exc))
            failures.append(f"Gemini: {exc}")
        except Exception as exc:  # noqa: BLE001
            _report("Gemini request succeeds", False, f"{type(exc).__name__}: {exc}")
            failures.append(f"Gemini: {exc}")
    else:
        _report("Gemini request succeeds", False, "skipped (no key)")
        failures.append("Gemini request skipped: no key")

    # 3. NotebookLM authentication works ------------------------------------
    nlm_ok = False
    try:
        count = await verify_notebooklm_auth(settings.profile)
        nlm_ok = True
        _report("NotebookLM authentication works", True, f"{count} notebook(s) visible")
    except NotebookLMAuthError as exc:
        first_line = str(exc).strip().splitlines()[0]
        _report("NotebookLM authentication works", False, first_line)
        failures.append(f"NotebookLM auth: {first_line}")
    except Exception as exc:  # noqa: BLE001
        _report("NotebookLM authentication works", False, f"{type(exc).__name__}: {exc}")
        failures.append(f"NotebookLM auth: {exc}")

    # 4-6. Notebook exists, retrieval, grounded context ----------------------
    if nlm_ok:
        from notebooklm import NotebookLMClient

        from agromanch_ai.services import NotebookService, RetrievalService

        try:
            async with NotebookLMClient.from_storage(profile=settings.profile) as client:
                notebooks = NotebookService(client, settings)
                if settings.notebook_id:
                    nb = await client.notebooks.get_or_none(settings.notebook_id)
                    nb_ok = nb is not None
                    detail = (
                        f"id {settings.notebook_id} -> {nb.title!r}" if nb
                        else f"AGROMANCH_NOTEBOOK_ID {settings.notebook_id} not found"
                    )
                else:
                    nb = next(
                        (n for n in await client.notebooks.list()
                         if n.title == settings.notebook_name),
                        None,
                    )
                    nb_ok = nb is not None
                    detail = (
                        f"found {settings.notebook_name!r} ({nb.id})" if nb
                        else f"no notebook titled {settings.notebook_name!r} — run "
                        "scripts/index_knowledge.py to create and fill it"
                    )
                _report("Notebook exists", nb_ok, detail)
                if not nb_ok:
                    failures.append(f"Notebook: {detail}")

                if nb_ok and nb is not None:
                    retrieval = RetrievalService(client, settings)
                    try:
                        ctx = await retrieval.get_context(nb.id, topic)
                        _report("Retrieval succeeds", True, f"topic: {topic!r}")
                        grounded = ctx.grounded and not ctx.is_empty
                        _report(
                            "Grounded context returned",
                            grounded,
                            f"{len(ctx.references)} citation(s)" if grounded
                            else "no relevant context — index documents on this "
                            "topic (scripts/index_knowledge.py)",
                        )
                        if not grounded:
                            failures.append("Retrieval returned no grounded context")
                    except Exception as exc:  # noqa: BLE001
                        _report("Retrieval succeeds", False, f"{type(exc).__name__}: {exc}")
                        _report("Grounded context returned", False, "skipped")
                        failures.append(f"Retrieval: {exc}")
                else:
                    _report("Retrieval succeeds", False, "skipped (no notebook)")
                    _report("Grounded context returned", False, "skipped (no notebook)")
        except Exception as exc:  # noqa: BLE001
            for label in ("Notebook exists", "Retrieval succeeds", "Grounded context returned"):
                _report(label, False, f"{type(exc).__name__}: {exc}")
            failures.append(f"NotebookLM session: {exc}")
    else:
        for label in ("Notebook exists", "Retrieval succeeds", "Grounded context returned"):
            _report(label, False, "skipped (NotebookLM not authenticated)")

    # Summary ----------------------------------------------------------------
    print()
    if not failures:
        print("Gemini Connected")
        print("NotebookLM Connected")
        print("Grounded Retrieval Working")
        print("Factory Ready")
        return 0
    print("Environment NOT ready. What failed:")
    for f in failures:
        print(f"  - {f}")
    print("\nFix guide: docs/setup.md (or run: python scripts/setup.py)")
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the AgroManch environment")
    parser.add_argument(
        "--topic", default="Fall Armyworm in maize",
        help="Topic used for the retrieval check",
    )
    args = parser.parse_args()
    sys.exit(asyncio.run(run_checks(args.topic)))


if __name__ == "__main__":
    main()
