# AgroManch Knowledge Base

This folder is the **verified agricultural knowledge base** that powers every
AgroManch AI workflow. Its documents are indexed into a Google NotebookLM
notebook, and all farmer-facing answers are grounded in — and cite — these
documents.

## Document metadata (frontmatter)

Every knowledge document starts with a YAML-style frontmatter block so it is
self-describing and machine-catalogued:

```markdown
---
title: Rice — Bacterial Leaf Blight (BLB)
category: crop_diseases
crop: rice
season: Kharif
state: Bihar
district: ""
source_org: ICAR-IIRR
publication_date: "2023-06-01"
last_verified_date: "2024-07-01"
language: en            # hi | en | bho
scientific_names: [Xanthomonas oryzae pv. oryzae]
hindi_names: [धान का जीवाणु झुलसा]
local_names: [patauwa jhulsa]
keywords: [rice disease, bacterial leaf blight, dhaan rog]
summary: One-line summary.
important_facts: [ ... ]
recommended_practices: [ ... ]
dosage: ""              # for agrochemicals, exactly per label
warnings: [ ... ]
references: [ ... ]
---
```

## Catalog, quality score, dedup & freshness

`python scripts/build_catalog.py` scans the library, gives each document a
**quality score (0-100)** from source trust + metadata completeness + references +
recency, **detects duplicates** (same title+crop+source or identical body) and
**outdated** documents (past a per-category freshness window), and writes a
searchable `knowledge/catalog.json`. The NotebookLM indexer consults this catalog
and **only feeds trusted, fresh, non-duplicate, sufficiently-scored knowledge**
into the Content Factory. Trusted-source priority and the curated collection
registry are documented in [../docs/knowledge-sources.md](../docs/knowledge-sources.md).

## How indexing works

NotebookLM treats each document as a *source*. `scripts/index_knowledge.py`
walks this folder and, for every domain subfolder, adds its documents to the
AgroManch notebook:

| File type in a domain folder | Becomes a NotebookLM source |
| ---------------------------- | --------------------------- |
| `.md`, `.txt`                | Text source (title = path relative to `knowledge/`) |
| `.pdf`, `.docx`, `.pptx`, `.csv` | Uploaded file source |
| `urls.txt` (one URL per line) | One web source per URL (`#` lines ignored) |
| `README.md`                  | Skipped — describes the folder, not knowledge |

NotebookLM then parses, chunks, and embeds each source. When a farmer asks a
question, it retrieves the most relevant chunks and answers **only** from
them, returning citation references that AgroManch surfaces as sources. The
importer is **idempotent** (it skips sources whose title already exists), so
you can re-run it whenever you add documents.

```bash
# one-time auth, then:
python scripts/index_knowledge.py
# pin the notebook it prints for faster subsequent runs:
export AGROMANCH_NOTEBOOK_ID=<printed id>
```

## Domains

Each subfolder is one knowledge domain, with its own `README.md` describing the
documents it should hold and the trusted sources they should come from:

`crops/` · `crop_diseases/` · `insects/` · `fertilizers/` · `pesticides/` ·
`weed_management/` · `government_schemes/` · `weather/` · `mandi/` ·
`crop_calendar/` · `soil_health/` · `irrigation/` · `animal_husbandry/` ·
`fisheries/` · `organic_farming/` · `post_harvest/`

The included `.md` files are **small starter samples** so the demos have real
content to cite. Replace and expand them with authoritative documents from the
sources listed in [docs/knowledge-sources.md](../docs/knowledge-sources.md).

> **Verification matters.** Agricultural advice affects livelihoods and safety.
> Only add documents from official, verifiable sources, keep pesticide/label
> information exactly as registered, and review content before indexing.
