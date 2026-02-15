"""
Generate detailed career information for professions via OpenAI.
Persists cache to a local JSON file with a 10-day TTL per entry.
Supports region-specific content (India / USA).
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

# ─── Region context ───────────────────────────────────────────────────────────
REGION_CONTEXT = {
    "usa": {
        "name": "United States",
        "currency": "USD ($)",
        "salary_note": "base it on realistic US market data in USD. Example format: '$65,000 – $180,000 per year'. Include entry-level to senior ranges",
        "education_note": "US education system (Associate's, Bachelor's, Master's, PhD from US universities like MIT, Stanford, CMU, state universities, community colleges)",
        "certification_note": "US-recognized certifications and licensing bodies (AWS, Google Cloud, PMP, CPA, bar exam, USMLE, etc.)",
        "job_market_note": "the US job market, Bureau of Labor Statistics projections, major hubs (San Francisco, NYC, Seattle, Austin, Boston)",
    },
    "india": {
        "name": "India",
        "currency": "INR (₹)",
        "salary_note": (
            "base it on realistic 2024 Indian market data in INR using the Indian numbering system. "
            "IMPORTANT: Use lakhs and crores format. Example formats: '₹4 LPA – ₹12 LPA' for entry-level, "
            "'₹15 LPA – ₹40 LPA' for mid-level, '₹50 LPA – ₹1.5 Cr+' for senior. "
            "LPA = Lakhs Per Annum. Show the full range from fresher to senior/director level"
        ),
        "education_note": (
            "Indian education system: 10+2 board exams, then undergraduate degrees like B.Tech/B.E. (from IITs, NITs, BITS Pilani, VIT, top state engineering colleges), "
            "MBBS (AIIMS, CMC Vellore, JIPMER), B.Com/BBA (SRCC, Christ University), BA LLB (NLUs, NLSIU), "
            "MBA (IIMs, ISB, XLRI, FMS Delhi, SPJIMR), M.Tech, PhD. "
            "Mention entrance exams: JEE Main/Advanced, NEET, CAT, CLAT, GATE, UPSC where relevant"
        ),
        "certification_note": (
            "Indian certifications: CA (ICAI), CS (ICSI), CMA, GATE score for PSUs, "
            "NET/SET for teaching, NEET for medicine. Also mention global certs popular in India: "
            "AWS/Azure/GCP certifications, PMP, Scrum Master, CFA, FRM, Google/Meta digital marketing certificates, "
            "NPTEL/SWAYAM courses with certification from IITs/IISc"
        ),
        "job_market_note": (
            "the Indian job market: IT/software hubs (Bangalore, Hyderabad, Pune, Chennai, Gurugram/Noida), "
            "top employers (TCS, Infosys, Wipro, HCL for IT; Deloitte, McKinsey, BCG for consulting; "
            "FAANG/MNC offices in India), startup ecosystem (Bangalore, NCR), "
            "government/PSU jobs (via UPSC, SSC, state PCS, bank exams), "
            "and freelancing/remote work trends"
        ),
    },
}

DEFAULT_REGION = "usa"


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

def _build_prompt(profession: Profession, region: str) -> str:
    ctx = REGION_CONTEXT.get(region, REGION_CONTEXT[DEFAULT_REGION])
    return f"""Generate a comprehensive career guide for the following profession **specifically for the {ctx["name"]} market**:

Title: {profession.title}
Short description: {profession.short_description}
Tags: {", ".join(profession.tags)}
Region: {ctx["name"]}

Return ONLY a valid JSON object (no markdown fences) with these exact keys:

- "overview": string (3-5 sentences providing a rich overview of this career in {ctx["name"]}, mentioning region-specific industry context)
- "salary_range": string ({ctx["salary_note"]}; include entry-level to senior ranges)
- "key_skills": array of 8-10 strings (most important skills for this career in {ctx["name"]})
- "education_requirements": string (2-3 sentences about typical education paths using the {ctx["education_note"]}; mention {ctx["certification_note"]})
- "career_path": array of 4-6 objects, each with:
    - "stage": string (e.g. "Junior Developer", "Senior Engineer", "Tech Lead" — use titles common in {ctx["name"]})
    - "years": string (e.g. "0-2 years", "3-5 years")
    - "description": string (1-2 sentences about what this stage involves in {ctx["name"]})
- "day_in_the_life": string (2-3 paragraph narrative about a typical workday for this professional in {ctx["name"]} — make it vivid and realistic, mention region-specific workplace culture)
- "pros": array of 5-7 strings (advantages of this career in {ctx["name"]})
- "cons": array of 4-6 strings (challenges or disadvantages specific to {ctx["name"]})
- "future_outlook": string (2-3 sentences about {ctx["job_market_note"]}, growth projections, and how technology/AI affects this profession)
"""


# ─── Main generation function ─────────────────────────────────────────────────

async def generate_career_detail(
    profession: Profession,
    image_url: str = "",
    region: str = DEFAULT_REGION,
) -> CareerDetail:
    """
    Return a CareerDetail for the given profession and region.
    Serves from cache when entry < 10 days old; otherwise generates via OpenAI.
    """
    region = region.lower() if region else DEFAULT_REGION
    if region not in REGION_CONTEXT:
        region = DEFAULT_REGION

    cache_key = f"{profession.id}__{region}"
    cache = _load_cache()

    if cache_key in cache and _is_entry_valid(cache[cache_key]):
        logger.info("Career cache hit for %s", cache_key)
        data = cache[cache_key]["data"]
        data["image_url"] = image_url
        return _payload_to_detail(data, profession, image_url)

    logger.info("Generating career detail for %s (%s) via OpenAI…", cache_key, region)
    user_prompt = _build_prompt(profession, region)
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
