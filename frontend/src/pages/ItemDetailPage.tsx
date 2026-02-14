import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { fetchItemDetail } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { Category, ErrorDetail, ItemDetail } from "../types";

export default function ItemDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { pathname } = useLocation();
  // Derive category from path: "/guardrails/some-id" -> "guardrails"
  const category = pathname.split("/")[1] as Category;

  const [detail, setDetail] = useState<ItemDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  useEffect(() => {
    if (!category || !id) return;
    setLoading(true);
    setError(null);

    fetchItemDetail(id, category)
      .then((res) => {
        if (res.success && res.data) {
          setDetail(res.data);
        } else {
          setError(res.error ?? { message: "Unknown error" });
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, [category, id]);

  if (loading)
    return (
      <Loader message="Generating detailed content via AI — this may take a moment…" />
    );
  if (error) return <ErrorBanner error={error} />;
  if (!detail) return null;

  return (
    <div className="detail-page">
      <Link to={`/${category}`} className="back-link">
        &larr; Back to {category}
      </Link>

      <h1 className="detail-title">{detail.title}</h1>

      <Section title="Overview">
        <p>{detail.overview}</p>
      </Section>

      <Section title="Why It Matters">
        <p>{detail.why_it_matters}</p>
      </Section>

      <Section title="Implementation Steps">
        <ol className="detail-list">
          {detail.implementation_steps.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </Section>

      {detail.examples.length > 0 && (
        <Section title="Examples">
          <div className="examples-grid">
            {detail.examples.map((ex, i) => (
              <div key={i} className="example-card">
                <h3 className="example-title">{ex.title}</h3>
                <p className="example-scenario">{ex.scenario}</p>
                {ex.code_snippet && (
                  <pre className="example-code"><code>{ex.code_snippet}</code></pre>
                )}
              </div>
            ))}
          </div>
        </Section>
      )}

      <Section title="Risks & Pitfalls">
        <ul className="detail-list">
          {detail.risks_and_pitfalls.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>
      </Section>

      <Section title="Metrics & Checks">
        <ul className="detail-list">
          {detail.metrics_or_checks.map((m, i) => (
            <li key={i}>{m}</li>
          ))}
        </ul>
      </Section>

    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="detail-section">
      <h2 className="detail-section-title">{title}</h2>
      {children}
    </section>
  );
}
