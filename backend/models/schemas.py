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


class Example(BaseModel):
    title: str = Field(..., description="Short label for the example")
    scenario: str = Field(..., description="Real-world scenario description")
    code_snippet: str = Field(default="", description="Python/pseudocode snippet (may be empty)")


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
    examples: list[Example] = Field(
        default=[], description="2-4 examples with scenarios and code snippets"
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
# Article schemas (admin article generator)
# ---------------------------------------------------------------------------

class ArticleSection(BaseModel):
    heading: str
    body: str = Field(..., description="Markdown body text for this section")


class DiagramNode(BaseModel):
    id: str
    label: str
    description: str = Field(default="", description="1-sentence description shown below the label")
    x: float = Field(..., description="X position for React Flow")
    y: float = Field(..., description="Y position for React Flow")
    node_type: str = Field(default="default", description="input | output | default | decision")


class DiagramEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str = ""
    animated: bool = True
    edge_type: str = Field(default="smoothstep", description="smoothstep | bezier | straight")


class ArticleSummary(BaseModel):
    id: str
    topic: str
    title: str
    created_at: str


class Article(BaseModel):
    id: str
    topic: str
    title: str
    subtitle: str
    sections: list[ArticleSection] = Field(
        ..., description="4-6 article sections"
    )
    diagram_nodes: list[DiagramNode] = Field(
        default=[], description="React Flow nodes for the architecture diagram"
    )
    diagram_edges: list[DiagramEdge] = Field(
        default=[], description="React Flow edges for the architecture diagram"
    )
    conclusion: str
    created_at: str


class AdminLoginRequest(BaseModel):
    password: str


class AdminLoginResponse(BaseModel):
    token: str


class ArticleGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="Topic for the Medium article")


# ---------------------------------------------------------------------------
# Career Counselor schemas
# ---------------------------------------------------------------------------

class Profession(BaseModel):
    id: str = Field(..., description="Slug-style identifier, e.g. 'software-engineer'")
    title: str
    short_description: str
    icon_emoji: str = ""
    tags: list[str] = []


class CareerPathStage(BaseModel):
    stage: str = Field(..., description="Stage name, e.g. 'Junior Developer'")
    years: str = Field(..., description="Typical years range, e.g. '0-2 years'")
    description: str = Field(..., description="What this stage involves")


class CareerDetail(BaseModel):
    id: str
    title: str
    overview: str
    salary_range: str = Field(..., description="e.g. '$60,000 – $180,000'")
    key_skills: list[str] = Field(..., min_length=5, max_length=10, description="8-10 key skills")
    education_requirements: str
    career_path: list[CareerPathStage] = Field(..., description="4-6 career stages")
    day_in_the_life: str = Field(..., description="Narrative paragraph about a typical day")
    pros: list[str] = Field(..., min_length=3, max_length=7, description="5-7 advantages")
    cons: list[str] = Field(..., min_length=3, max_length=6, description="4-6 disadvantages")
    future_outlook: str
    image_url: str = Field(default="", description="URL to the DALL-E generated image")


class CareerTransitionEdge(BaseModel):
    id: str
    source: str = Field(..., description="Source profession id")
    target: str = Field(..., description="Target profession id")
    label: str = Field(..., description="Transition description, e.g. 'Analytics skills'")
    stage: str = Field(default="Mid-Career", description="At what stage this transition is common")
    difficulty: str = Field(default="moderate", description="easy | moderate | hard")


class CareerTransitionGraph(BaseModel):
    nodes: list[Profession]
    edges: list[CareerTransitionEdge]


class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


class CareerChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1, description="Conversation history")


class CareerChatResponse(BaseModel):
    reply: str


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
