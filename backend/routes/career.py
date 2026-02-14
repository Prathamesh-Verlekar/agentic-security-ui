"""
API routes for the Career Counselor feature.
"""

import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.models.schemas import (
    ApiResponse,
    CareerChatRequest,
    CareerChatResponse,
    CareerDetail,
    CareerTransitionGraph,
    ErrorDetail,
    Profession,
)
from backend.models.career_seed import PROFESSIONS, PROFESSIONS_BY_ID, CAREER_TRANSITIONS
from backend.services.career_generator import generate_career_detail
from backend.services.career_chat import chat_with_career_agent
from backend.services.image_generator import (
    generate_career_image,
    get_cached_image_path,
    has_cached_image,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/careers", tags=["careers"])


def _image_url_for(profession_id: str) -> str:
    """Build the API URL for a profession's image."""
    return f"/api/v1/careers/{profession_id}/image"


# ---------------------------------------------------------------------------
# GET /api/v1/careers — list all professions
# ---------------------------------------------------------------------------
@router.get("", response_model=ApiResponse[list[Profession]])
async def list_careers():
    """Return all professions with image URLs baked in."""
    # We return Profession objects; frontend uses the image endpoint separately
    return ApiResponse(success=True, data=PROFESSIONS)


# ---------------------------------------------------------------------------
# GET /api/v1/careers/transitions — career transition graph data
# ---------------------------------------------------------------------------
@router.get("/transitions", response_model=ApiResponse[CareerTransitionGraph])
async def get_career_transitions():
    """Return the career transition graph (nodes + edges) for all professions."""
    graph = CareerTransitionGraph(
        nodes=PROFESSIONS,
        edges=CAREER_TRANSITIONS,
    )
    return ApiResponse(success=True, data=graph)


# ---------------------------------------------------------------------------
# GET /api/v1/careers/{profession_id} — detailed career info
# ---------------------------------------------------------------------------
@router.get("/{profession_id}", response_model=ApiResponse[CareerDetail])
async def get_career_detail(profession_id: str):
    """Return LLM-generated career detail for a profession."""
    profession = PROFESSIONS_BY_ID.get(profession_id)
    if not profession:
        raise HTTPException(
            status_code=404,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(message=f"Profession '{profession_id}' not found"),
            ).model_dump(),
        )

    try:
        image_url = _image_url_for(profession_id)
        detail = await generate_career_detail(profession, image_url=image_url)
        return ApiResponse(success=True, data=detail)
    except Exception as exc:
        logger.exception("Error generating career detail for %s", profession_id)
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(
                    message="Failed to generate career detail",
                    details=str(exc),
                ),
            ).model_dump(),
        )


# ---------------------------------------------------------------------------
# GET /api/v1/careers/{profession_id}/image — serve the DALL-E image
# ---------------------------------------------------------------------------
@router.get("/{profession_id}/image")
async def get_career_image(profession_id: str):
    """Serve the cached DALL-E image, generating it on first request."""
    profession = PROFESSIONS_BY_ID.get(profession_id)
    if not profession:
        raise HTTPException(status_code=404, detail="Profession not found")

    try:
        image_path = await generate_career_image(profession_id, profession.title)
        return FileResponse(
            path=str(image_path),
            media_type="image/png",
            headers={"Cache-Control": "public, max-age=604800"},  # 7 days
        )
    except Exception as exc:
        logger.exception("Error generating/serving image for %s", profession_id)
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {exc}",
        )


# ---------------------------------------------------------------------------
# POST /api/v1/careers/{profession_id}/chat — career counselor chat
# ---------------------------------------------------------------------------
@router.post("/{profession_id}/chat", response_model=ApiResponse[CareerChatResponse])
async def career_chat(profession_id: str, body: CareerChatRequest):
    """Multi-turn chat with the career counselor agent for a specific profession."""
    profession = PROFESSIONS_BY_ID.get(profession_id)
    if not profession:
        raise HTTPException(
            status_code=404,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(message=f"Profession '{profession_id}' not found"),
            ).model_dump(),
        )

    try:
        reply = await chat_with_career_agent(profession, body.messages)
        return ApiResponse(success=True, data=CareerChatResponse(reply=reply))
    except Exception as exc:
        logger.exception("Error in career chat for %s", profession_id)
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(
                    message="Chat failed",
                    details=str(exc),
                ),
            ).model_dump(),
        )
