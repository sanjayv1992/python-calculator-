"""Smoke tests: every module and example script imports/compiles offline.

These guard against typos and API drift. The Gemini and NotebookLM clients are
never constructed here (no key, no network) — only imports and compilation.
"""

import compileall
import importlib
from pathlib import Path

import pytest

PACKAGE_MODULES = [
    "agromanch_ai",
    "agromanch_ai.config",
    "agromanch_ai.logging",
    "agromanch_ai.models",
    "agromanch_ai.ai",
    "agromanch_ai.ai.engine",
    "agromanch_ai.ai.generator",
    "agromanch_ai.ai.pipeline",
    "agromanch_ai.prompts",
    "agromanch_ai.prompts.spec",
    "agromanch_ai.prompts.advisory_prompts",
    "agromanch_ai.prompts.content_prompts",
    "agromanch_ai.services",
    "agromanch_ai.services.notebook_service",
    "agromanch_ai.services.retrieval_service",
    "agromanch_ai.services.content_service",
    "agromanch_ai.services.advisory_service",
    "agromanch_ai.services.artifact_service",
    "agromanch_ai.utils",
    "agromanch_ai.utils.authcheck",
    "agromanch_ai.utils.dose",
    "agromanch_ai.utils.text",
    "agromanch_ai.utils.seasonal",
    "agromanch_ai.utils.angles",
    "agromanch_ai.utils.quality_report",
    "agromanch_ai.prompts.brand",
    "agromanch_ai.knowledge",
    "agromanch_ai.knowledge.frontmatter",
    "agromanch_ai.knowledge.schema",
    "agromanch_ai.knowledge.sources",
    "agromanch_ai.knowledge.quality",
    "agromanch_ai.knowledge.catalog",
    "agromanch_ai.knowledge.registry",
    "agromanch_ai.intelligence",
    "agromanch_ai.intelligence.trend_library",
    "agromanch_ai.intelligence.angle_generator",
    "agromanch_ai.intelligence.competitor",
    "agromanch_ai.analytics",
    "agromanch_ai.analytics.history",
    "agromanch_ai.analytics.learning",
    "agromanch_ai.analytics.performance",
    "agromanch_ai.review",
    "agromanch_ai.review.base",
    "agromanch_ai.review.writer",
    "agromanch_ai.review.fact_checker",
    "agromanch_ai.review.marketing_reviewer",
    "agromanch_ai.review.seo_reviewer",
    "agromanch_ai.review.readability_reviewer",
    "agromanch_ai.review.quality_manager",
    "agromanch_ai.prompts.review_prompts",
    "agromanch_ai.personas",
    "agromanch_ai.planning",
    "agromanch_ai.planning.campaign",
    "agromanch_ai.planning.calendar",
    "agromanch_ai.planning.planner",
    "agromanch_ai.planning.queue",
    "agromanch_ai.planning.gaps",
    "agromanch_ai.planning.evergreen",
    "agromanch_ai.planning.recommend",
    "agromanch_ai.planning.reports",
]

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.parametrize("module", PACKAGE_MODULES)
def test_package_module_imports(module):
    assert importlib.import_module(module) is not None


def test_examples_and_scripts_compile():
    for folder in ("examples", "scripts"):
        target = REPO_ROOT / folder
        assert compileall.compile_dir(str(target), quiet=1), f"{folder} failed to compile"
