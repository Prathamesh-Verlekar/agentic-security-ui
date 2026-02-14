"""
Admin-only API routes for the article generator.
Protected by a simple password-based token auth.
"""

import hashlib
import hmac
import logging

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse

from backend.config import ADMIN_PASSWORD, ADMIN_TOKEN_SECRET
from backend.models.schemas import (
    AdminLoginRequest,
    AdminLoginResponse,
    ApiResponse,
    Article,
    ArticleGenerateRequest,
    ArticleSummary,
    ErrorDetail,
)
from backend.services.article_generator import (
    generate_article,
    get_article,
    list_articles,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin")


# ─── Token helpers ────────────────────────────────────────────────────────────

def _make_token() -> str:
    """Create an HMAC-based token from the admin password."""
    return hmac.new(
        ADMIN_TOKEN_SECRET.encode(),
        ADMIN_PASSWORD.encode(),
        hashlib.sha256,
    ).hexdigest()


def _verify_token(token: str) -> bool:
    expected = _make_token()
    return hmac.compare_digest(token, expected)


async def verify_admin(authorization: str = Header(default="")) -> None:
    """FastAPI dependency – extracts and verifies the Bearer token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization[7:]
    if not _verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid admin token")


# ─── Login ────────────────────────────────────────────────────────────────────

@router.post("/login")
async def admin_login(body: AdminLoginRequest):
    """Return a JSON response directly (not HTTPException) so CORS headers are preserved."""
    if body.password != ADMIN_PASSWORD:
        return JSONResponse(
            status_code=401,
            content=ApiResponse(
                success=False,
                error=ErrorDetail(message="Incorrect password"),
            ).model_dump(),
        )
    token = _make_token()
    return ApiResponse(success=True, data=AdminLoginResponse(token=token))


# ─── Articles (all require admin auth) ────────────────────────────────────────

@router.post(
    "/articles/generate",
    response_model=ApiResponse[Article],
    dependencies=[Depends(verify_admin)],
)
async def generate_article_endpoint(body: ArticleGenerateRequest):
    try:
        article = await generate_article(body.topic)
        return ApiResponse(success=True, data=article)
    except Exception as exc:
        logger.exception("Error generating article for topic: %s", body.topic)
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(
                    message="Failed to generate article",
                    details=str(exc),
                ),
            ).model_dump(),
        )


@router.get(
    "/articles",
    response_model=ApiResponse[list[ArticleSummary]],
    dependencies=[Depends(verify_admin)],
)
async def list_articles_endpoint():
    summaries = list_articles()
    return ApiResponse(success=True, data=summaries)


@router.get(
    "/articles/{article_id}",
    response_model=ApiResponse[Article],
    dependencies=[Depends(verify_admin)],
)
async def get_article_endpoint(article_id: str):
    article = get_article(article_id)
    if not article:
        raise HTTPException(
            status_code=404,
            detail=ApiResponse(
                success=False,
                error=ErrorDetail(message=f"Article '{article_id}' not found"),
            ).model_dump(),
        )
    return ApiResponse(success=True, data=article)
