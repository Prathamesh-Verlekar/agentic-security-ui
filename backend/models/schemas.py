"""
Pydantic models for request/response validation.
Shared data model for the Agentic Security application.
"""

from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Category(str, Enum):
    GUARDRAILS = "guardrails"
    EVALS = "evals"


# ---------------------------------------------------------------------------
# Item schemas
# ---------------------------------------------------------------------------

class ItemSummary(BaseModel):
    id: str = Field(..., description="Slug-style identifier, e.g. 'prompt-injection-defense'")
    title: str
    short_description: str
    category: Category
    tags: list[str] = []


class ItemDetail(BaseModel):
    id: str
    title: str
    category: Category
    overview: str
    why_it_matters: str
    implementation_steps: list[str] = Field(
        ..., min_length=5, max_length=8,
        description="5-8 implementation bullets"
    )
    example_patterns: list[str] = Field(
        default=[], description="Concrete patterns / pseudo examples"
    )
    risks_and_pitfalls: list[str] = Field(
        ..., min_length=3, max_length=6,
        description="3-6 risk bullets"
    )
    metrics_or_checks: list[str] = Field(
        ..., min_length=3, max_length=6,
        description="3-6 metrics bullets"
    )


# ---------------------------------------------------------------------------
# Standard API response wrapper
# ---------------------------------------------------------------------------

class ErrorDetail(BaseModel):
    message: str
    details: Optional[Any] = None


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None
