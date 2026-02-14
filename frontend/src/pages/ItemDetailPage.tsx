import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchItemDetail } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { Category, ErrorDetail, ItemDetail } from "../types";

export default function ItemDetailPage() {
  const { category, id } = useParams<{ category: string; id: string }>();
  const [detail, setDetail] = useState<ItemDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  useEffect(() => {
    if (!category || !id) return;
    setLoading(true);
    setError(null);

    fetchItemDetail(id, category as Category)
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

      {detail.example_patterns.length > 0 && (
        <Section title="Example Patterns">
          <ul className="detail-list">
            {detail.example_patterns.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
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

      {detail.references.length > 0 && (
        <Section title="References">
          <ul className="detail-list references-list">
            {detail.references.map((ref, i) => (
              <li key={i}>
                <a href={ref.url} target="_blank" rel="noopener noreferrer">
                  {ref.title}
                </a>
              </li>
            ))}
          </ul>
        </Section>
      )}
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
