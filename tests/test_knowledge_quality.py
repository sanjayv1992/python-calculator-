from datetime import date

from agromanch_ai.knowledge.quality import band, is_outdated, score_document
from agromanch_ai.knowledge.schema import KnowledgeDocument
from agromanch_ai.knowledge.sources import source_rank


def _doc(**kw):
    base = dict(
        title="Doc", category="crops", crop="rice", season="Kharif",
        state="Bihar", source_org="ICAR", publication_date="2024-01-01",
        last_verified_date="2024-06-01", language="en",
        summary="s", keywords=["k"], important_facts=["f"],
        recommended_practices=["p"], references=["r"],
        scientific_names=["Oryza sativa"], hindi_names=["dhaan"],
        local_names=["dhan"], district="Patna",
    )
    base.update(kw)
    return KnowledgeDocument(**base)


TODAY = date(2024, 8, 1)


def test_icar_complete_recent_scores_high():
    score = score_document(_doc(), TODAY)
    assert score >= 75
    assert band(score) == "High"


def test_missing_references_lowers_score():
    with_refs = score_document(_doc(), TODAY)
    without = score_document(_doc(references=[]), TODAY)
    assert without < with_refs


def test_outdated_lowers_score():
    fresh = score_document(_doc(), TODAY)
    old = score_document(
        _doc(publication_date="2010-01-01", last_verified_date="2010-01-01"), TODAY
    )
    assert old < fresh


def test_source_rank_order():
    assert source_rank("ICAR-IIRR") < source_rank("Krishi Vigyan Kendra")
    assert source_rank("KVK") < source_rank("Some Random Blog")
    assert source_rank(None) > len(("a",) * 10)  # unknown ranks lowest


def test_outdated_detection_by_category_window():
    # mandi has a 1-year freshness window
    mandi = _doc(category="mandi", publication_date="2022-01-01",
                 last_verified_date="2022-01-01")
    assert is_outdated(mandi, TODAY)


def test_undated_treated_as_outdated():
    assert is_outdated(_doc(publication_date="", last_verified_date=""), TODAY)
