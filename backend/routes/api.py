"""
API v1 routes for the Agentic Security backend.
"""

import logging

from fastapi import APIRouter, HTTPException, Query

from backend.models.schemas import (
    ApiResponse,
    Category,
    ErrorDetail,
    ItemDetail,
    ItemSummary,
)
from backend.models.seed_data import ALL_ITEMS, ITEMS_BY_CATEGORY
from backend.services.content_generator import generate_item_detail

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")


# ---------------------------------------------------------------------------
# GET /api/v1/categories
# ---------------------------------------------------------------------------
@router.get("/categories", response_model=ApiResponse[list[str]])
async def list_categories():
    """Return the available top-level categories."""
    return ApiResponse(
        success=True,
        data=[c.value for c in Category],
    )


# ---------------------------------------------------------------------------
# GET /api/v1/items?category=guardrails|evals
# ---------------------------------------------------------------------------
@router.get("/items", response_model=ApiResponse[list[ItemSummary]])
async def list_items(category: Category = Query(..., description="Filter by category")):
    """Return item summaries for a given category."""
    items = ITEMS_BY_CATEGORY.get(category, [])
    return ApiResponse(success=True, data=items)


# ---------------------------------------------------------------------------
# GET /api/v1/items/{item_id}?category=guardrails|evals
# ---------------------------------------------------------------------------
@router.get("/items/{item_id}", response_model=ApiResponse[ItemDetail])
async def get_item_detail(
    item_id: str,
    category: Category = Query(..., description="Category the item belongs to"),
):
    """Return detailed content for a specific item. Generates via OpenAI if not cached."""
    item_summary = ALL_ITEMS.get(item_id)

    if item_summary is None or item_summary.category != category:
        raise HTTPException(
            status_code=404,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(
                    message=f"Item '{item_id}' not found in category '{category.value}'"
                ),
            ).model_dump(),
        )

    try:
        detail = await generate_item_detail(item_summary)
        return ApiResponse(success=True, data=detail)
    except Exception as exc:
        logger.exception("Error generating detail for %s", item_id)
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(
                    message="Failed to generate item detail",
                    details=str(exc),
                ),
            ).model_dump(),
        )
