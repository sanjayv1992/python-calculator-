"""Advisory service — farmer-facing answers on the unified Gemini pipeline.

Powers the future Crop Doctor, Farmer Chat, Dealer, and Government Scheme
assistants. Each method builds a topic string, then delegates to the same
:class:`~agromanch_ai.ai.generator.AgroManchGenerator` used for content, so
there is exactly one AI path: NotebookLM retrieval → Gemini generation.
"""

from __future__ import annotations

from agromanch_ai.ai.generator import AgroManchGenerator
from agromanch_ai.config import Settings
from agromanch_ai.logging import get_logger
from agromanch_ai.models import GeneratedContent

logger = get_logger("advisory")


class AdvisoryService:
    """Grounded advisory answers for AgroManch farmer-facing features."""

    def __init__(self, generator: AgroManchGenerator, settings: Settings) -> None:
        self._generator = generator
        self._settings = settings

    async def _answer(
        self, notebook_id: str, task: str, topic: str, **fields: str
    ) -> GeneratedContent:
        return await self._generator.run(
            task, topic=topic, notebook_id=notebook_id, **fields
        )

    async def crop_doctor(
        self, notebook_id: str, *, crop: str, region: str, symptoms: str
    ) -> GeneratedContent:
        topic = f"{crop} disease diagnosis in {region}: {symptoms}"
        return await self._answer(
            notebook_id, "crop_doctor", topic, crop=crop, region=region, symptoms=symptoms
        )

    async def pest_disease(
        self, notebook_id: str, *, pest_or_disease: str, crop: str
    ) -> GeneratedContent:
        topic = f"{pest_or_disease} in {crop}"
        return await self._answer(
            notebook_id, "pest_disease", topic, pest_or_disease=pest_or_disease, crop=crop
        )

    async def fertilizer(
        self, notebook_id: str, *, crop: str, stage: str, soil_context: str
    ) -> GeneratedContent:
        topic = f"fertilizer plan for {crop} at {stage}"
        return await self._answer(
            notebook_id, "fertilizer", topic, crop=crop, stage=stage, soil_context=soil_context
        )

    async def pesticide_label(
        self, notebook_id: str, *, product: str, crop: str, target: str
    ) -> GeneratedContent:
        topic = f"{product} on {crop} for {target}"
        return await self._answer(
            notebook_id, "pesticide_label", topic, product=product, crop=crop, target=target
        )

    async def weather(
        self, notebook_id: str, *, region: str, crop_stage: str, weather_context: str
    ) -> GeneratedContent:
        topic = f"weather advisory for {crop_stage} in {region}"
        return await self._answer(
            notebook_id, "weather", topic, region=region,
            crop_stage=crop_stage, weather_context=weather_context,
        )

    async def mandi(
        self, notebook_id: str, *, commodity: str, region: str
    ) -> GeneratedContent:
        topic = f"{commodity} mandi prices in {region}"
        return await self._answer(
            notebook_id, "mandi", topic, commodity=commodity, region=region
        )

    async def govt_scheme(
        self, notebook_id: str, *, farmer_profile: str, question: str
    ) -> GeneratedContent:
        topic = f"government scheme guidance: {question}"
        return await self._answer(
            notebook_id, "govt_scheme", topic, farmer_profile=farmer_profile, question=question
        )

    async def livestock(
        self, notebook_id: str, *, animal: str, question: str
    ) -> GeneratedContent:
        topic = f"{animal} husbandry: {question}"
        return await self._answer(
            notebook_id, "livestock", topic, animal=animal, question=question
        )

    async def ask(self, notebook_id: str, question: str) -> GeneratedContent:
        return await self._answer(notebook_id, "farmer_qa", question, question=question)
