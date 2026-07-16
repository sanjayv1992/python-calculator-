"""Farmer Persona Engine.

Each persona yields a directive injected (via ``{persona_directive}``) into every
prompt so language, CTA and examples adapt to the audience. Deterministic; no LLM.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Persona:
    key: str
    name: str
    focus: str      # what they care about
    cta: str        # the CTA framing that fits them
    examples: str   # the kind of examples to use


PERSONAS: dict[str, Persona] = {
    "small_farmer": Persona(
        "small_farmer", "Small Farmer",
        "low-cost, low-risk practices and saving inputs",
        "message AgroManch on WhatsApp for free personalised advice",
        "1-2 acre paddy/wheat/vegetable examples"),
    "large_farmer": Persona(
        "large_farmer", "Large / Commercial Farmer",
        "yield, efficiency, mechanisation and ROI",
        "talk to an AgroManch expert to plan the season",
        "multi-acre, machinery and input-cost examples"),
    "dairy_farmer": Persona(
        "dairy_farmer", "Dairy Farmer",
        "milk yield, animal health, feed and fodder",
        "ask AgroManch about your animal's health plan",
        "cattle/buffalo feeding, vaccination and dairy examples"),
    "vegetable_grower": Persona(
        "vegetable_grower", "Vegetable Grower",
        "pest/disease control, quality and market price",
        "get a spray/nutrition schedule from AgroManch",
        "tomato/okra/cucurbit and mandi-price examples"),
    "sugarcane_farmer": Persona(
        "sugarcane_farmer", "Sugarcane Farmer",
        "ratoon management, water and long-season care",
        "plan your cane season with AgroManch",
        "sugarcane planting, ratoon and irrigation examples"),
    "organic_farmer": Persona(
        "organic_farmer", "Organic Farmer",
        "bio-inputs, certification and soil health",
        "explore organic practices with AgroManch",
        "compost, biopesticide and certification examples"),
    "dealer": Persona(
        "dealer", "Input Dealer",
        "product knowledge, label-accurate advice and farmer trust",
        "partner with AgroManch for verified product guidance",
        "dealer-counter and product-recommendation examples"),
    "input_shop": Persona(
        "input_shop", "Input Shop Owner",
        "stocking the right inputs for the season and demand",
        "get seasonal demand insights from AgroManch",
        "seasonal stocking and farmer-demand examples"),
    "village_entrepreneur": Persona(
        "village_entrepreneur", "Village Entrepreneur",
        "custom-hiring, services and rural business",
        "grow your rural agri-business with AgroManch",
        "custom-hiring, drone-spray and service-business examples"),
}

DEFAULT_PERSONA = "small_farmer"


def get_persona(key: str | None) -> Persona:
    return PERSONAS.get((key or "").strip().lower(), PERSONAS[DEFAULT_PERSONA])


def persona_directive(key: str | None) -> str:
    """Prompt block adapting language, CTA and examples to the persona."""
    p = get_persona(key)
    return (
        f"AUDIENCE PERSONA — {p.name}: they care about {p.focus}. Use "
        f"{p.examples}; frame the CTA as '{p.cta}'. Adapt tone and vocabulary to "
        "this persona."
    )
