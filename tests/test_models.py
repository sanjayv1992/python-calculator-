from agromanch_ai.models import CitedAnswer, GeneratedContent, SourceRef


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
