"""AgroManch AI Knowledge Engine.

A production-oriented knowledge platform for Indian agriculture built on top of
Google NotebookLM (via the unofficial `notebooklm-py` library). It powers
AgroManch workflows such as the Crop Doctor, Farmer AI Chat, Government Scheme
Assistant, and agricultural content automation.
"""

from agromanch_ai.config import Settings
from agromanch_ai.models import (
    CitedAnswer,
    DoseRecommendation,
    GeneratedContent,
    SourceRef,
)

__version__ = "0.1.0"

__all__ = [
    "Settings",
    "CitedAnswer",
    "DoseRecommendation",
    "GeneratedContent",
    "SourceRef",
    "__version__",
]
