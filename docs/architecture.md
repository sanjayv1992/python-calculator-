# AgroManch AI Architecture

The AgroManch AI Knowledge Engine turns a verified library of agricultural
documents into farmer-facing answers and content. NotebookLM is the grounding
and retrieval layer; the services in `src/agromanch_ai/` wrap it into reusable
building blocks that future AgroManch products (mobile app, dealer portal,
content studio) call.

## End-to-end workflow

```
                         Farmer question
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │   NotebookLM Knowledge Base   │  verified ICAR / SAU / KVK
                 │  (indexed & cited documents)  │  docs, scheme PDFs, labels
                 └──────────────┬───────────────┘
                                │  retrieval + citations
                                ▼
                    Verified agricultural answer
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │   Gemini API (reasoning /     │  personalisation, language,
                 │   orchestration layer)*       │  routing (see roadmap)
                 └──────────────┬───────────────┘
                                │
      ┌───────────────┬─────────┼──────────┬──────────────┬───────────────┐
      ▼               ▼         ▼          ▼              ▼               ▼
 Crop Doctor    Dose Calculator  Weather   Mandi Prices  Scheme/Dealer  Content
 (diagnosis)    (label + math)   Advisory  (market data) Assistants     Generator
      │               │         │          │              │               │
      └───────────────┴─────────┴────┬─────┴──────────────┴───────────────┘
                                      ▼
                             AgroManch Mobile App
                        (farmers, dealers, extension staff)
```

\* The Gemini API layer is **documented here but not implemented in this repo**
(it needs API keys and is scoped for a later phase — see
[roadmap.md](roadmap.md)). Today, NotebookLM itself performs both retrieval and
answer synthesis; the services expose clean seams so a Gemini orchestration
layer can be inserted without restructuring.

## Layers

### 1. Knowledge Base (NotebookLM)
The `knowledge/` folder is indexed into a NotebookLM notebook by
`scripts/index_knowledge.py`. Each document becomes a *source*; answers are
grounded in these sources and return citations. This is the single source of
truth — see [knowledge-sources.md](knowledge-sources.md) for the sourcing
policy.

### 2. Services (`src/agromanch_ai/services/`)
Async, reusable, and independent of any UI:
- **`NotebookService`** — resolve/create the notebook, add sources, bulk-import
  the knowledge folder.
- **`ChatService`** — grounded Q&A returning `CitedAnswer` (answer + source
  references); renders named prompt templates; supports Hindi/English.
- **`ContentService`** — generate channel content (carousel, WhatsApp, blog,
  scripts, FAQ…) as `GeneratedContent`, preserving citations.
- **`ArtifactService`** — generate and download audio (podcasts), quizzes, and
  flashcards.

### 3. Prompts (`src/agromanch_ai/prompts/`)
Every question/brief is a versioned template. Advisory templates enforce
"answer only from the documents", the farmer's language, and safety framing for
agrochemicals. Content templates produce channel-ready structure.

### 4. Domain features
Thin compositions of the services, one per farmer need:
Crop Doctor, pest/disease chat, fertilizer advisor, pesticide dose calculator
(NotebookLM label lookup **+** offline `agromanch_ai.utils.dose` math), weather
advisor, mandi research, government-scheme assistant, livestock assistant. Each
has a runnable example in `examples/agromanch/`.

### 5. Content automation
`ContentService` + content prompts generate Instagram carousels, Facebook
posts, WhatsApp broadcasts, YouTube Shorts scripts/descriptions, SEO keywords,
blog outlines/drafts, podcast scripts, FAQs, and farmer-education notes —
grounded and cited.

### 6. Delivery
The AgroManch mobile app and other surfaces call the services (directly, or via
the future API layer). Configuration is entirely environment-driven
(`AGROMANCH_*`), so the same code runs locally, in CI, and in production.

## Integration seams for the future

- **API layer** — wrap the services in FastAPI/gRPC handlers under a future
  `src/agromanch_ai/api/`; models already serialize via `to_dict()`.
- **Weather / mandi providers** — replace the "index a bulletin URL" step with
  live provider adapters; the advisory prompts stay unchanged.
- **LLM orchestration** — insert Gemini (or another model) between the verified
  answer and the feature layer for personalisation and multi-step reasoning.
- **Multilingual** — `AGROMANCH_LANGUAGE` (and per-call overrides, as in the
  WhatsApp example) already switch answer language.
