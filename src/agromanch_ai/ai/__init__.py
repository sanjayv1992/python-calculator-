"""The AgroManch AI engine: Gemini generation + the unified generator/pipeline.

Architecture (single path for content AND advisory):

    NotebookLM retrieval -> VerifiedContext -> Gemini generation -> output

- ``GeminiEngine`` / ``TextEngine`` — the Gemini text-generation seam.
- ``AgroManchGenerator`` — the shared brain: retrieve verified context, then
  generate grounded output for any task (content channel or advisory).
- ``ContentFactory`` — produce the full multi-asset content bundle for a topic
  and hand it off for one-click publishing.
"""

from agromanch_ai.ai.engine import GeminiEngine, TextEngine
from agromanch_ai.ai.generator import AgroManchGenerator
from agromanch_ai.ai.pipeline import DEFAULT_BUNDLE, ContentFactory

__all__ = [
    "TextEngine",
    "GeminiEngine",
    "AgroManchGenerator",
    "ContentFactory",
    "DEFAULT_BUNDLE",
]
