"""
Generate a step-by-step career transition plan between two professions via OpenAI.
Persists cache to a local JSON file with a 10-day TTL per entry.
"""

import json
import logging
import time
from pathlib import Path

from backend.models.schemas import Profession, TransitionPlan, TransitionStep
from backend.services.openai_client import chat_completion

logger = logging.getLogger(__name__)

# ─── Cache configuration ─────────────────────────────────────────────────────
CACHE_TTL_SECONDS = 10 * 24 * 60 * 60  # 10 days
CACHE_FILE = Path(__file__).resolve().parent.parent / "cache" / "transition_plan_cache.json"

SYSTEM_PROMPT = (
    "You are an experienced career transition coach and workforce strategist. "
    "You help professionals navigate career changes with practical, step-by-step plans. "
    "Return valid JSON only — no markdown fences."
)


# ─── File-backed cache helpers ────────────────────────────────────────────────

def _load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read transition plan cache: %s", exc)
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

def _build_prompt(source: Profession, target: Profession) -> str:
    return f"""Create a comprehensive career transition plan for someone moving from:

CURRENT PROFESSION: {source.title}
  Description: {source.short_description}
  Skills/Tags: {", ".join(source.tags)}

TARGET PROFESSION: {target.title}
  Description: {target.short_description}
  Skills/Tags: {", ".join(target.tags)}

Return ONLY a valid JSON object with these exact keys:

- "summary": string (2-3 sentences summarizing this transition — what transferable skills help, what gaps exist)
- "estimated_duration": string (total realistic estimate, e.g. "1-2 years", "6-12 months")
- "difficulty": string (one of "easy", "moderate", "hard")
- "steps": array of 8-12 objects, each with:
    - "order": integer (1-based, sequential)
    - "title": string (short action title, e.g. "Master Python & Data Libraries")
    - "category": string (one of: "Education", "Certification", "Course", "Skill", "Experience", "Networking", "Portfolio")
    - "duration": string (e.g. "2-3 months", "3-6 months")
    - "description": string (2-3 sentences explaining what to do and why it matters for this transition)
    - "resources": array of 1-3 strings (specific course names, platforms, books, or certifications — be specific, e.g. "Coursera: Google Data Analytics Certificate")
    - "priority": string (one of "required", "recommended", "optional")
- "tips": array of 3-5 strings (practical advice for someone making this specific transition)

Make the steps practical and ordered chronologically — what to do first, second, etc.
Include specific certifications, courses, and platforms by name where possible.
Consider transferable skills from the current profession.
"""


# ─── Main generation function ─────────────────────────────────────────────────

async def generate_transition_plan(
    source: Profession,
    target: Profession,
) -> TransitionPlan:
    """
    Return a TransitionPlan between two professions.
    Serves from cache when entry < 10 days old; otherwise generates via OpenAI.
    """
    cache_key = f"{source.id}__to__{target.id}"
    cache = _load_cache()

    if cache_key in cache and _is_entry_valid(cache[cache_key]):
        logger.info("Transition plan cache hit for %s", cache_key)
        payload = cache[cache_key]["data"]
        return _payload_to_plan(payload, source, target)

    logger.info("Generating transition plan %s → %s via OpenAI…", source.id, target.id)
    user_prompt = _build_prompt(source, target)
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
        logger.error("Failed to parse transition plan JSON: %s", exc)
        payload = _fallback_payload(source, target)

    # Persist to cache
    cache[cache_key] = {
        "cached_at": time.time(),
        "data": payload,
    }
    _save_cache(cache)
    logger.info("Cached transition plan for %s", cache_key)

    return _payload_to_plan(payload, source, target)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _payload_to_plan(
    payload: dict,
    source: Profession,
    target: Profession,
) -> TransitionPlan:
    steps_raw = payload.get("steps", [])
    steps = []
    for s in steps_raw:
        try:
            steps.append(TransitionStep(**s))
        except Exception as exc:
            logger.warning("Skipping invalid transition step: %s", exc)

    return TransitionPlan(
        source_id=source.id,
        source_title=source.title,
        target_id=target.id,
        target_title=target.title,
        summary=payload.get("summary", f"Transition from {source.title} to {target.title}."),
        estimated_duration=payload.get("estimated_duration", "1-2 years"),
        difficulty=payload.get("difficulty", "moderate"),
        steps=steps,
        tips=payload.get("tips", [
            "Leverage your transferable skills from your current role.",
            "Network with professionals already in the target field.",
            "Start with small projects to build portfolio evidence.",
        ]),
    )


def _fallback_payload(source: Profession, target: Profession) -> dict:
    return {
        "summary": f"Transitioning from {source.title} to {target.title} requires learning new skills while leveraging your existing experience.",
        "estimated_duration": "1-2 years",
        "difficulty": "moderate",
        "steps": [
            {
                "order": 1,
                "title": "Assess Transferable Skills",
                "category": "Skill",
                "duration": "1-2 weeks",
                "description": "Identify skills from your current role that transfer to the new career.",
                "resources": ["LinkedIn Skills Assessment"],
                "priority": "required",
            },
            {
                "order": 2,
                "title": "Research the Target Field",
                "category": "Education",
                "duration": "2-4 weeks",
                "description": "Learn about the day-to-day, required qualifications, and job market for the target profession.",
                "resources": ["Bureau of Labor Statistics", "LinkedIn Career Explorer"],
                "priority": "required",
            },
            {
                "order": 3,
                "title": "Build Foundation Skills",
                "category": "Course",
                "duration": "3-6 months",
                "description": "Take courses to build the core skills required for the new profession.",
                "resources": ["Coursera", "Udemy", "edX"],
                "priority": "required",
            },
            {
                "order": 4,
                "title": "Earn a Relevant Certification",
                "category": "Certification",
                "duration": "2-4 months",
                "description": "Get certified to validate your new skills and improve your resume.",
                "resources": [],
                "priority": "recommended",
            },
            {
                "order": 5,
                "title": "Build a Portfolio",
                "category": "Portfolio",
                "duration": "2-3 months",
                "description": "Create projects that demonstrate your new skills to potential employers.",
                "resources": ["GitHub", "Personal Website"],
                "priority": "required",
            },
            {
                "order": 6,
                "title": "Network in the New Field",
                "category": "Networking",
                "duration": "Ongoing",
                "description": "Attend meetups, conferences, and connect with professionals in your target field.",
                "resources": ["LinkedIn", "Meetup.com"],
                "priority": "recommended",
            },
        ],
        "tips": [
            "Start small — take on side projects before making the full switch.",
            "Find a mentor in the target profession.",
            "Update your resume to highlight transferable skills.",
        ],
    }
