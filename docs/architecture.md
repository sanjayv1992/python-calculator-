# AgroManch AI Architecture

AgroManch is an **AI Content Factory** for Indian agriculture. **Gemini is the
central AI engine** that generates every output; **NotebookLM is a retrieval-only
layer** that supplies verified context from trusted documents (ICAR, KVK,
government PDFs, labels). There is exactly **one AI path** for both content and
advisory — no second pipeline.

## The unified pipeline

```
      Research (trusted agricultural documents: ICAR / KVK / Gov / labels)
                                │  indexed once
                                ▼
                 ┌──────────────────────────────┐
                 │   NotebookLM  (RETRIEVAL)     │
                 │   grounded facts + citations  │
                 └──────────────┬───────────────┘
                                ▼
                       Verified Context
                                ▼
                 ┌──────────────────────────────┐
                 │   Gemini API  (GENERATION)    │  the central engine
                 └──────────────┬───────────────┘
                                ▼
   ┌───────────────────── full content bundle (15 assets) ─────────────────────┐
   │ Research Summary · Instagram Carousel · Carousel Image Prompts · Facebook  │
   │ WhatsApp · YouTube Shorts Script · Veo Video Prompt · Voiceover Script     │
   │ Subtitle (SRT) · SEO Keywords · Blog · Podcast Script · Thumbnail Prompt   │
   │ Story Prompt · CTA   (+ Hook, Image Prompt, Reel shot list)                │
   └───────────────────────────────┬───────────────────────────────────────────┘
                                    ▼
            AgroManch one-click Publishing (manifest + per-platform folders)
        Instagram · Facebook · YouTube Shorts · WhatsApp · Telegram
```

The same path serves advisory features (Crop Doctor, Farmer Chat, Dealer &
Government Scheme assistants): retrieve verified context → Gemini writes the
farmer-friendly answer.

## Layers

### 1. Knowledge Base (NotebookLM — retrieval only)
`knowledge/` is indexed into a NotebookLM notebook by
`scripts/index_knowledge.py`. `RetrievalService.get_context()` asks NotebookLM to
**extract** the relevant facts + citations for a topic — it never writes final
copy. If the documents don't cover a topic it returns empty context, which the
grounding rule acts on. Single source of truth: see
[knowledge-sources.md](knowledge-sources.md).

### 2. Gemini engine (`src/agromanch_ai/ai/engine.py`)
`GeminiEngine` wraps the `google-genai` SDK and implements the small
`TextEngine` protocol (`generate(system_instruction, prompt, temperature)`). The
client is dependency-injected, so tests run with a fake — no key, no network.
Model and temperature come from `GEMINI_MODEL` / `GEMINI_TEMPERATURE`.

### 3. Unified generator (`src/agromanch_ai/ai/generator.py`)
`AgroManchGenerator.run(task, topic, …)` is the single brain:
retrieve `VerifiedContext` → enforce the **grounding rule** (required by default;
`--no-grounding` / `require_grounding=False` produces clearly-marked *UNVERIFIED*
output) → render the task's `PromptSpec` with the context injected → Gemini
generates → wrap with the context's citations.

### 4. Content Factory (`src/agromanch_ai/ai/pipeline.py`)
`ContentFactory.produce()` retrieves context **once** and reuses it across all 15
assets (consistency + grounding + fewer NotebookLM calls), returning a
`ContentBundle`. `publish()` is the **one-click publishing handoff**: a markdown
file per asset, per-platform folders (`instagram/`, `facebook/`,
`youtube_shorts/`, `whatsapp/`, `telegram/`), and a `manifest.json` a publishing
worker can consume.

### 5. Prompts (`src/agromanch_ai/prompts/`)
Every task is a versioned `PromptSpec` (system instruction + user template +
temperature) tuned for content quality: audience, exact channel format, quality
bar, language, and a strict grounding instruction. Image/video specs emit
**generator-ready prompts** (subject, scene, style, aspect ratio, negatives) for
downstream Imagen/Veo.

### 6. Services (`src/agromanch_ai/services/`)
Thin wrappers over the generator: `ContentService` (single assets),
`AdvisoryService` (Crop Doctor, pest/disease, fertilizer, pesticide label,
weather, mandi, scheme, livestock, ask), `RetrievalService` (NotebookLM),
`NotebookService` (indexing). `ArtifactService` (NotebookLM audio/quiz) is kept
**optional/legacy**, outside the core path.

## Scope boundary — media rendering
Every bundle item is Gemini **text**: copy, scripts, SRT subtitles, and *prompts*
for images/video. Actually rendering images (Imagen), video (Veo), or audio (TTS)
needs those APIs with enabled billing and is a **documented integration seam**
(wired via `google-genai` when keys are present), not part of the core, verifiable
pipeline.

## Integration seams for the future
- **API layer** — wrap the services/factory in FastAPI/gRPC under `src/agromanch_ai/api/`; models already serialize via `to_dict()` / `manifest()`.
- **Media generation** — plug Imagen/Veo/TTS into `publish()` to turn prompts/scripts into rendered assets.
- **Publishing** — replace the manifest handoff with real Instagram/Facebook/YouTube/WhatsApp/Telegram API posting.
- **Weather / mandi providers** — feed live bulletins into retrieval as sources.
- **Multilingual** — `AGROMANCH_LANGUAGE` (and per-call settings overrides, as in the WhatsApp example) switch output language.
