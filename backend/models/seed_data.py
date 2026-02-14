"""
Seed data for guardrails and evals item summaries.
"""

from backend.models.schemas import Category, ItemSummary

GUARDRAIL_ITEMS: list[ItemSummary] = [
    ItemSummary(
        id="input-output-schema-validation",
        title="Input / Output Schema Validation",
        short_description="Enforce strict JSON-schema or Pydantic validation on every LLM request and response to prevent malformed data from propagating.",
        category=Category.GUARDRAILS,
        tags=["validation", "schema", "pydantic", "data-integrity"],
    ),
    ItemSummary(
        id="prompt-injection-defense",
        title="Prompt Injection Defense",
        short_description="Detect and block adversarial instructions hidden in user inputs that attempt to override system prompts.",
        category=Category.GUARDRAILS,
        tags=["security", "injection", "adversarial", "input-filtering"],
    ),
    ItemSummary(
        id="tool-access-policy",
        title="Tool Access Policy",
        short_description="Define and enforce which tools an agent is allowed to invoke, with scoped permissions per user role or session.",
        category=Category.GUARDRAILS,
        tags=["policy", "tools", "permissions", "authorization"],
    ),
    ItemSummary(
        id="pii-redaction",
        title="PII Redaction",
        short_description="Automatically detect and mask personally identifiable information in both prompts and LLM outputs.",
        category=Category.GUARDRAILS,
        tags=["privacy", "pii", "redaction", "compliance"],
    ),
    ItemSummary(
        id="secrets-detection",
        title="Secrets Detection",
        short_description="Scan inputs and outputs for API keys, tokens, passwords, and other secrets before they reach or leave the LLM.",
        category=Category.GUARDRAILS,
        tags=["security", "secrets", "scanning", "leak-prevention"],
    ),
    ItemSummary(
        id="grounding-and-citations",
        title="Grounding & Citations",
        short_description="Require the model to cite retrieved sources and ground answers in provided context to reduce hallucinations.",
        category=Category.GUARDRAILS,
        tags=["grounding", "citations", "rag", "factuality"],
    ),
    ItemSummary(
        id="rate-limiting-and-abuse",
        title="Rate Limiting & Abuse Prevention",
        short_description="Throttle per-user and per-session request rates to prevent denial-of-service and cost-runaway attacks.",
        category=Category.GUARDRAILS,
        tags=["rate-limit", "abuse", "cost-control", "throttling"],
    ),
    ItemSummary(
        id="audit-logging-and-tracing",
        title="Audit Logging & Tracing",
        short_description="Record every agent action, tool call, and LLM interaction with structured trace IDs for post-hoc analysis.",
        category=Category.GUARDRAILS,
        tags=["logging", "tracing", "audit", "observability"],
    ),
    ItemSummary(
        id="session-management-and-isolation",
        title="Session Management & Isolation",
        short_description="Isolate conversation state per user session to prevent cross-session data leakage or context contamination.",
        category=Category.GUARDRAILS,
        tags=["session", "isolation", "multi-tenancy", "state"],
    ),
    ItemSummary(
        id="jailbreak-detection",
        title="Jailbreak Detection",
        short_description="Identify and block prompts designed to bypass safety filters or elicit disallowed content from the model.",
        category=Category.GUARDRAILS,
        tags=["jailbreak", "safety", "detection", "content-filtering"],
    ),
]

EVAL_ITEMS: list[ItemSummary] = [
    ItemSummary(
        id="groundedness",
        title="Groundedness",
        short_description="Measure how well the model's answers are supported by the provided context or retrieved documents.",
        category=Category.EVALS,
        tags=["factuality", "rag", "grounding", "evaluation"],
    ),
    ItemSummary(
        id="correctness",
        title="Correctness",
        short_description="Evaluate factual accuracy of model outputs against a known ground-truth or reference answer set.",
        category=Category.EVALS,
        tags=["accuracy", "ground-truth", "evaluation"],
    ),
    ItemSummary(
        id="refusal-compliance",
        title="Refusal Compliance",
        short_description="Check that the model correctly refuses harmful, out-of-scope, or policy-violating requests.",
        category=Category.EVALS,
        tags=["safety", "refusal", "compliance", "policy"],
    ),
    ItemSummary(
        id="tool-call-accuracy",
        title="Tool-Call Accuracy",
        short_description="Assess whether the agent invokes the correct tool with proper arguments and interprets tool results accurately.",
        category=Category.EVALS,
        tags=["tools", "function-calling", "accuracy"],
    ),
    ItemSummary(
        id="latency-and-cost",
        title="Latency & Cost",
        short_description="Track end-to-end response latency and token spend per interaction to keep performance within budget.",
        category=Category.EVALS,
        tags=["performance", "latency", "cost", "monitoring"],
    ),
    ItemSummary(
        id="regression-suite",
        title="Regression Suite",
        short_description="Run a fixed set of golden-answer test cases after every model or prompt change to catch regressions.",
        category=Category.EVALS,
        tags=["regression", "testing", "ci-cd", "golden-set"],
    ),
    ItemSummary(
        id="adversarial-prompt-suite",
        title="Adversarial Prompt Suite",
        short_description="Evaluate model robustness against a curated set of adversarial and edge-case prompts.",
        category=Category.EVALS,
        tags=["adversarial", "red-team", "robustness"],
    ),
    ItemSummary(
        id="pii-leakage-eval",
        title="PII Leakage Eval",
        short_description="Detect whether the model inadvertently reveals personally identifiable information in its responses.",
        category=Category.EVALS,
        tags=["pii", "privacy", "leakage", "evaluation"],
    ),
    ItemSummary(
        id="hallucination-rate",
        title="Hallucination Rate",
        short_description="Quantify the frequency at which the model generates unsupported or fabricated claims.",
        category=Category.EVALS,
        tags=["hallucination", "factuality", "measurement"],
    ),
]

# Quick lookup maps
ITEMS_BY_CATEGORY: dict[Category, list[ItemSummary]] = {
    Category.GUARDRAILS: GUARDRAIL_ITEMS,
    Category.EVALS: EVAL_ITEMS,
}

ALL_ITEMS: dict[str, ItemSummary] = {
    item.id: item
    for items in ITEMS_BY_CATEGORY.values()
    for item in items
}
