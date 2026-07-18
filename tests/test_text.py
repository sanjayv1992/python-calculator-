from dataclasses import dataclass

from agromanch_ai.utils.text import references_from_ask_result, safe_filename


def test_safe_filename():
    assert safe_filename("Fall Armyworm in Maize!") == "Fall_Armyworm_in_Maize"
    assert safe_filename("") == "untitled"
    assert safe_filename("a/b\\c") == "a_b_c"
    assert len(safe_filename("x" * 200)) == 80


@dataclass
class _Ref:
    source_id: str
    citation_number: int | None = None
    cited_text: str | None = None


@dataclass
class _Result:
    references: list


def test_references_dedup_and_sort():
    result = _Result(
        references=[
            _Ref("s2", 2, "second"),
            _Ref("s1", 1, "first"),
            _Ref("s1", 1, "duplicate"),  # dropped
            _Ref(None, 3),  # skipped
        ]
    )
    refs = references_from_ask_result(result, {"s1": "Doc One", "s2": "Doc Two"})
    assert [r.source_id for r in refs] == ["s1", "s2"]
    assert refs[0].title == "Doc One"
    assert refs[0].cited_text == "first"


def test_references_empty():
    assert references_from_ask_result(_Result(references=[])) == []
    assert references_from_ask_result(object()) == []
