/* ─── Shared type definitions (mirrors backend schemas) ─── */

export type Category = "guardrails" | "evals";

export interface ItemSummary {
  id: string;
  title: string;
  short_description: string;
  category: Category;
  tags: string[];
}

export interface Example {
  title: string;
  scenario: string;
  code_snippet: string;
}

export interface ItemDetail {
  id: string;
  title: string;
  category: Category;
  overview: string;
  why_it_matters: string;
  implementation_steps: string[];
  examples: Example[];
  risks_and_pitfalls: string[];
  metrics_or_checks: string[];
}

/* ─── Article types (admin) ─── */

export interface ArticleSection {
  heading: string;
  body: string;
}

export interface DiagramNode {
  id: string;
  label: string;
  description: string;
  x: number;
  y: number;
  node_type: string;
}

export interface DiagramEdge {
  id: string;
  source: string;
  target: string;
  label: string;
  animated: boolean;
  edge_type: string;
}

export interface ArticleSummary {
  id: string;
  topic: string;
  title: string;
  created_at: string;
}

export interface Article {
  id: string;
  topic: string;
  title: string;
  subtitle: string;
  sections: ArticleSection[];
  diagram_nodes: DiagramNode[];
  diagram_edges: DiagramEdge[];
  conclusion: string;
  created_at: string;
}

/* ─── Career Counselor types ─── */

export interface Profession {
  id: string;
  title: string;
  short_description: string;
  icon_emoji: string;
  tags: string[];
}

export interface CareerPathStage {
  stage: string;
  years: string;
  description: string;
}

export interface CareerDetail {
  id: string;
  title: string;
  overview: string;
  salary_range: string;
  key_skills: string[];
  education_requirements: string;
  career_path: CareerPathStage[];
  day_in_the_life: string;
  pros: string[];
  cons: string[];
  future_outlook: string;
  image_url: string;
}

export interface CareerTransitionEdge {
  id: string;
  source: string;
  target: string;
  label: string;
  stage: string;
  difficulty: "easy" | "moderate" | "hard";
}

export interface CareerTransitionGraph {
  nodes: Profession[];
  edges: CareerTransitionEdge[];
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface CareerChatResponse {
  reply: string;
}

/* ─── Career Transition Plan ─── */

export interface TransitionStep {
  order: number;
  title: string;
  category: string;
  duration: string;
  description: string;
  resources: string[];
  priority: "required" | "recommended" | "optional";
}

export interface TransitionPlan {
  source_id: string;
  source_title: string;
  target_id: string;
  target_title: string;
  summary: string;
  estimated_duration: string;
  difficulty: "easy" | "moderate" | "hard";
  steps: TransitionStep[];
  tips: string[];
}

/* ─── Common ─── */

export interface ErrorDetail {
  message: string;
  details?: unknown;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: ErrorDetail | null;
}
