"""Service layer for AgroManch.

- ``NotebookService`` — index/manage the knowledge base (bulk import).
- ``RetrievalService`` — NotebookLM's only job: fetch verified context.
- ``ContentService`` / ``AdvisoryService`` — thin wrappers over the unified
  Gemini generator.
- ``ArtifactService`` — optional/legacy NotebookLM audio/quiz artifacts (not part
  of the core Gemini content path).
"""

from agromanch_ai.services.advisory_service import AdvisoryService
from agromanch_ai.services.artifact_service import ArtifactService
from agromanch_ai.services.content_service import ContentService
from agromanch_ai.services.notebook_service import NotebookService
from agromanch_ai.services.retrieval_service import RetrievalService

__all__ = [
    "NotebookService",
    "RetrievalService",
    "ContentService",
    "AdvisoryService",
    "ArtifactService",
]
