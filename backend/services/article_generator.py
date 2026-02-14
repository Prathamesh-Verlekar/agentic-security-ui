"""
Generate Medium-style articles via OpenAI with React Flow diagram data.
Persists articles to a local JSON file with a 10-day TTL.
"""

import json
import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from backend.models.schemas import (
    Article,
    ArticleSection,
    ArticleSummary,
    DiagramEdge,
    DiagramNode,
)
from backend.config import OPENAI_ARTICLE_MODEL
from backend.services.openai_client import chat_completion

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 10 * 24 * 60 * 60  # 10 days
ARTICLES_FILE = Path(__file__).resolve().parent.parent / "cache" / "articles.json"

SYSTEM_PROMPT = (
    "You are a senior technical writer and architect who publishes in-depth, "
    "publication-ready Medium articles about AI, LLM security, agentic frameworks, "
    "and software engineering. Your articles are detailed, practical, and include "
    "real-world examples, code snippets, and clear architecture diagrams. "
    "Return valid JSON only."
)


def _build_article_prompt(topic: str) -> str:
    return f"""Write a comprehensive, in-depth Medium-style technical article about: "{topic}"

This article should be publication-ready, detailed enough for a senior engineer audience.

Return ONLY a valid JSON object (no markdown fences) with these exact keys:

- "title": string (catchy, engaging Medium-style title)
- "subtitle": string (compelling 1-2 sentence subtitle that hooks the reader)
- "sections": array of 6-8 objects, each with:
    - "heading": string (clear, descriptive section heading)
    - "body": string (4-6 paragraphs of rich, detailed markdown content per section. Each paragraph should be 3-5 sentences. Include:
        - **bold** for key concepts and important terms
        - *italic* for emphasis
        - Bullet lists (using - prefix) for enumerating points, steps, or comparisons
        - Inline `code` for technical terms, function names, libraries, and commands
        - Concrete real-world examples and scenarios
        - Where relevant, include short Python/pseudocode snippets wrapped in backticks
        - Industry references and practical advice)
- "conclusion": string (3-4 paragraphs summarizing key takeaways, future outlook, and actionable next steps)
- "diagram_nodes": array of 10-14 objects representing a detailed, professional architecture/workflow diagram. Each node:
    - "id": string (unique, e.g. "node_1")
    - "label": string (concise label, 2-4 words, e.g. "Input Validation", "LLM Gateway", "Response Filter")
    - "description": string (1 short sentence explaining what this step does, e.g. "Validates and sanitizes all user inputs before processing")
    - "x": number (x position — use a LAYERED LAYOUT with these columns:
        Column 1 (entry): x=50
        Column 2 (processing): x=300
        Column 3 (core): x=550
        Column 4 (output): x=800
        Rows spaced 140px apart, starting at y=30)
    - "y": number (y position)
    - "node_type": string — MUST be one of:
        "input" — for entry points and data sources (1-2 nodes)
        "output" — for final outputs and results (1-2 nodes)
        "decision" — for branching/conditional logic points (1-3 nodes)
        "default" — for all other processing steps
- "diagram_edges": array of 12-18 objects connecting the nodes. Each edge:
    - "id": string (unique, e.g. "edge_1_2")
    - "source": string (source node id)
    - "target": string (target node id)
    - "label": string (action/data label on the arrow, 2-5 words, e.g. "validated request", "on failure", "raw response")
    - "animated": boolean (true for the main/happy-path flow, false for error paths, fallbacks, and feedback loops)
    - "edge_type": string — one of:
        "smoothstep" — for most connections (clean right-angle routing)
        "bezier" — for feedback loops or backwards connections
        "straight" — for direct short connections

CRITICAL DIAGRAM GUIDELINES:
1. Layout: Use a clear LEFT-TO-RIGHT or TOP-TO-BOTTOM layered flow. Entry points on the left/top, outputs on the right/bottom.
2. Branching: Include at least 2 decision/branching points (e.g. "Valid?", "Safe?") with separate paths for success and failure/error.
3. Feedback loops: Include at least 1 feedback or retry loop (e.g. "retry with backoff", "re-validate").
4. Parallel paths: Where appropriate, show parallel processing branches that merge back.
5. No overlap: Ensure adequate spacing — nodes in the same column should be at least 140px apart vertically.
6. Descriptive edges: Every edge label should describe WHAT flows along that connection (data, action, or condition), not just "next".
7. Completeness: The diagram should tell the full story of the system — someone should be able to understand the architecture just from the diagram.
"""


# ─── File persistence helpers ─────────────────────────────────────────────────

def _load_articles() -> dict:
    if not ARTICLES_FILE.exists():
        return {}
    try:
        return json.loads(ARTICLES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read articles file: %s", exc)
        return {}


def _save_articles(articles: dict) -> None:
    ARTICLES_FILE.parent.mkdir(parents=True, exist_ok=True)
    ARTICLES_FILE.write_text(
        json.dumps(articles, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


# ─── Public API ───────────────────────────────────────────────────────────────

async def generate_article(topic: str) -> Article:
    """Generate a new article via OpenAI and persist it."""
    logger.info("Generating article for topic: %s", topic)
    user_prompt = _build_article_prompt(topic)
    raw = await chat_completion(
        prompt=user_prompt,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
        model=OPENAI_ARTICLE_MODEL,
    )

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1]).strip()

    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse article JSON: %s", exc)
        payload = _fallback_payload(topic)

    article_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc).isoformat()

    article = Article(
        id=article_id,
        topic=topic,
        title=payload.get("title", topic),
        subtitle=payload.get("subtitle", ""),
        sections=[
            ArticleSection(**s) for s in payload.get("sections", [])
        ] or [ArticleSection(heading="Introduction", body=f"An exploration of {topic}.")],
        diagram_nodes=[
            DiagramNode(**n) for n in payload.get("diagram_nodes", [])
        ],
        diagram_edges=[
            DiagramEdge(**e) for e in payload.get("diagram_edges", [])
        ],
        conclusion=payload.get("conclusion", ""),
        created_at=now,
    )

    # Persist
    articles = _load_articles()
    articles[article_id] = {
        "cached_at": time.time(),
        "data": article.model_dump(),
    }
    _save_articles(articles)
    logger.info("Saved article %s: %s", article_id, article.title)

    return article


def list_articles() -> list[ArticleSummary]:
    """Return summaries of all saved articles (newest first)."""
    articles = _load_articles()
    summaries = []
    for entry in articles.values():
        data = entry.get("data", {})
        summaries.append(
            ArticleSummary(
                id=data.get("id", ""),
                topic=data.get("topic", ""),
                title=data.get("title", ""),
                created_at=data.get("created_at", ""),
            )
        )
    summaries.sort(key=lambda s: s.created_at, reverse=True)
    return summaries


def get_article(article_id: str) -> Article | None:
    """Retrieve a specific article by ID."""
    articles = _load_articles()
    entry = articles.get(article_id)
    if not entry:
        return None

    # Check TTL
    cached_at = entry.get("cached_at", 0)
    if (time.time() - cached_at) > CACHE_TTL_SECONDS:
        # Expired, remove it
        del articles[article_id]
        _save_articles(articles)
        return None

    return Article(**entry["data"])


def _fallback_payload(topic: str) -> dict:
    return {
        "title": f"Understanding {topic}",
        "subtitle": f"A deep dive into {topic} and why it matters.",
        "sections": [
            {"heading": "Introduction", "body": f"In this article, we explore **{topic}** and its significance in modern software engineering."},
            {"heading": "Core Concepts", "body": f"The fundamental ideas behind {topic} include several key principles that practitioners should understand."},
            {"heading": "Implementation", "body": f"Implementing {topic} requires careful planning and a structured approach."},
            {"heading": "Best Practices", "body": f"When working with {topic}, following established best practices ensures reliable outcomes."},
        ],
        "conclusion": f"Understanding {topic} is essential for building robust systems. The key takeaway is to start small, iterate, and measure your progress.",
        "diagram_nodes": [
            {"id": "node_1", "label": "Start", "description": "Entry point for the system", "x": 50, "y": 50, "node_type": "input"},
            {"id": "node_2", "label": "Validate Input", "description": "Checks and sanitizes incoming data", "x": 300, "y": 50, "node_type": "default"},
            {"id": "node_3", "label": "Process", "description": "Core processing logic", "x": 550, "y": 50, "node_type": "default"},
            {"id": "node_4", "label": "Output", "description": "Returns the final result", "x": 800, "y": 50, "node_type": "output"},
        ],
        "diagram_edges": [
            {"id": "edge_1_2", "source": "node_1", "target": "node_2", "label": "raw input", "animated": True, "edge_type": "smoothstep"},
            {"id": "edge_2_3", "source": "node_2", "target": "node_3", "label": "validated data", "animated": True, "edge_type": "smoothstep"},
            {"id": "edge_3_4", "source": "node_3", "target": "node_4", "label": "result", "animated": True, "edge_type": "smoothstep"},
        ],
    }
