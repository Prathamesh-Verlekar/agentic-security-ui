/* ─── Shared type definitions (mirrors backend schemas) ─── */

export type Category = "guardrails" | "evals";

export interface ItemSummary {
  id: string;
  title: string;
  short_description: string;
  category: Category;
  tags: string[];
}

export interface ItemDetail {
  id: string;
  title: string;
  category: Category;
  overview: string;
  why_it_matters: string;
  implementation_steps: string[];
  example_patterns: string[];
  risks_and_pitfalls: string[];
  metrics_or_checks: string[];
}

export interface ErrorDetail {
  message: string;
  details?: unknown;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: ErrorDetail | null;
}
