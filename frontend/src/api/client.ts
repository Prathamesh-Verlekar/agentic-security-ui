/* ─── API client – talks to the FastAPI backend ─── */

import type {
  ApiResponse,
  Article,
  ArticleSummary,
  Category,
  ItemDetail,
  ItemSummary,
} from "../types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    return {
      success: false,
      data: null,
      error: body?.error ?? body?.detail?.error ?? { message: `HTTP ${res.status}` },
    };
  }
  return res.json() as Promise<ApiResponse<T>>;
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
