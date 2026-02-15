/* ─── API client – talks to the FastAPI backend ─── */

import type {
  ApiResponse,
  Article,
  ArticleSummary,
  CareerChatResponse,
  CareerDetail,
  CareerTransitionGraph,
  Category,
  ChatMessage,
  ItemDetail,
  ItemSummary,
  Profession,
  TransitionPlan,
} from "../types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  const res = await fetch(`${BASE_URL}${path}`, options);
  const body = await res.json().catch(() => null);

  // If the response is already in our ApiResponse format, return it directly
  if (body && typeof body.success === "boolean") {
    return body as ApiResponse<T>;
  }

  // Otherwise, wrap the error
  if (!res.ok) {
    return {
      success: false,
      data: null,
      error: body?.error ?? body?.detail?.error ?? { message: `HTTP ${res.status}` },
    };
  }

  return body as ApiResponse<T>;
}

function authHeaders(): Record<string, string> {
  const token = sessionStorage.getItem("admin_token") ?? "";
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };
}

// ─── Public endpoints ────────────────────────────────────────────────────────

export async function fetchCategories(): Promise<ApiResponse<string[]>> {
  return apiFetch<string[]>("/api/v1/categories");
}

export async function fetchItems(
  category: Category
): Promise<ApiResponse<ItemSummary[]>> {
  return apiFetch<ItemSummary[]>(`/api/v1/items?category=${category}`);
}

export async function fetchItemDetail(
  itemId: string,
  category: Category
): Promise<ApiResponse<ItemDetail>> {
  return apiFetch<ItemDetail>(
    `/api/v1/items/${itemId}?category=${category}`
  );
}

// ─── Career endpoints ─────────────────────────────────────────────────────────

export async function fetchCareers(): Promise<ApiResponse<Profession[]>> {
  return apiFetch<Profession[]>("/api/v1/careers");
}

export async function fetchCareerDetail(
  professionId: string
): Promise<ApiResponse<CareerDetail>> {
  return apiFetch<CareerDetail>(`/api/v1/careers/${professionId}`);
}

export function getCareerImageUrl(professionId: string): string {
  return `${BASE_URL}/api/v1/careers/${professionId}/image`;
}

export async function fetchCareerTransitions(): Promise<ApiResponse<CareerTransitionGraph>> {
  return apiFetch<CareerTransitionGraph>("/api/v1/careers/transitions");
}

export async function chatWithCareer(
  professionId: string,
  messages: ChatMessage[]
): Promise<ApiResponse<CareerChatResponse>> {
  return apiFetch<CareerChatResponse>(`/api/v1/careers/${professionId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });
}

export async function fetchTransitionPlan(
  sourceId: string,
  targetId: string
): Promise<ApiResponse<TransitionPlan>> {
  return apiFetch<TransitionPlan>(
    `/api/v1/careers/transition-plan?source=${encodeURIComponent(sourceId)}&target=${encodeURIComponent(targetId)}`
  );
}

// ─── Admin endpoints ─────────────────────────────────────────────────────────

export async function adminLogin(
  password: string
): Promise<ApiResponse<{ token: string }>> {
  return apiFetch<{ token: string }>("/api/v1/admin/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });
}

export async function generateArticle(
  topic: string
): Promise<ApiResponse<Article>> {
  return apiFetch<Article>("/api/v1/admin/articles/generate", {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ topic }),
  });
}

export async function fetchArticles(): Promise<ApiResponse<ArticleSummary[]>> {
  return apiFetch<ArticleSummary[]>("/api/v1/admin/articles", {
    headers: authHeaders(),
  });
}

export async function fetchArticle(
  articleId: string
): Promise<ApiResponse<Article>> {
  return apiFetch<Article>(`/api/v1/admin/articles/${articleId}`, {
    headers: authHeaders(),
  });
}
