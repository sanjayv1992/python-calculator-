"""Advisory prompt specs — farmer-facing answers on the same Gemini pipeline.

These power the future Crop Doctor, Farmer Chat, Dealer, and Government Scheme
assistants. Same architecture as content: NotebookLM supplies the verified
context, Gemini reasons over it and writes the farmer-friendly answer.

Rules baked into the system instruction: answer only from the verified context,
be honest about gaps, put safety first for agrochemicals, and answer in the
farmer's language.
"""

from __future__ import annotations

from agromanch_ai.prompts.spec import PromptSpec

_SYS = (
    "You are AgroManch's trusted agricultural advisor for smallholder farmers in "
    "{target_region}. Answer in {language_name}. {language_directive} Be simple, "
    "practical, warm and respectful. Use ONLY the verified context from trusted "
    "agricultural documents; if it does not cover something, say so clearly instead "
    "of guessing. Never state a pesticide or fertilizer dose that is not in the "
    "context — defer to the registered label and the local KVK. Keep answers "
    "well-structured and actionable. "
)

# Seasonal context is injected so advice is timely; no marketing angle (accuracy
# first). The generator also supplies content_angle, which advisory ignores.
_USER = "{context_block}\n\n{seasonal_context}\n\n{persona_directive}\n\nTOPIC: {topic}\n\n"


def _advisory(instruction: str, temperature: float = 0.4) -> PromptSpec:
    return PromptSpec(_SYS, _USER + instruction, temperature)


ADVISORY_SPECS: dict[str, PromptSpec] = {
    "crop_doctor": _advisory(
        "The farmer grows {crop} in {region} and reports these symptoms: "
        "{symptoms}\n\nProvide: 1) most likely disease/disorder and why the "
        "symptoms match; 2) other possibilities to rule out and how to tell them "
        "apart; 3) immediate management (cultural first, then chemical); "
        "4) prevention next season; 5) when to escalate to the local KVK."
    ),
    "pest_disease": _advisory(
        "Explain {pest_or_disease} affecting {crop}: 1) how to identify it in the "
        "field; 2) damage and economic threshold if documented; 3) integrated "
        "management (cultural, mechanical, biological, chemical); 4) safety "
        "precautions for any chemical option."
    ),
    "fertilizer": _advisory(
        "Crop: {crop}. Growth stage: {stage}. Soil context: {soil_context}\n\n"
        "Recommend: 1) nutrient needs for this stage; 2) fertilizer products and "
        "per-hectare quantities from the documents; 3) application method and "
        "timing; 4) signs of over/under application to watch for."
    ),
    "pesticide_label": _advisory(
        "Product: {product}. Crop: {crop}. Target: {target}\n\nFrom the label "
        "documents state: 1) registered label dose per hectare and spray volume; "
        "2) number of applications and interval; 3) pre-harvest interval; "
        "4) mandatory safety precautions and PPE. If this combination is not in "
        "the context, say so and advise checking the printed label and local KVK."
    ),
    "weather": _advisory(
        "Region: {region}. Crop and stage: {crop_stage}. Forecast context: "
        "{weather_context}\n\nGive a practical advisory: 1) what this weather means "
        "for the crop now; 2) field operations to do, delay, or avoid in the next "
        "few days; 3) pest/disease risks this weather raises; 4) irrigation and "
        "input-application adjustments."
    ),
    "mandi": _advisory(
        "Commodity: {commodity}. Markets/region: {region}\n\nSummarize from the "
        "documents: 1) recent price levels and trend; 2) supply/arrival factors; "
        "3) practical selling guidance (hold/sell signals, quality premiums); "
        "4) which data is missing that would improve this analysis.",
        temperature=0.5,
    ),
    "govt_scheme": _advisory(
        "Farmer profile: {farmer_profile}. Question: {question}\n\nCover: 1) which "
        "scheme(s) in the documents apply and key benefits; 2) eligibility checked "
        "against the profile; 3) documents required and how/where to apply; "
        "4) deadlines or seasonal windows if documented."
    ),
    "livestock": _advisory(
        "Animal: {animal}. Question: {question}\n\nAnswer with: 1) direct guidance "
        "from the documents; 2) feeding/housing/vaccination specifics where "
        "relevant; 3) warning signs that need a veterinarian immediately."
    ),
    "farmer_qa": _advisory(
        "Answer the farmer's question clearly and practically: {question}"
    ),
}
