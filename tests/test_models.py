from agromanch_ai.models import (
    CitedAnswer,
    ContentBundle,
    GeneratedContent,
    SourceRef,
    VerifiedContext,
)


def test_source_ref_label():
    assert SourceRef("s1", 2, "ICAR Guide").label() == "[2] ICAR Guide"
    assert SourceRef("s9").label() == "s9"


def test_cited_answer_markdown_with_sources():
    answer = CitedAnswer(
        question="What is BLB?",
        answer="Bacterial leaf blight is a disease of rice.",
        references=[SourceRef("s1", 1, "Rice BLB")],
    )
    md = answer.to_markdown()
    assert "What is BLB?" in md
    assert "**Sources:**" in md
    assert "[1] Rice BLB" in md


def test_cited_answer_markdown_without_sources():
    answer = CitedAnswer(question="Q", answer="A")
    assert "Sources" not in answer.to_markdown()


def test_generated_content_markdown_and_dict():
    content = GeneratedContent(
        kind="instagram_carousel",
        topic="drip irrigation",
        body="SLIDE 1 ...",
        references=[SourceRef("s2", 1, "Drip guide")],
    )
    md = content.to_markdown()
    assert "Instagram Carousel" in md
    assert "Knowledge sources" in md
    assert content.to_dict()["kind"] == "instagram_carousel"


def test_generated_content_unverified_warning():
    content = GeneratedContent(kind="blog", topic="x", body="...", grounded=False)
    assert "UNVERIFIED" in content.to_markdown()


def test_verified_context_prompt_block_and_empty():
    ctx = VerifiedContext(
        topic="rice", context_text="Rice needs water.",
        references=[SourceRef("s1", 1, "Rice guide")],
    )
    block = ctx.to_prompt_block()
    assert "VERIFIED CONTEXT" in block
    assert "Rice needs water." in block
    assert "Rice guide" in block
    assert not ctx.is_empty

    empty = VerifiedContext(topic="x", context_text="   ")
    assert empty.is_empty
    assert "none" in empty.to_prompt_block().lower()


def test_content_bundle_manifest_and_publishing_map():
    ctx = VerifiedContext(
        topic="drip", context_text="facts", references=[SourceRef("s1", 1, "Guide")]
    )
    bundle = ContentBundle(topic="drip", context=ctx)
    bundle.items["instagram_carousel"] = GeneratedContent(
        kind="instagram_carousel", topic="drip", body="SLIDE 1"
    )
    bundle.items["cta"] = GeneratedContent(kind="cta", topic="drip", body="Join!")

    manifest = bundle.manifest()
    assert manifest["topic"] == "drip"
    assert manifest["grounded"] is True
    assert "instagram_carousel" in manifest["items"]
    assert manifest["sources"][0]["source_id"] == "s1"

    pmap = bundle.publishing_map()
    assert pmap["instagram"] == ["instagram_carousel", "cta"]
    assert bundle.get("cta").body == "Join!"
