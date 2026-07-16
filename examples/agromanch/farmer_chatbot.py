"""Farmer chatbot: interactive terminal chat over the knowledge base.

A minimal version of the AgroManch Farmer AI Assistant: every answer is
grounded in the notebook's verified documents and shows its sources. The
conversation ID is reused so follow-up questions keep context.

Run:
    python examples/agromanch/farmer_chatbot.py
    (type 'exit' to quit)
"""

from __future__ import annotations

import asyncio

from _common import agromanch_session

WELCOME = """\
AgroManch Farmer Assistant — ask anything about crops, pests, fertilizers,
schemes, or livestock. Answers come only from the verified knowledge base.
Type 'exit' to quit.
"""


async def main() -> None:
    async with agromanch_session() as ctx:
        print(WELCOME)
        conversation_id: str | None = None

        while True:
            try:
                question = (await asyncio.to_thread(input, "\nYou: ")).strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not question or question.lower() in {"exit", "quit"}:
                break

            answer = await ctx.chat.ask(
                ctx.notebook.id, question, conversation_id=conversation_id
            )
            conversation_id = answer.conversation_id

            print(f"\nAgroManch: {answer.answer}")
            if answer.references:
                print("\nSources:")
                for ref in answer.references:
                    print(f"  - {ref.label()}")

        print("\nDhanyavaad! Happy farming.")


if __name__ == "__main__":
    asyncio.run(main())
