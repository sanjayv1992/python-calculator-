# AgroManch AI Roadmap

This repository is **Phase 1**: the verified knowledge base and reusable
service layer. The phases below build on that foundation without restructuring
it — each adds a layer the current architecture already leaves a seam for (see
[architecture.md](architecture.md)).

## Phase 1 — NotebookLM Knowledge Base ✅ (this repo)
- Structured `knowledge/` base across 16 agricultural domains.
- Idempotent indexing into NotebookLM (`scripts/index_knowledge.py`).
- Reusable async services (notebook, chat, content, artifacts).
- Grounded, cited answers in English and Hindi.
- Runnable AgroManch workflow examples and offline dose math.

## Phase 2 — Farmer AI Chat
- Wrap `ChatService` in an API (`src/agromanch_ai/api/`) for the mobile app.
- Conversation history and per-farmer context.
- Voice/text input in more Indian languages.

## Phase 3 — Crop Doctor AI
- Image-based diagnosis (photo → symptom features → grounded diagnosis).
- Confidence scoring and "escalate to KVK" routing.
- Feedback loop to improve knowledge coverage.

## Phase 4 — Content Automation
- Scheduled, multi-channel content pipelines (Instagram, WhatsApp, YouTube,
  blog) from `ContentService`.
- Editorial review and publishing integrations.

## Phase 5 — Podcast Generation
- Regular farmer-education podcasts via `ArtifactService.generate_podcast`.
- Multilingual episodes and distribution to the app and YouTube.

## Phase 6 — Voice AI
- Voice-first assistant for low-literacy farmers.
- Speech-to-text in and text-to-speech out, grounded in the knowledge base.

## Phase 7 — AgroManch AI Operating System
- Unified orchestration (Gemini or equivalent) across Crop Doctor, dose
  calculator, weather, mandi, schemes, and content.
- Live weather and mandi provider integrations.
- Dealer and extension-worker assistants on the same knowledge core.
