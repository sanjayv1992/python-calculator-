"""Reusable utilities for AgroManch services and examples."""

from agromanch_ai.utils.authcheck import ensure_authenticated
from agromanch_ai.utils.dose import calculate_dose
from agromanch_ai.utils.text import references_from_ask_result, safe_filename

__all__ = [
    "ensure_authenticated",
    "calculate_dose",
    "references_from_ask_result",
    "safe_filename",
]
