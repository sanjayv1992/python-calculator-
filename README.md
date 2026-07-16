# AgroManch AI Knowledge Engine

A production-oriented **AI knowledge platform for Indian agriculture**, built on
Google NotebookLM (via the unofficial [`notebooklm-py`](https://github.com/teng-lin/notebooklm-py)
library). It turns a verified library of ICAR / State Agricultural University /
KVK documents, government-scheme PDFs, and product labels into **grounded,
cited** answers and farmer-facing content.

This repository is the foundation for AgroManch's AI services — not a throwaway
demo. It is modular and async-first so future APIs, AI models, weather/mandi
providers, and the AgroManch mobile app can integrate without restructuring.

## What AgroManch uses this for

| Capability | What it does | Where |
| ---------- | ------------ | ----- |
| **Crop Doctor knowledge** | Diagnose crop problems from symptoms, grounded in disease docs | `examples/agromanch/crop_doctor_assistant.py` |
| **Farmer AI chat** | Grounded Q&A over the whole knowledge base, Hindi/English | `examples/agromanch/farmer_chatbot.py` |
| **Disease & pest knowledge** | Identification, thresholds, integrated management | `pest_disease_chat.py` |
| **Agriculture research** | Fertilizer, weather, mandi, livestock advisories | `fertilizer_advisor.py`, `weather_crop_advisor.py`, `mandi_price_research.py` |
| **Government Scheme Assistant** | Eligibility & application help from scheme PDFs | `govt_scheme_assistant.py` |
| **Dealer / advisory assistant** | Label-accurate dose guidance + offline field math | `pesticide_dose_calculator.py` |
| **Content generation** | Carousels, WhatsApp, YouTube, blogs, podcasts | `examples/agromanch/*_generator.py` |
| **Internal knowledge search & management** | Bulk-index and query a verified KB | `scripts/index_knowledge.py` |
| **Future AI services** | Clean service seams for the roadmap | [docs/roadmap.md](docs/roadmap.md) |

Every answer is **grounded only in the indexed documents and returns source
citations**, so advice is auditable — essential for agriculture.

## How it works

```
Farmer question → NotebookLM Knowledge Base → verified, cited answer
      → (future Gemini orchestration) → Crop Doctor / Dose Calculator /
        Weather / Mandi / Scheme & Dealer Assistants / Content Generator
      → AgroManch mobile app
```

See [docs/architecture.md](docs/architecture.md) for the full diagram and each
layer's role. The reusable code lives in `src/agromanch_ai/`; the runnable
workflows live in `examples/`.

## Project structure

```
src/agromanch_ai/      Reusable, installable package
  config.py            Env-driven settings (AGROMANCH_*)
  logging.py           Structured logging
  models.py            Typed results (CitedAnswer, GeneratedContent, DoseRecommendation)
  services/            Async services wrapping notebooklm-py
  prompts/             Versioned advisory & content prompt templates
  utils/               Auth check, offline dose math, text/citation helpers
examples/              Runnable workflows
  quickstart.py, research_to_podcast.py, study_kit.py   Generic NotebookLM demos
  agromanch/           14 AgroManch workflows (crop doctor, dose calc, content…)
knowledge/             Verified knowledge base, 16 domains (indexed into NotebookLM)
docs/                  architecture, knowledge-sources, mcp-setup, roadmap
scripts/index_knowledge.py   Idempotent bulk importer
tests/                Offline unit & smoke tests
```

## Setup

### 1. Install

```bash
# Recommended: isolated CLI + browser automation for login
uv tool install "notebooklm-py[browser]"      # or: pipx install "notebooklm-py[browser]"

# Install this project (from the repo root)
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,browser]"
```

### 2. Authenticate with Google (one-time)

```bash
notebooklm login              # opens a browser for Google sign-in
notebooklm auth check --test  # verify

# Headless server alternatives:
notebooklm login --browser-cookies chrome     # reuse a logged-in browser
notebooklm login --master-token --account you@example.com   # unattended/CI
```

### 3. Build the knowledge base

Add authoritative documents to `knowledge/<domain>/` (see
[docs/knowledge-sources.md](docs/knowledge-sources.md)), then index:

```bash
python scripts/index_knowledge.py
export AGROMANCH_NOTEBOOK_ID=<id printed by the script>   # optional, speeds up runs
```

How indexing works: each document in `knowledge/` becomes a NotebookLM
*source*. `.md`/`.txt` are added as text, `.pdf`/office files are uploaded, and
`urls.txt` files add web sources. NotebookLM parses, chunks, and embeds them;
queries retrieve the most relevant chunks and answer **only** from them,
returning citations. The importer is idempotent — re-run it as you add
documents. Details in [knowledge/README.md](knowledge/README.md).

### 4. Configure (optional)

Copy `.env.example` to `.env` and adjust `AGROMANCH_*` variables (notebook name,
language `en`/`hi`, output directory, timeouts). No secrets go here — Google auth
is handled entirely by `notebooklm login`.

### 5. Run a workflow

```bash
python examples/agromanch/crop_doctor_assistant.py --crop rice --region "West Bengal"
python examples/agromanch/pesticide_dose_calculator.py --offline --acres 2.5
python examples/agromanch/instagram_carousel_generator.py --topic "drip irrigation"
python examples/agromanch/farmer_chatbot.py
```

## Use from Claude / MCP

The knowledge base is queryable directly from Claude Code / claude.ai via the
NotebookLM MCP server — including content generation. Setup and example prompts
(*"Explain Fall Armyworm in Hindi"*, *"Generate an Instagram carousel"*,
*"Create a WhatsApp farmer message"*) are in [docs/mcp-setup.md](docs/mcp-setup.md).

## Testing

Offline unit and smoke tests (no Google login needed) cover config, prompt
rendering, models, dose math, citation extraction, and imports:

```bash
pytest
```

Live NotebookLM workflows require `notebooklm login` and are exercised by
running the example scripts.

## Roadmap

Phase 1 (this repo) → Farmer AI Chat → Crop Doctor AI → Content Automation →
Podcast Generation → Voice AI → AgroManch AI Operating System. See
[docs/roadmap.md](docs/roadmap.md).

## Disclaimer

`notebooklm-py` uses **undocumented Google APIs** that can change without
notice and is **not affiliated with Google**. Treat this platform as
prototype-grade for research and internal use. Agricultural advice generated
here must be reviewed against official sources; always follow registered
pesticide labels and confirm critical decisions with your local KVK or
agriculture officer.
