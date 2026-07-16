"""Seasonal Intelligence Engine.

Pure, date-based, deterministic. Produces a seasonal directive injected into every
prompt so content prioritizes what farmers actually need right now. The calendar
below is a general guide for the Purvanchal / eastern-UP / Bihar cropping system —
verify locally; agronomy varies by district and year.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

# season codes
KHARIF = "Kharif (monsoon)"
RABI = "Rabi (winter)"
ZAID = "Zaid (summer)"


@dataclass(frozen=True, slots=True)
class SeasonInfo:
    month_name: str
    season: str
    crops: str
    stage: str
    pests: str
    weather: str
    activities: str


# month (1-12) -> seasonal picture for the target region.
_CALENDAR: dict[int, SeasonInfo] = {
    1: SeasonInfo("January", RABI, "wheat, mustard, potato, gram, lentil",
                  "wheat tillering/CRI; mustard flowering",
                  "aphids on mustard, late blight on potato, yellow rust on wheat",
                  "cold, foggy, occasional frost",
                  "irrigation, top-dressing nitrogen, aphid watch, frost protection"),
    2: SeasonInfo("February", RABI, "wheat, mustard, potato, vegetables",
                  "wheat jointing/booting; mustard pod fill",
                  "yellow rust, aphids, potato late blight",
                  "cool days, rising temperatures",
                  "second irrigation, disease scouting, potato harvest begins"),
    3: SeasonInfo("March", RABI, "wheat, mustard, spring maize, vegetables",
                  "wheat grain filling to maturity; mustard maturity",
                  "wheat aphids, termites, rust in late fields",
                  "warming, dry",
                  "wheat & mustard harvest prep and harvest, threshing, safe storage"),
    4: SeasonInfo("April", ZAID, "moong, urad, spring maize, vegetables, fodder",
                  "wheat harvest wrap-up; zaid crops vegetative",
                  "stem borer in maize, whitefly/jassids on vegetables",
                  "hot, dry",
                  "harvest & storage, zaid irrigation, field prep for kharif"),
    5: SeasonInfo("May", ZAID, "moong, urad, cucurbits, fodder, sugarcane (standing)",
                  "zaid pulses pod fill; cucurbit fruiting",
                  "fruit fly on cucurbits, sucking pests",
                  "very hot, pre-monsoon showers",
                  "light irrigation, mulching, nursery planning, summer ploughing"),
    6: SeasonInfo("June", KHARIF, "paddy nursery, maize, pigeonpea, sugarcane",
                  "paddy nursery sowing; kharif land prep",
                  "stem borer & fall armyworm building in maize",
                  "monsoon onset, first rains",
                  "MONSOON PREPARATION: nursery sowing, field bunding, seed treatment"),
    7: SeasonInfo("July", KHARIF, "paddy, maize, pigeonpea, urad",
                  "paddy transplanting; maize knee-high",
                  "Fall Armyworm in maize, stem borer, case worm in paddy",
                  "active monsoon, high humidity",
                  "paddy transplanting, weeding, basal fertilizer, FAW scouting"),
    8: SeasonInfo("August", KHARIF, "paddy, maize, pigeonpea, vegetables",
                  "paddy tillering; maize tasseling",
                  "rice stem borer & leaf folder, bacterial leaf blight, sheath blight",
                  "heavy monsoon, waterlogging risk",
                  "nitrogen top-dressing, drainage, disease management, pest scouting"),
    9: SeasonInfo("September", KHARIF, "paddy, pigeonpea, early vegetables",
                  "paddy panicle initiation/booting",
                  "brown planthopper, neck blast, sheath blight",
                  "retreating monsoon, humid",
                  "water management, BPH watch, rabi planning, potato seed arrangement"),
    10: SeasonInfo("October", RABI, "paddy (maturing), potato, mustard, wheat prep",
                   "paddy maturity/harvest; rabi sowing begins",
                   "rice grain pests; early aphids on mustard",
                   "clear, cooling",
                   "WHEAT PREPARATION, paddy harvest, potato & mustard sowing"),
    11: SeasonInfo("November", RABI, "wheat, mustard, potato, gram, lentil",
                   "wheat sowing/germination; potato planting",
                   "cutworm, termite, early aphids",
                   "cool, dry",
                   "timely wheat sowing, seed treatment, first irrigation, weed control"),
    12: SeasonInfo("December", RABI, "wheat, mustard, potato, gram, vegetables",
                   "wheat crown-root initiation; mustard vegetative",
                   "aphids, potato late blight onset",
                   "cold, foggy",
                   "CRI-stage irrigation + nitrogen, late-blight watch, frost care"),
}


def season_info(today: date | None = None) -> SeasonInfo:
    """Seasonal picture for the given (or current) date."""
    today = today or date.today()
    return _CALENDAR[today.month]


def seasonal_context(today: date | None = None) -> str:
    """Directive injected into prompts so content is timely and in-season."""
    info = season_info(today)
    return (
        f"SEASONAL CONTEXT — it is now {info.month_name}, {info.season} season in "
        f"the target region. Main crops: {info.crops}. Typical growth stage: "
        f"{info.stage}. Current pest/disease pressure: {info.pests}. Weather: "
        f"{info.weather}. Farmers are busy with: {info.activities}. "
        "Prioritise what farmers need at THIS time of year. If the requested TOPIC "
        "is clearly out of season, still cover it but add a short note on its right "
        "seasonal window."
    )
