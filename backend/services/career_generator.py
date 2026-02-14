"""
Generate detailed career information for professions via OpenAI.
Persists cache to a local JSON file with a 10-day TTL per entry.
"""

import json
import logging
import time
from pathlib import Path

from backend.models.schemas import CareerDetail, CareerPathStage, Profession
from backend.services.openai_client import chat_completion

logger = logging.getLogger(__name__)

# ─── Cache configuration ─────────────────────────────────────────────────────
CACHE_TTL_SECONDS = 10 * 24 * 60 * 60  # 10 days
CACHE_FILE = Path(__file__).resolve().parent.parent / "cache" / "career_cache.json"

SYSTEM_PROMPT = (
    "You are an experienced career counselor and workforce analyst. "
    "You provide accurate, well-researched, and encouraging career guidance. "
    "Return valid JSON only."
)


# ─── File-backed cache helpers ────────────────────────────────────────────────

def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read career cache: %s", exc)
        return {}


def _save_cache(cache: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _is_entry_valid(entry: dict) -> bool:
    cached_at = entry.get("cached_at", 0)
    return (time.time() - cached_at) < CACHE_TTL_SECONDS


# ─── Prompt builder ───────────────────────────────────────────────────────────

def _build_prompt(profession: Profession) -> str:
    return f"""Generate a comprehensive career guide for the following profession:

Title: {profession.title}
Short description: {profession.short_description}
Tags: {", ".join(profession.tags)}

Return ONLY a valid JSON object (no markdown fences) with these exact keys:

- "overview": string (3-5 sentences providing a rich overview of this career)
- "salary_range": string (e.g. "$60,000 – $180,000 per year" — base it on realistic US market data)
- "key_skills": array of 8-10 strings (most important skills for this career)
- "education_requirements": string (2-3 sentences about typical education paths, degrees, certifications)
- "career_path": array of 4-6 objects, each with:
    - "stage": string (e.g. "Junior Developer", "Senior Engineer", "Tech Lead")
    - "years": string (e.g. "0-2 years", "3-5 years")
    - "description": string (1-2 sentences about what this stage involves)
- "day_in_the_life": string (2-3 paragraph narrative about a typical workday — make it vivid and realistic)
- "pros": array of 5-7 strings (advantages of this career)
- "cons": array of 4-6 strings (challenges or disadvantages)
- "future_outlook": string (2-3 sentences about job market trends, growth projections, and how technology/AI affects this profession)
"""


# ─── Main generation function ─────────────────────────────────────────────────

async def generate_career_detail(
    profession: Profession,
    image_url: str = "",
) -> CareerDetail:
    """
    Return a CareerDetail for the given profession.
    Serves from cache when entry < 10 days old; otherwise generates via OpenAI.
    """
    cache_key = profession.id
    cache = _load_cache()

    if cache_key in cache and _is_entry_valid(cache[cache_key]):
        logger.info("Career cache hit for %s", cache_key)
        data = cache[cache_key]["data"]
        # Update image_url in case it changed
        data["image_url"] = image_url
        return _payload_to_detail(data, profession, image_url)

    logger.info("Generating career detail for %s via OpenAI…", cache_key)
    user_prompt = _build_prompt(profession)
    raw = await chat_completion(
        prompt=user_prompt,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
    )

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse career JSON: %s", exc)
        payload = _fallback_payload(profession)

    # Persist to cache
    cache[cache_key] = {
        "cached_at": time.time(),
        "data": payload,
    }
    _save_cache(cache)
    logger.info("Cached career detail for %s", cache_key)

    return _payload_to_detail(payload, profession, image_url)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _payload_to_detail(
    payload: dict,
    profession: Profession,
    image_url: str,
) -> CareerDetail:
    return CareerDetail(
        id=profession.id,
        title=profession.title,
        overview=payload.get("overview", profession.short_description),
        salary_range=payload.get("salary_range", "Varies by experience and location"),
        key_skills=payload.get("key_skills", ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5"]),
        education_requirements=payload.get("education_requirements", "Varies by specialization."),
        career_path=[
            CareerPathStage(**stage)
            for stage in payload.get("career_path", [
                {"stage": "Entry Level", "years": "0-2 years", "description": "Starting position"},
                {"stage": "Mid Level", "years": "3-5 years", "description": "Growing responsibilities"},
                {"stage": "Senior Level", "years": "6-10 years", "description": "Leadership and mentoring"},
                {"stage": "Expert / Director", "years": "10+ years", "description": "Strategic direction"},
            ])
        ],
        day_in_the_life=payload.get("day_in_the_life", "A typical day involves a variety of tasks and responsibilities."),
        pros=payload.get("pros", ["Great career growth", "Competitive salary", "Meaningful work"]),
        cons=payload.get("cons", ["Can be stressful", "Requires continuous learning", "Work-life balance challenges"]),
        future_outlook=payload.get("future_outlook", "The outlook for this profession remains positive."),
        image_url=image_url,
    )


def _fallback_payload(profession: Profession) -> dict:
    return {
        "overview": profession.short_description,
        "salary_range": "Varies by experience and location",
        "key_skills": ["Communication", "Problem-Solving", "Critical Thinking", "Adaptability", "Teamwork"],
        "education_requirements": "Typically requires a bachelor's degree in a relevant field.",
        "career_path": [
            {"stage": "Entry Level", "years": "0-2 years", "description": "Learning fundamentals and building skills."},
            {"stage": "Mid Level", "years": "3-5 years", "description": "Taking on more responsibility and specializing."},
            {"stage": "Senior Level", "years": "6-10 years", "description": "Leading projects and mentoring others."},
            {"stage": "Expert / Director", "years": "10+ years", "description": "Setting strategic direction."},
        ],
        "day_in_the_life": f"A day as a {profession.title} involves a mix of focused work, collaboration, and continuous learning.",
        "pros": ["Rewarding work", "Good compensation", "Growth opportunities"],
        "cons": ["Can be demanding", "Requires continuous learning", "Competitive field"],
        "future_outlook": f"The demand for {profession.title} professionals is expected to remain strong.",
    }
