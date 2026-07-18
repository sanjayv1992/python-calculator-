"""Shared test fakes: no API key, no network, fully offline.

The Gemini engine and NotebookLM retrieval are dependency-injected, so tests
substitute these fakes for the whole AI path.
"""

from __future__ import annotations

import pytest

from agromanch_ai.models import SourceRef, VerifiedContext


class FakeEngine:
    """A `TextEngine` that echoes a deterministic reply and records calls."""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def generate(
        self,
        *,
        system_instruction: str,
        prompt: str,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        self.calls.append(
            {"system": system_instruction, "prompt": prompt, "temperature": temperature}
        )
        # Echo the topic line so tests can assert grounding/consistency.
        topic_line = next(
            (ln for ln in prompt.splitlines() if ln.startswith("TOPIC:")), "TOPIC: ?"
        )
        return f"GENERATED (temp={temperature}) for {topic_line}"


class FakeRetrieval:
    """A `RetrievalService` returning a preset `VerifiedContext`."""

    def __init__(self, context: VerifiedContext) -> None:
        self._context = context
        self.calls: list[tuple[str, str]] = []

    async def get_context(
        self, notebook_id: str, topic: str, *, source_ids=None
    ) -> VerifiedContext:
        self.calls.append((notebook_id, topic))
        # Preserve the requested topic on the returned context.
        return VerifiedContext(
            topic=topic,
            context_text=self._context.context_text,
            references=list(self._context.references),
            grounded=self._context.grounded,
        )


@pytest.fixture
def grounded_context() -> VerifiedContext:
    return VerifiedContext(
        topic="seed",
        context_text="Rice BLB is caused by Xanthomonas oryzae.",
        references=[SourceRef("s1", 1, "Rice BLB")],
        grounded=True,
    )


@pytest.fixture
def empty_context() -> VerifiedContext:
    return VerifiedContext(topic="seed", context_text="", references=[], grounded=False)


@pytest.fixture
def fake_engine() -> FakeEngine:
    return FakeEngine()
