# AgroManch AI Roadmap

This repository is the **AI Content Factory foundation**: Gemini generation
grounded in NotebookLM-verified sources, one unified pipeline for content and
advisory. The phases below extend it without restructuring — each adds a layer
the architecture already leaves a seam for (see [architecture.md](architecture.md)).

## Phase 1 — Content Factory + Verified Knowledge Base ✅ (this repo)
- Structured `knowledge/` base (16 domains) indexed into NotebookLM.
- NotebookLM retrieval → `VerifiedContext` with citations.
- Gemini engine + unified generator (grounding rule enforced).
- Full 15-asset content bundle per topic + one-click publishing handoff.
- Advisory workflows (Crop Doctor, schemes, etc.) on the same pipeline.

## Delivered alongside Phase 1: Self-improving layer ✅
- Multi-Agent Review (Gemini reviewers) + automatic rewrite loop to 95+.
- Competitor Intelligence (viral-format library, primary+secondary angles).
- Performance Learning (local-JSON history → learned style preferences).

## Delivered: Autonomous Content Operations ✅
- Content Strategy Planner (7/30/90-day), Editorial Calendar, Campaign Engine.
- Intelligent Publishing Queue, Content Gap Analyzer, Evergreen classifier.
- Farmer Persona Engine (prompt-injected), Recommendation layer, internal reports.
- All deterministic and offline (`scripts/plan_content.py`); no new LLM.

## Phase 2 — Farmer AI Chat
- Wrap the generator/advisory service in an API (`src/agromanch_ai/api/`).
- Per-farmer context and conversation history.
- More Indian languages.

## Phase 3 — Crop Doctor AI
- Image-based diagnosis (photo → symptoms → grounded Gemini answer).
- Confidence scoring and "escalate to KVK" routing.

## Phase 4 — Content Automation at scale
- Scheduled, multi-topic content runs feeding the publishing manifest.
- Editorial review and real platform-API posting (Instagram/Facebook/YouTube/WhatsApp/Telegram).

## Phase 5 — Media Generation
- Plug Imagen (images), Veo (video), and TTS (voiceover) into `publish()` so the
  factory outputs rendered assets, not just prompts/scripts.
- Auto-burn subtitles from the generated SRT.

## Phase 6 — Voice AI
- Voice-first assistant for low-literacy farmers (STT in, TTS out), grounded in
  the same knowledge base.

## Phase 7 — AgroManch AI Operating System
- Unified orchestration across Crop Doctor, advisories, and the content factory.
- Live weather/mandi provider integrations; dealer and extension-worker assistants
  on the same knowledge core.
