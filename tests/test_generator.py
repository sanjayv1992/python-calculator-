import pytest

from agromanch_ai.ai.generator import AgroManchGenerator, GroundingError
from agromanch_ai.config import Settings
from conftest import FakeRetrieval


def make_generator(context, engine, **settings_kw):
    settings = Settings(**settings_kw)
    return AgroManchGenerator(FakeRetrieval(context), engine, settings), settings


@pytest.mark.asyncio
async def test_run_generates_grounded_content(grounded_context, fake_engine):
    gen, _ = make_generator(grounded_context, fake_engine)
    result = await gen.run("instagram_carousel", topic="rice BLB", notebook_id="nb1")
    assert result.kind == "instagram_carousel"
    assert result.grounded is True
    assert result.references[0].source_id == "s1"
    # The verified context was injected into the Gemini prompt.
    assert "Xanthomonas" in fake_engine.calls[0]["prompt"]


@pytest.mark.asyncio
async def test_run_requires_grounding_by_default(empty_context, fake_engine):
    gen, _ = make_generator(empty_context, fake_engine)
    with pytest.raises(GroundingError):
        await gen.run("blog", topic="unknown crop", notebook_id="nb1")
    assert fake_engine.calls == []  # never called Gemini


@pytest.mark.asyncio
async def test_run_override_allows_unverified(empty_context, fake_engine):
    gen, _ = make_generator(empty_context, fake_engine)
    result = await gen.run(
        "blog", topic="unknown crop", notebook_id="nb1", require_grounding=False
    )
    assert result.grounded is False
    assert "UNVERIFIED" in result.to_markdown()
    assert len(fake_engine.calls) == 1


@pytest.mark.asyncio
async def test_run_reuses_passed_context_without_retrieval(grounded_context, fake_engine):
    retrieval = FakeRetrieval(grounded_context)
    gen = AgroManchGenerator(retrieval, fake_engine, Settings())
    await gen.run("hook", topic="rice", context=grounded_context)
    assert retrieval.calls == []  # context reused, no retrieval call


@pytest.mark.asyncio
async def test_run_passes_temperature_from_spec(grounded_context, fake_engine):
    gen, _ = make_generator(grounded_context, fake_engine)
    await gen.run("research_summary", topic="rice", notebook_id="nb1")
    assert fake_engine.calls[0]["temperature"] == 0.3  # research_summary spec temp


@pytest.mark.asyncio
async def test_run_needs_notebook_or_context(grounded_context, fake_engine):
    gen, _ = make_generator(grounded_context, fake_engine)
    with pytest.raises(ValueError):
        await gen.run("hook", topic="rice")
