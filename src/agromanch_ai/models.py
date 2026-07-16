"""Typed result models shared across AgroManch services.

These are plain dataclasses (no third-party schema library) so they can be
serialized straight to JSON for the future AgroManch API layer.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SourceRef:
    """A citation back to a NotebookLM source document."""

    source_id: str
    citation_number: int | None = None
    title: str | None = None
    cited_text: str | None = None

    def label(self) -> str:
        num = f"[{self.citation_number}] " if self.citation_number else ""
        return f"{num}{self.title or self.source_id}"


@dataclass(slots=True)
class CitedAnswer:
    """A verified answer grounded in the agricultural knowledge base."""

    question: str
    answer: str
    references: list[SourceRef] = field(default_factory=list)
    conversation_id: str | None = None
    language: str = "en"

    def to_markdown(self) -> str:
        lines = [f"### Q: {self.question}", "", self.answer]
        if self.references:
            lines += ["", "**Sources:**"]
            lines += [f"- {ref.label()}" for ref in self.references]
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class GeneratedContent:
    """A piece of farmer-facing content generated from the knowledge base."""

    kind: str  # e.g. "instagram_carousel", "whatsapp_broadcast"
    topic: str
    body: str
    language: str = "en"
    references: list[SourceRef] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [f"## {self.kind.replace('_', ' ').title()}: {self.topic}", "", self.body]
        if self.references:
            lines += ["", "---", "**Knowledge sources:**"]
            lines += [f"- {ref.label()}" for ref in self.references]
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DoseRecommendation:
    """Offline pesticide/fertilizer dose calculation for one field.

    Values mirror what an Indian product label states: a dose per hectare and
    a recommended spray volume. The calculator converts those to the farmer's
    actual field size and knapsack tank.
    """

    product: str
    crop: str
    dose_per_ha: float  # ml or g of product per hectare (from the label)
    unit: str  # "ml" or "g"
    area_ha: float
    spray_volume_per_ha: float  # litres of water per hectare
    tank_capacity_l: float  # knapsack/sprayer tank size in litres

    @property
    def total_product(self) -> float:
        """Total product needed for the field, in ``unit``."""
        return round(self.dose_per_ha * self.area_ha, 2)

    @property
    def total_water_l(self) -> float:
        return round(self.spray_volume_per_ha * self.area_ha, 2)

    @property
    def tanks_needed(self) -> float:
        return round(self.total_water_l / self.tank_capacity_l, 2)

    @property
    def product_per_tank(self) -> float:
        """Product to add to each full tank, in ``unit``."""
        return round(
            self.dose_per_ha / self.spray_volume_per_ha * self.tank_capacity_l, 2
        )

    def to_markdown(self) -> str:
        return "\n".join(
            [
                f"### Dose plan: {self.product} on {self.crop}",
                "",
                f"- Field size: {self.area_ha} ha",
                f"- Label dose: {self.dose_per_ha} {self.unit}/ha "
                f"in {self.spray_volume_per_ha} L water/ha",
                f"- Total product needed: **{self.total_product} {self.unit}**",
                f"- Total spray water: **{self.total_water_l} L** "
                f"(~{self.tanks_needed} tanks of {self.tank_capacity_l} L)",
                f"- Add **{self.product_per_tank} {self.unit} per tank**",
                "",
                "> Always follow the registered label, wear protective equipment,"
                " observe pre-harvest intervals, and confirm with your local"
                " KVK/agriculture officer.",
            ]
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data.update(
            total_product=self.total_product,
            total_water_l=self.total_water_l,
            tanks_needed=self.tanks_needed,
            product_per_tank=self.product_per_tank,
        )
        return data
