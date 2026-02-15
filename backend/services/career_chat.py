"""
Career counselor chat service — multi-turn conversation about a specific profession.
Supports region-specific context (India / USA).
Uses gpt-4o-mini for cost efficiency.
"""

import logging

from backend.models.schemas import ChatMessage, Profession
from backend.services.openai_client import get_openai_client
from backend.config import OPENAI_MODEL_NAME

logger = logging.getLogger(__name__)

REGION_NAMES = {
    "usa": "United States",
    "india": "India",
}

DEFAULT_REGION = "usa"


REGION_DETAILS = {
    "usa": (
        "Use USD for salaries (e.g. $60,000 – $180,000/year). "
        "Reference US universities, certifications (AWS, PMP, CPA, bar exam, USMLE), "
        "and job markets (SF, NYC, Seattle, Austin)."
    ),
    "india": (
        "ALWAYS use Indian Rupees (₹) for salaries in lakhs per annum (LPA) or crores format "
        "(e.g. ₹4-8 LPA for freshers, ₹15-40 LPA for mid-level, ₹50 LPA-1.5 Cr for senior). "
        "Reference Indian institutions (IITs, IIMs, AIIMS, NITs, NLUs, BITS Pilani), "
        "entrance exams (JEE, CAT, GATE, NEET, UPSC), Indian certifications (CA from ICAI, CS from ICSI), "
        "Indian companies (TCS, Infosys, Wipro, Flipkart, Razorpay, FAANG India offices), "
        "IT hubs (Bangalore, Hyderabad, Pune, Chennai, Gurugram/Noida), "
        "Indian learning platforms (NPTEL/SWAYAM, UpGrad, Great Learning, Unacademy), "
        "and government/PSU job routes where relevant."
    ),
}


def _build_system_prompt(profession: Profession, region: str) -> str:
    region_name = REGION_NAMES.get(region, REGION_NAMES[DEFAULT_REGION])
    region_detail = REGION_DETAILS.get(region, REGION_DETAILS[DEFAULT_REGION])
    return (
        f"You are an experienced, empathetic career counselor specializing in the "
        f"'{profession.title}' profession **in {region_name}**. Your goal is to help "
        f"the user understand this career path in the context of the {region_name} market.\n\n"
        f"Profession overview: {profession.short_description}\n"
        f"Relevant tags: {', '.join(profession.tags)}\n"
        f"Region: {region_name}\n\n"
        f"IMPORTANT region-specific instructions:\n{region_detail}\n\n"
        f"Guidelines:\n"
        f"- Answer questions about salary expectations (in local currency), required skills, "
        f"education paths (using {region_name} education system and institutions), "
        f"work-life balance, career growth, industry trends, and day-to-day responsibilities "
        f"**specific to {region_name}**.\n"
        f"- Always mention region-specific companies, institutions, certifications, and job markets.\n"
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
    region: str = DEFAULT_REGION,
) -> str:
    """
    Send a multi-turn conversation to OpenAI and return the assistant reply.
    The full conversation history is passed for context continuity.
    """
    region = region.lower() if region else DEFAULT_REGION
    if region not in REGION_NAMES:
        region = DEFAULT_REGION

    system = _build_system_prompt(profession, region)

    openai_messages: list[dict] = [{"role": "system", "content": system}]
    for msg in messages:
        openai_messages.append({"role": msg.role, "content": msg.content})

    logger.info(
        "Career chat for %s (%s) — %d messages in history",
        profession.id,
        region,
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
