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
