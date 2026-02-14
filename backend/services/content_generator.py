"""
Generate detailed content for guardrail / eval items via OpenAI.
Persists cache to a local JSON file with a 10-day TTL per entry.
"""

import json
import logging
import time
from pathlib import Path

from backend.models.schemas import Category, Example, ItemDetail, ItemSummary
from backend.services.openai_client import chat_completion

logger = logging.getLogger(__name__)

# ─── Cache configuration ─────────────────────────────────────────────────────
CACHE_TTL_SECONDS = 10 * 24 * 60 * 60  # 10 days
CACHE_FILE = Path(__file__).resolve().parent.parent / "cache" / "detail_cache.json"

SYSTEM_PROMPT = (
    "You are an expert in AI/LLM security, agentic frameworks, and evaluation. "
    "When asked, you produce detailed, actionable technical content in valid JSON."
)


# ─── File-backed cache helpers ────────────────────────────────────────────────

def _load_cache() -> dict:
    """Load the full cache dict from disk. Returns {} on any error."""
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read cache file, starting fresh: %s", exc)
        return {}


def _save_cache(cache: dict) -> None:
    """Persist the full cache dict to disk."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _is_entry_valid(entry: dict) -> bool:
    """Return True if the cached entry is still within the TTL window."""
    cached_at = entry.get("cached_at", 0)
    return (time.time() - cached_at) < CACHE_TTL_SECONDS


# ─── Prompt builder ───────────────────────────────────────────────────────────

def _build_user_prompt(item: ItemSummary) -> str:
    category_label = "guardrail" if item.category == Category.GUARDRAILS else "evaluation"
    return f"""Generate a detailed technical write-up for the following {category_label}:

Title: {item.title}
Short description: {item.short_description}
Tags: {", ".join(item.tags)}

Return ONLY a valid JSON object (no markdown fences) with these exact keys:
- "overview": string (2-4 sentences)
- "why_it_matters": string (2-4 sentences)
- "implementation_steps": array of 5-8 actionable bullet strings
- "examples": array of 2-4 objects, each with:
    - "title": string (short label, e.g. "Blocking a prompt injection attack")
    - "scenario": string (2-4 sentence real-world scenario describing when/how this applies)
    - "code_snippet": string (Python or pseudocode snippet demonstrating the concept; use \\n for newlines)
- "risks_and_pitfalls": array of 3-6 bullet strings
- "metrics_or_checks": array of 3-6 bullet strings
"""


# ─── Main generation function ─────────────────────────────────────────────────

async def generate_item_detail(item: ItemSummary) -> ItemDetail:
    """
    Return an ItemDetail for the given item.
    Serves from the persistent JSON cache when the entry is < 10 days old;
    otherwise generates fresh content via OpenAI and updates the cache.
    """
    cache_key = f"{item.category.value}:{item.id}"
    cache = _load_cache()

    # ── Check cache ──────────────────────────────────────────────────────
    if cache_key in cache and _is_entry_valid(cache[cache_key]):
        logger.info("Cache hit for %s (age %.1f hrs)",
                     cache_key,
                     (time.time() - cache[cache_key]["cached_at"]) / 3600)
        return _entry_to_detail(cache[cache_key]["data"], item)

    # ── Generate via OpenAI ──────────────────────────────────────────────
    logger.info("Generating detail for %s via OpenAI…", cache_key)
    user_prompt = _build_user_prompt(item)
    raw = await chat_completion(prompt=user_prompt, system=SYSTEM_PROMPT)

    # Strip markdown code fences if present
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse LLM JSON: %s", exc)
        payload = _fallback_payload(item)

    # ── Persist to cache ─────────────────────────────────────────────────
    cache[cache_key] = {
        "cached_at": time.time(),
        "data": payload,
    }
    _save_cache(cache)
    logger.info("Cached detail for %s (TTL %d days)", cache_key, CACHE_TTL_SECONDS // 86400)

    return _entry_to_detail(payload, item)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _entry_to_detail(payload: dict, item: ItemSummary) -> ItemDetail:
    """Convert a raw JSON payload dict into a validated ItemDetail."""
    return ItemDetail(
        id=item.id,
        title=item.title,
        category=item.category,
        overview=payload.get("overview", ""),
        why_it_matters=payload.get("why_it_matters", ""),
        implementation_steps=payload.get("implementation_steps",
                                          ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"]),
        examples=[Example(**ex) for ex in payload.get("examples", [])],
        risks_and_pitfalls=payload.get("risks_and_pitfalls",
                                        ["Risk 1", "Risk 2", "Risk 3"]),
        metrics_or_checks=payload.get("metrics_or_checks",
                                       ["Metric 1", "Metric 2", "Metric 3"]),
    )


def _fallback_payload(item: ItemSummary) -> dict:
    """Return a minimal valid payload when LLM JSON parsing fails."""
    return {
        "overview": f"{item.title}: {item.short_description}",
        "why_it_matters": "This is a critical component of agentic security that helps protect AI systems.",
        "implementation_steps": [
            "Identify the scope and requirements",
            "Design the architecture and integration points",
            "Implement core logic",
            "Add configuration and policy controls",
            "Write unit and integration tests",
        ],
        "examples": [],
        "risks_and_pitfalls": [
            "Incomplete coverage may leave gaps",
            "Over-aggressive rules can block legitimate use",
            "Maintenance burden increases with complexity",
        ],
        "metrics_or_checks": [
            "Coverage percentage of protected surfaces",
            "False-positive rate",
            "Mean time to detection",
        ],
    }


def clear_cache() -> None:
    """Delete the cache file and start fresh."""
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
        logger.info("Cache file deleted")
