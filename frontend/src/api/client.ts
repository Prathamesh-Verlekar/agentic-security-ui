/* ─── API client – talks to the FastAPI backend ─── */

import type { ApiResponse, Category, ItemDetail, ItemSummary } from "../types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function apiFetch<T>(path: string): Promise<ApiResponse<T>> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    return {
      success: false,
      data: null,
      error: body?.error ?? { message: `HTTP ${res.status}` },
    };
  }
  return res.json() as Promise<ApiResponse<T>>;
}

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
