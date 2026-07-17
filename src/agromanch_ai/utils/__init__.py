"""Reusable utilities for AgroManch services and examples."""

from agromanch_ai.utils.authcheck import (
    NotebookLMAuthError,
    ensure_authenticated,
    has_stored_session,
    verify_notebooklm_auth,
)
from agromanch_ai.utils.dose import calculate_dose
from agromanch_ai.utils.text import references_from_ask_result, safe_filename

__all__ = [
    "ensure_authenticated",
    "has_stored_session",
    "verify_notebooklm_auth",
    "NotebookLMAuthError",
    "calculate_dose",
    "references_from_ask_result",
    "safe_filename",
]
