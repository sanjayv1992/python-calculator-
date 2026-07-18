import json
from datetime import date

from agromanch_ai.knowledge.catalog import build_catalog

DOC_A = """\
---
title: Rice BLB
category: crop_diseases
crop: rice
source_org: ICAR
publication_date: "2024-01-01"
last_verified_date: "2024-06-01"
language: en
keywords: [paddy, dhaan]
hindi_names: [धान झुलसा]
summary: BLB in rice.
references: [ICAR bulletin]
important_facts: [lesions]
recommended_practices: [resistant variety]
---
# Rice BLB
Unique body A about bacterial leaf blight in rice fields.
"""

# Same title+crop+source as A → duplicate.
DOC_DUP = DOC_A.replace("Unique body A", "Slightly different body")

DOC_OLD = """\
---
title: Old Mandi Note
category: mandi
crop: soybean
source_org: Agmarknet
publication_date: "2015-01-01"
last_verified_date: "2015-01-01"
language: hi
keywords: [mandi]
summary: Old price note.
references: [agmarknet]
---
# Old note
Prices long ago.
"""


def _write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_catalog_dedup_outdated_and_searchable(tmp_path):
    _write(tmp_path, "crop_diseases/a.md", DOC_A)
    _write(tmp_path, "crop_diseases/dup.md", DOC_DUP)
    _write(tmp_path, "mandi/old.md", DOC_OLD)
    _write(tmp_path, "crop_diseases/README.md", "# folder readme (skipped)")

    entries, summary = build_catalog(tmp_path, today=date(2024, 8, 1))

    assert summary.total == 3  # README skipped
    assert len(summary.duplicates) == 1
    assert any("old.md" in p for p in summary.outdated)

    # catalog.json written with searchable multilingual terms
    catalog = json.loads((tmp_path / "catalog.json").read_text())
    assert catalog["summary"]["total"] == 3
    a_entry = next(e for e in entries if e["path"].endswith("a.md"))
    joined = " ".join(a_entry["search_terms"]).lower()
    assert "paddy" in joined and "धान" in " ".join(a_entry["search_terms"])
    assert a_entry["usable"] is True

    dup_entry = next(e for e in entries if e["path"].endswith("dup.md"))
    assert dup_entry["duplicate"] is True
    assert dup_entry["usable"] is False


def test_catalog_empty_dir(tmp_path):
    entries, summary = build_catalog(tmp_path, today=date(2024, 8, 1), write=False)
    assert entries == []
    assert summary.total == 0
    assert summary.avg_score == 0.0
