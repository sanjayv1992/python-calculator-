"""Knowledge document schema: categories + the KnowledgeDocument model."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from agromanch_ai.knowledge.frontmatter import parse_frontmatter

SUPPORTED_LANGUAGES = ("hi", "en", "bho")


class Category(str, Enum):
    """The 19 AgroManch knowledge categories, mapped to `knowledge/` folders."""

    CROPS = "crops"
    CROP_DISEASES = "crop_diseases"
    INSECTS = "insects"
    NUTRIENT_DEFICIENCY = "nutrient_deficiency"
    FERTILIZERS = "fertilizers"
    HERBICIDES = "weed_management"  # Herbicides live in the weed_management folder
    PESTICIDES = "pesticides"
    PLANT_GROWTH_REGULATORS = "plant_growth_regulators"
    SOIL_HEALTH = "soil_health"
    IRRIGATION = "irrigation"
    WEATHER = "weather"
    GOVERNMENT_SCHEMES = "government_schemes"
    CROP_CALENDAR = "crop_calendar"
    MANDI = "mandi"
    ANIMAL_HUSBANDRY = "animal_husbandry"
    FISHERIES = "fisheries"
    ORGANIC_FARMING = "organic_farming"
    POST_HARVEST = "post_harvest"
    FARM_MACHINERY = "farm_machinery"

    @classmethod
    def from_folder(cls, folder: str) -> "Category":
        for c in cls:
            if c.value == folder:
                return c
        raise ValueError(f"No category for folder {folder!r}")

    @classmethod
    def folders(cls) -> list[str]:
        # Distinct folder names (Herbicides shares weed_management).
        return sorted({c.value for c in cls})


# Fields whose presence the quality scorer rewards (completeness).
SCORED_FIELDS = (
    "title", "category", "crop", "season", "state", "district", "source_org",
    "publication_date", "last_verified_date", "language", "scientific_names",
    "hindi_names", "local_names", "keywords", "summary", "important_facts",
    "recommended_practices", "references",
)


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [p.strip() for p in str(value).split(",") if p.strip()]


@dataclass(slots=True)
class KnowledgeDocument:
    """A verified knowledge document with full metadata."""

    title: str
    category: str
    path: str = ""
    crop: str = ""
    season: str = ""
    state: str = ""
    district: str = ""
    source_org: str = ""
    publication_date: str = ""
    last_verified_date: str = ""
    language: str = "hi"
    scientific_names: list[str] = field(default_factory=list)
    hindi_names: list[str] = field(default_factory=list)
    local_names: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    summary: str = ""
    important_facts: list[str] = field(default_factory=list)
    recommended_practices: list[str] = field(default_factory=list)
    dosage: str = ""
    warnings: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    body: str = ""
    quality_score: int = 0

    @classmethod
    def from_file(cls, path: str | Path) -> "KnowledgeDocument":
        path = Path(path)
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        return cls.from_metadata(meta, body=body, path=str(path))

    @classmethod
    def from_metadata(
        cls, meta: dict[str, Any], *, body: str = "", path: str = ""
    ) -> "KnowledgeDocument":
        list_fields = {
            "scientific_names", "hindi_names", "local_names", "keywords",
            "important_facts", "recommended_practices", "warnings", "references",
        }
        kwargs: dict[str, Any] = {"body": body, "path": path}
        for f in SCORED_FIELDS + ("dosage", "warnings"):
            if f in list_fields:
                kwargs[f] = _as_list(meta.get(f))
            else:
                kwargs[f] = str(meta.get(f, "") or "")
        kwargs["language"] = (kwargs.get("language") or "hi").lower()
        doc = cls(**kwargs)  # type: ignore[arg-type]
        return doc

    def validate(self) -> list[str]:
        """Return a list of validation problems (empty = valid)."""
        problems: list[str] = []
        if not self.title:
            problems.append("missing title")
        if not self.category:
            problems.append("missing category")
        elif self.category not in Category.folders():
            problems.append(f"unknown category folder {self.category!r}")
        if self.language not in SUPPORTED_LANGUAGES:
            problems.append(f"language must be one of {SUPPORTED_LANGUAGES}")
        if not self.source_org:
            problems.append("missing source_org")
        return problems

    def dedup_key(self) -> str:
        """Identity key for duplicate detection (title+crop+source)."""
        return "|".join(
            s.strip().lower() for s in (self.title, self.crop, self.source_org)
        )

    def content_hash(self) -> str:
        return hashlib.sha256(self.body.strip().encode("utf-8")).hexdigest()

    def search_terms(self) -> list[str]:
        """Flattened multilingual searchable metadata."""
        terms = [self.title, self.crop, self.category, self.summary]
        terms += self.keywords + self.scientific_names + self.hindi_names + self.local_names
        return [t for t in (s.strip() for s in terms) if t]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
