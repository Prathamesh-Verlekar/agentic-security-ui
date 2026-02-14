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
from backend.services.openai_client import chat_completion

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 10 * 24 * 60 * 60  # 10 days
ARTICLES_FILE = Path(__file__).resolve().parent.parent / "cache" / "articles.json"

SYSTEM_PROMPT = (
    "You are an expert technical writer who creates engaging, in-depth Medium articles "
    "about AI, LLM security, agentic frameworks, and software engineering. "
    "You also design clear workflow/architecture diagrams. "
    "Return valid JSON only."
)


def _build_article_prompt(topic: str) -> str:
    return f"""Write a comprehensive Medium-style technical article about: "{topic}"

Return ONLY a valid JSON object (no markdown fences) with these exact keys:

- "title": string (catchy, Medium-style title)
- "subtitle": string (1-sentence subtitle)
- "sections": array of 4-6 objects, each with:
    - "heading": string (section heading)
    - "body": string (2-4 paragraphs of rich markdown content per section; use **bold**, *italic*, bullet lists, and inline `code` where appropriate)
- "conclusion": string (2-3 paragraph conclusion with key takeaways)
- "diagram_nodes": array of 5-8 objects representing workflow/architecture steps, each with:
    - "id": string (unique, e.g. "node_1")
    - "label": string (short label for the node, max 4 words)
    - "x": number (x position, space nodes 200-250px apart horizontally, start at 50)
    - "y": number (y position, space nodes 150-200px apart vertically, start at 50)
    - "node_type": string (use "input" for the first node, "output" for the last node, "default" for others)
- "diagram_edges": array of objects connecting the nodes, each with:
    - "id": string (unique, e.g. "edge_1_2")
    - "source": string (source node id)
    - "target": string (target node id)
    - "label": string (short edge label describing the flow, max 5 words)
    - "animated": boolean (true for primary flow, false for secondary)

The diagram should represent the architecture or workflow described in the article.
Arrange nodes in a logical top-to-bottom or left-to-right flow.
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
    raw = await chat_completion(prompt=user_prompt, system=SYSTEM_PROMPT)

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
            {"id": "node_1", "label": "Start", "x": 250, "y": 50, "node_type": "input"},
            {"id": "node_2", "label": "Process", "x": 250, "y": 200, "node_type": "default"},
            {"id": "node_3", "label": "Output", "x": 250, "y": 350, "node_type": "output"},
        ],
        "diagram_edges": [
            {"id": "edge_1_2", "source": "node_1", "target": "node_2", "label": "Input", "animated": True},
            {"id": "edge_2_3", "source": "node_2", "target": "node_3", "label": "Result", "animated": True},
        ],
    }
