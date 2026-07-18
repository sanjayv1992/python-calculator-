from agromanch_ai.knowledge.frontmatter import parse_frontmatter

DOC = """\
---
title: Rice BLB
category: crop_diseases
crop: rice
keywords:
  - paddy
  - dhaan
scientific_names: [Xanthomonas oryzae]
summary: "A quoted summary"
---

# Body heading

Some body text.
"""


def test_parses_scalars_lists_and_body():
    meta, body = parse_frontmatter(DOC)
    assert meta["title"] == "Rice BLB"
    assert meta["category"] == "crop_diseases"
    assert meta["keywords"] == ["paddy", "dhaan"]
    assert meta["scientific_names"] == ["Xanthomonas oryzae"]
    assert meta["summary"] == "A quoted summary"  # quotes stripped
    assert body.startswith("# Body heading")


def test_no_frontmatter_returns_empty_meta():
    meta, body = parse_frontmatter("# Just a doc\n\ntext")
    assert meta == {}
    assert body.startswith("# Just a doc")


def test_unterminated_block_is_ignored():
    meta, body = parse_frontmatter("---\ntitle: X\n(no close)")
    assert meta == {}
