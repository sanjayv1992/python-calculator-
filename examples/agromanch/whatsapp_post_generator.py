"""WhatsApp broadcast generator: short farmer-group messages, Hindi + English.

Generates the same grounded message in both languages by building a per-language
generator over the shared retrieval + Gemini engine — the pattern AgroManch uses
for multilingual broadcasts.

Run:
    python examples/agromanch/whatsapp_post_generator.py \
        --topic "safe pesticide spraying practices"
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import replace

from _common import agromanch_session

from agromanch_ai.ai import AgroManchGenerator, GeminiEngine
from agromanch_ai.services import ContentService


async def main() -> None:
    parser = argparse.ArgumentParser(description="AgroManch WhatsApp broadcast")
    parser.add_argument("--topic", default="safe pesticide spraying practices")
    args = parser.parse_args()

    async with agromanch_session() as ctx:
        for language in ("en", "hi"):
            settings = replace(ctx.settings, language=language)
            generator = AgroManchGenerator(
                ctx.retrieval, GeminiEngine(settings), settings
            )
            content_service = ContentService(generator, settings)
            message = await content_service.generate(
                ctx.notebook.id, "whatsapp_broadcast", args.topic
            )
            print(f"\n===== {settings.language_name} =====\n")
            print(message.to_markdown())
            content_service.save(message)


if __name__ == "__main__":
    asyncio.run(main())
