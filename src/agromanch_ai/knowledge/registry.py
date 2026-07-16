"""Curated trusted-source registry — the documented collection targets.

This is the repeatable "where verified knowledge comes from" list per category.
It is a curated registry of official portals, NOT an auto-scraper: agricultural
advice must be human-verified before entering the library (see
`scripts/fetch_source.py` and docs/knowledge-sources.md).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceEntry:
    name: str
    org: str  # canonical trusted-source label (see sources.TRUSTED_SOURCES)
    url: str
    categories: tuple[str, ...]


# Curated official sources. URLs are official landing pages; specific documents
# are added to knowledge/<category>/ after human verification.
REGISTRY: tuple[SourceEntry, ...] = (
    SourceEntry("ICAR", "ICAR", "https://icar.org.in", ("crops", "crop_diseases", "insects")),
    SourceEntry("ICAR-NCIPM (pest advisories)", "ICAR", "https://ncipm.icar.gov.in",
                ("insects", "crop_diseases")),
    SourceEntry("ICAR-IIWBR (wheat)", "ICAR", "https://iiwbr.icar.gov.in", ("crops",)),
    SourceEntry("ICAR-IIRR (rice)", "ICAR", "https://icar-iirr.org", ("crops",)),
    SourceEntry("State Agricultural Universities", "State Agricultural University",
                "https://icar.org.in/agricultural-universities",
                ("crops", "fertilizers", "weed_management", "plant_growth_regulators")),
    SourceEntry("Krishi Vigyan Kendras", "KVK", "https://kvk.icar.gov.in",
                ("crops", "crop_calendar", "nutrient_deficiency")),
    SourceEntry("Ministry of Agriculture & Farmers Welfare", "Government Department",
                "https://agriwelfare.gov.in", ("government_schemes", "crop_calendar")),
    SourceEntry("Soil Health Card", "Government Department",
                "https://soilhealth.dac.gov.in", ("soil_health", "fertilizers")),
    SourceEntry("PMKSY (micro-irrigation)", "Government Department",
                "https://pmksy.gov.in", ("irrigation",)),
    SourceEntry("IMD Agromet (weather bulletins)", "IMD", "https://mausam.imd.gov.in",
                ("weather",)),
    SourceEntry("Agmarknet (mandi prices)", "Agmarknet", "https://agmarknet.gov.in",
                ("mandi",)),
    SourceEntry("eNAM", "eNAM", "https://enam.gov.in", ("mandi",)),
    SourceEntry("CIB&RC (pesticide labels)", "Official Product Label",
                "https://ppqs.gov.in", ("pesticides", "weed_management")),
    SourceEntry("NABARD", "NABARD", "https://nabard.org",
                ("government_schemes", "animal_husbandry", "fisheries")),
    SourceEntry("FSSAI", "FSSAI", "https://fssai.gov.in", ("post_harvest", "organic_farming")),
    SourceEntry("Dept. of Animal Husbandry & Dairying", "Government Department",
                "https://dahd.nic.in", ("animal_husbandry",)),
    SourceEntry("Dept. of Fisheries (PMMSY)", "Government Department",
                "https://dof.gov.in", ("fisheries",)),
    SourceEntry("Farm Machinery (SMAM)", "Government Department",
                "https://agrimachinery.nic.in", ("farm_machinery",)),
)


def sources_for(category: str) -> list[SourceEntry]:
    return [e for e in REGISTRY if category in e.categories]
