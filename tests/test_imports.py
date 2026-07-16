"""Smoke tests: every module and example script imports without network access.

These guard against typos and API drift in the reusable code. Example scripts
under examples/agromanch/ import `_common`, so they are exercised by compiling
rather than importing (importing would require the package's sibling path).
"""

import importlib
import compileall
from pathlib import Path

import pytest

PACKAGE_MODULES = [
    "agromanch_ai",
    "agromanch_ai.config",
    "agromanch_ai.logging",
    "agromanch_ai.models",
    "agromanch_ai.prompts",
    "agromanch_ai.prompts.advisory_prompts",
    "agromanch_ai.prompts.content_prompts",
    "agromanch_ai.services",
    "agromanch_ai.services.notebook_service",
    "agromanch_ai.services.chat_service",
    "agromanch_ai.services.content_service",
    "agromanch_ai.services.artifact_service",
    "agromanch_ai.utils",
    "agromanch_ai.utils.authcheck",
    "agromanch_ai.utils.dose",
    "agromanch_ai.utils.text",
]

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("module", PACKAGE_MODULES)
def test_package_module_imports(module):
    assert importlib.import_module(module) is not None


def test_examples_and_scripts_compile():
    for folder in ("examples", "scripts"):
        target = REPO_ROOT / folder
        assert compileall.compile_dir(str(target), quiet=1), f"{folder} failed to compile"
