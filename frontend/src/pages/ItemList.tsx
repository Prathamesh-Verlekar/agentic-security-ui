import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { fetchItems } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import ItemCard from "../components/ItemCard";
import Loader from "../components/Loader";
import type { Category, ErrorDetail, ItemSummary } from "../types";

const TITLES: Record<Category, string> = {
  guardrails: "LLM Guardrails",
  evals: "Evaluations",
};

export default function ItemList() {
  const { pathname } = useLocation();
  // Derive category from the path: "/guardrails" -> "guardrails", "/evals" -> "evals"
  const category = pathname.split("/")[1] as Category;

  const [items, setItems] = useState<ItemSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  useEffect(() => {
    if (!category) return;
    setLoading(true);
    setError(null);

    fetchItems(category)
      .then((res) => {
        if (res.success && res.data) {
          setItems(res.data);
        } else {
          setError(res.error ?? { message: "Unknown error" });
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, [category]);

  if (loading) return <Loader message={`Loading ${category}…`} />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <div className="item-list-page">
      <h1 className="page-title">{TITLES[category] ?? category}</h1>
      <p className="page-subtitle">
        Click any card to see a detailed, AI-generated deep dive.
      </p>
      <div className="items-grid">
        {items.map((item) => (
          <ItemCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}
