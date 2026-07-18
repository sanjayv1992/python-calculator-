# AgroManch AI Content Factory

An **AI Content Factory for Indian agriculture**. **Gemini** generates the
highest-quality farmer content; **NotebookLM** supplies verified context from
trusted documents (ICAR, KVK, government PDFs, product labels). One unified,
grounded pipeline powers both content generation and farmer advisory.

```
Research → NotebookLM (retrieval + citations) → Verified Context
   → Gemini (generation) → full 15-asset content bundle
   → one-click Publishing (Instagram · Facebook · YouTube Shorts · WhatsApp · Telegram)
```

Every content request produces a complete, publish-ready bundle grounded in — and
citing — trusted sources.

## What one request produces

1. Research Summary · 2. Instagram Carousel · 3. Carousel Image Prompts ·
4. Facebook Post · 5. WhatsApp Broadcast · 6. YouTube Shorts Script ·
7. Veo Video Prompt · 8. Voiceover Script · 9. Subtitle File (SRT) ·
10. SEO Keywords · 11. Blog · 12. Podcast Script · 13. Thumbnail Prompt ·
14. Story Prompt · 15. CTA — plus standalone Hooks, an Image Prompt, and a Reel
shot list.

`publish()` lays these out into per-platform folders and a `manifest.json` for a
one-click publishing worker.

## What AgroManch uses this for

| Capability | Where |
| ---------- | ----- |
| **Content factory** (all 15 assets for a topic) | `examples/agromanch/content_factory.py` |
| **Single-asset generation** (carousel, blog, Shorts, …) | `instagram_carousel_generator.py`, `blog_generator.py`, `youtube_script_generator.py` |
| **Multilingual broadcasts** (Hindi + English) | `whatsapp_post_generator.py` |
| **Crop Doctor knowledge** | `crop_doctor_assistant.py` |
| **Farmer AI chat** | `farmer_chatbot.py` |
| **Disease & pest, fertilizer, weather, mandi** | `pest_disease_chat.py`, `fertilizer_advisor.py`, `weather_crop_advisor.py`, `mandi_price_research.py` |
| **Government Scheme / Dealer assistant** | `govt_scheme_assistant.py`, `pesticide_dose_calculator.py` |
| **Internal knowledge search & indexing** | `scripts/index_knowledge.py` |

Content and advisory share **one AI path** — NotebookLM retrieves, Gemini
generates. Advisory outputs are the seeds of the future Crop Doctor, Farmer Chat,
Dealer, and Scheme assistants.

## Premium content quality (built in)

Every generated package is shaped by a permanent quality system, applied
automatically through the single prompt-injection seam:

- **AgroManch Brand Style Guide** (`prompts/brand.py`) — one voice, seven
  mandatory pillars (Emotional Hook, Practical Value, Scientific Accuracy, Local
  Context, Clear CTA, High Shareability, High Saveability), and per-format rules
  (carousel Problem→Cause→Solution→CTA, 3-second reel hooks, forwardable WhatsApp,
  story-driven YouTube, art-directed image/Veo prompts).
- **Language & region** — default **Hindi** (natural village Hindi, not
  textbook), plus **Bhojpuri** (`bho`) for spoken/social assets while SEO+blog
  stay searchable in Hindi/Hinglish; localised to **Purvanchal/UP/Bihar**
  (`AGROMANCH_REGION`).
- **Seasonal Intelligence** (`utils/seasonal.py`) — content auto-adapts to the
  current agricultural season (crops, growth stage, pest pressure, farmer
  activities) for the region.
- **Viral angle** (`utils/angles.py`) — each package gets one fresh marketing
  angle so the same crop never yields repetitive content.
- **Internal Quality Report** — `publish()` writes `quality_report.txt` (research
  confidence, grounding, per-platform potential, overall /100) at the bundle
  root; it never appears in the public per-platform posts.

## Autonomous content operations

Beyond generating content, AgroManch decides **what / when / why / where / how**
(deterministic, JSON-backed, offline — `python scripts/plan_content.py --days 30`):

- **Content Strategy Planner** (`planning/planner.py`) — 7/30/90-day plans from
  season, crop calendar, active campaigns, and priorities.
- **Editorial Calendar** (`planning/calendar.py`) — `editorial_calendar.json`,
  deduplicated topics, crop/format balance, status tracking.
- **Campaign Engine** (`planning/campaign.py`) — Rice/Wheat Season, Crop Doctor
  Awareness, Pashu Bazaar, Schemes, Weather Alerts, Festival — each with goal,
  audience, KPIs, assets and frequency.
- **Publishing Queue** (`planning/queue.py`) — `publishing_queue.json` prioritised
  by seasonal urgency, government/weather alerts, viral potential and knowledge
  confidence, with per-item platform recommendations.
- **Gap Analyzer** (`planning/gaps.py`) — missing crops/categories/personas →
  what to create next.
- **Evergreen classifier** (`planning/evergreen.py`) and **Recommendation layer**
  (`planning/recommend.py`) — best format/hook/time/CTA/hashtags/campaign.
- **Farmer Persona Engine** (`personas.py`) — 9 personas; `AGROMANCH_PERSONA`
  adapts language, CTA and examples in every prompt.
- Internal reports: `strategy_report.txt`, `editorial_report.txt`,
  `gap_report.txt`, `campaign_report.txt`.

## Self-improving layer (Gemini-only)

- **Multi-Agent Review** (`review/`) — after generation, four Gemini reviewers
  (fact-checker, marketing, SEO, readability) score the hero asset across 8
  categories; the Quality Manager aggregates to an overall /100 and **rewrites up
  to 3 times** toward a 95+ score, keeping the best version. Writes an internal
  `review_report.txt`. Toggle with `AGROMANCH_REVIEW` (default on). Reviewers are
  Gemini calls — no second model.
- **Competitor Intelligence** (`intelligence/`) — a curated library of viral
  content *structures* (no scraping). Each package gets a fresh **primary +
  secondary angle**, and a "borrow structure, never copy wording" inspiration
  block is injected into prompts.
- **Performance Learning** (`analytics/`) — record real performance with
  `scripts/record_performance.py`; the learning engine ranks the best hook / CTA /
  carousel-structure / hashtags / pacing / caption styles and injects a
  `learning_directive` so future generations prefer what performed best. Local
  JSON, fully deterministic. Each publish also writes `learning_snapshot.json`
  explaining the creative choices.

## Knowledge Library

`knowledge/` is a structured, verifiable library across 19 categories. Each
document carries rich frontmatter metadata (title, category, crop, season, state,
district, source, dates, scientific/Hindi/local names, keywords, summary, facts,
practices, dosage, warnings, references). `python scripts/build_catalog.py`
scores every document, flags duplicates and outdated docs, and writes a searchable
`knowledge/catalog.json`; the indexer then feeds only trusted, fresh, non-duplicate
knowledge into NotebookLM. Trusted-source priority (ICAR → SAU → KVK → Govt → IMD →
Agmarknet → eNAM → labels → NABARD → FSSAI) and a curated source registry
(`knowledge/registry.py`) are documented in
[docs/knowledge-sources.md](docs/knowledge-sources.md).

## Grounding rule

By default, generation **requires** NotebookLM-verified context, so agricultural
output stays accurate and cited. Pass `--no-grounding` (or set
`AGROMANCH_REQUIRE_GROUNDING=false`) to allow Gemini-only output — which is
clearly marked **UNVERIFIED**.

## Project structure

```
src/agromanch_ai/
  ai/            Gemini engine, unified generator, content-factory pipeline
  services/      retrieval (NotebookLM), content, advisory, notebook, artifact(legacy)
  prompts/       versioned PromptSpec templates (content + advisory)
  models.py      VerifiedContext, GeneratedContent, ContentBundle, DoseRecommendation
  config.py      env-driven settings (AGROMANCH_* + GEMINI_*)
  utils/         auth check, offline dose math, citation/text helpers
examples/
  agromanch/     content_factory + 14 workflows (content & advisory)
  quickstart.py …   raw notebooklm-py library basics (not the AgroManch path)
knowledge/       verified knowledge base, 16 domains (indexed into NotebookLM)
docs/            architecture · knowledge-sources · mcp-setup · roadmap
scripts/index_knowledge.py   idempotent bulk importer
tests/           offline unit + smoke tests (fakes for Gemini & NotebookLM)
```

## Setup

**Guided path (recommended):** `python scripts/setup.py` walks through the Gemini
key, NotebookLM login, notebook selection, saving `.env`, and full validation.
Re-check anytime with `python scripts/check_environment.py` (PASS/FAIL per check,
ends with **Factory Ready**). Guides: **[FIRST_RUN.md](FIRST_RUN.md)** (zero →
Factory Ready), **[RUN_PRODUCTION.md](RUN_PRODUCTION.md)** (generating real
content), **[TEST_PRODUCTION.md](TEST_PRODUCTION.md)** (verifying every layer),
[docs/setup.md](docs/setup.md) (credentials + troubleshooting).

### 1. Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,browser]"     # includes google-genai + notebooklm-py[browser]
```

### 2. Credentials — two of them

```bash
# NotebookLM (retrieval): one-time Google sign-in
notebooklm login
notebooklm auth check --test

# Gemini (generation): get a key from Google AI Studio
export GEMINI_API_KEY=your-key       # or GOOGLE_API_KEY
```

Copy `.env.example` to `.env` to configure the model (`gemini-2.5-flash` default,
`gemini-2.5-pro` for max quality), language (`en`/`hi`), grounding rule, and
output directory.

### 3. Build the knowledge base

Add authoritative documents to `knowledge/<domain>/` (see
[docs/knowledge-sources.md](docs/knowledge-sources.md)), then index:

```bash
python scripts/index_knowledge.py
export AGROMANCH_NOTEBOOK_ID=<id printed by the script>   # optional, speeds up runs
```

Indexing: each document becomes a NotebookLM *source*; the retrieval layer pulls
the relevant, cited facts per topic and hands them to Gemini. Details in
[knowledge/README.md](knowledge/README.md).

### 4. Run the factory

```bash
python examples/agromanch/content_factory.py --topic "Fall Armyworm control in maize"
# advisory on the same pipeline:
python examples/agromanch/crop_doctor_assistant.py --crop rice --region "West Bengal"
python examples/agromanch/pesticide_dose_calculator.py --offline --acres 2.5
```

## Use from Claude / MCP

The verified knowledge base is queryable from Claude Code / claude.ai via the
NotebookLM MCP server — useful for exploring sources and drafting interactively.
Setup and example prompts are in [docs/mcp-setup.md](docs/mcp-setup.md).

## Testing

Offline unit + smoke tests (no API key, no network — Gemini and NotebookLM are
faked): grounding logic, the full 15-asset bundle and publishing manifest, prompt
rendering, models, dose math, and imports.

```bash
pytest
```

Live runs require `notebooklm login` + `GEMINI_API_KEY` and are exercised by the
example scripts.

## Roadmap

Content Factory (this repo) → Farmer AI Chat → Crop Doctor AI → Content
Automation at scale → Media Generation (Imagen/Veo/TTS) → Voice AI → AgroManch AI
Operating System. See [docs/roadmap.md](docs/roadmap.md).

## Scope & disclaimer

Every bundle item is Gemini **text** — copy, scripts, SRT, and *prompts* for
images/video. Rendering images (Imagen), video (Veo), or audio (TTS) and posting
to platforms are documented integration seams, not part of the core pipeline.

`notebooklm-py` uses **undocumented Google APIs** that can change without notice
and is **not affiliated with Google**. Treat this as prototype-grade for research
and internal use. Review all generated agricultural content against official
sources; always follow registered pesticide labels and confirm critical decisions
with your local KVK or agriculture officer.
