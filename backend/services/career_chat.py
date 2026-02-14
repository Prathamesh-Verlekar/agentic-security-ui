"""
Career counselor chat service — multi-turn conversation about a specific profession.
Uses gpt-4o-mini for cost efficiency.
"""

import logging

from backend.models.schemas import ChatMessage, Profession
from backend.services.openai_client import get_openai_client
from backend.config import OPENAI_MODEL_NAME

logger = logging.getLogger(__name__)


def _build_system_prompt(profession: Profession) -> str:
    return (
        f"You are an experienced, empathetic career counselor specializing in the "
        f"'{profession.title}' profession. Your goal is to help the user understand "
        f"this career path thoroughly.\n\n"
        f"Profession overview: {profession.short_description}\n"
        f"Relevant tags: {', '.join(profession.tags)}\n\n"
        f"Guidelines:\n"
        f"- Answer questions about salary expectations, required skills, education paths, "
        f"work-life balance, career growth, industry trends, and day-to-day responsibilities.\n"
        f"- Be encouraging but honest — mention both opportunities and challenges.\n"
        f"- Provide specific, actionable advice when possible.\n"
        f"- If the user asks about a different profession, briefly acknowledge it but steer "
        f"back to {profession.title} or suggest they explore the other profession card.\n"
        f"- Keep responses concise (2-4 paragraphs) unless the user asks for more detail.\n"
        f"- Use a warm, professional tone."
    )


async def chat_with_career_agent(
    profession: Profession,
    messages: list[ChatMessage],
) -> str:
    """
    Send a multi-turn conversation to OpenAI and return the assistant reply.
    The full conversation history is passed for context continuity.
    """
    system = _build_system_prompt(profession)

    openai_messages: list[dict] = [{"role": "system", "content": system}]
    for msg in messages:
        openai_messages.append({"role": msg.role, "content": msg.content})

    logger.info(
        "Career chat for %s — %d messages in history",
        profession.id,
        len(messages),
    )

    client = get_openai_client()
    response = await client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=openai_messages,
        temperature=0.7,
        max_tokens=1024,
    )

    reply = response.choices[0].message.content or ""
    logger.info("Career chat reply length: %d chars", len(reply))
    return reply
