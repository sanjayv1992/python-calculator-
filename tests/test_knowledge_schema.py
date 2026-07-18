from pathlib import Path

from agromanch_ai.knowledge.schema import Category, KnowledgeDocument

REPO = Path(__file__).resolve().parent.parent
KNOWLEDGE = REPO / "knowledge"


def test_category_folder_mapping():
    assert Category.HERBICIDES.value == "weed_management"
    assert Category.from_folder("insects") is Category.INSECTS
    # 19 categories, 18 distinct folders (Herbicides shares weed_management)
    assert len(list(Category)) == 19
    assert "nutrient_deficiency" in Category.folders()
    assert "farm_machinery" in Category.folders()


def test_seed_docs_parse_and_validate():
    docs = list(KNOWLEDGE.rglob("*.md"))
    seed = [p for p in docs if p.name != "README.md"]
    assert seed, "expected seed knowledge docs"
    for path in seed:
        doc = KnowledgeDocument.from_file(path)
        assert doc.title, f"{path} missing title"
        assert doc.category in Category.folders(), f"{path} bad category"
        assert doc.language in ("hi", "en", "bho")
        assert doc.validate() == [], f"{path}: {doc.validate()}"


def test_search_terms_multilingual():
    doc = KnowledgeDocument.from_file(
        KNOWLEDGE / "insects" / "maize_fall_armyworm.md"
    )
    terms = " ".join(doc.search_terms()).lower()
    assert "fall armyworm" in terms
    assert "spodoptera" in terms  # scientific name
    assert any("keeda" in t.lower() for t in doc.search_terms())  # local/hindi


def test_dedup_key_and_hash_stable():
    doc = KnowledgeDocument(title="T", category="crops", crop="rice", source_org="ICAR")
    assert doc.dedup_key() == "t|rice|icar"
    assert doc.content_hash() == KnowledgeDocument(
        title="T", category="crops", crop="rice", source_org="ICAR"
    ).content_hash()
