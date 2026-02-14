import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchCareers, getCareerImageUrl } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { ErrorDetail, Profession } from "../types";

export default function CareerLanding() {
  const [professions, setProfessions] = useState<Profession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  useEffect(() => {
    fetchCareers()
      .then((res) => {
        if (res.success && res.data) {
          setProfessions(res.data);
        } else {
          setError(res.error ?? { message: "Failed to load careers" });
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader message="Loading professions…" />;
  if (error) return <ErrorBanner error={error} />;

  return (
    <div className="career-landing">
      <div className="career-hero">
        <h1 className="career-hero-title">Career Counselor</h1>
        <p className="career-hero-subtitle">
          Explore top professions, discover what each career path looks like, and
          chat with an AI career counselor to find your perfect fit.
        </p>
      </div>

      <Link to="/careers/transitions" className="transition-map-banner">
        <div className="transition-map-banner-icon">&#x1F5FA;</div>
        <div className="transition-map-banner-text">
          <h3>Career Transition Map</h3>
          <p>
            See how you can switch between professions at any career stage —
            interactive graph with difficulty ratings.
          </p>
        </div>
        <span className="transition-map-banner-cta">View Map &rarr;</span>
      </Link>

      <div className="career-grid">
        {professions.map((p) => (
          <Link
            key={p.id}
            to={`/careers/${p.id}`}
            className="career-card"
          >
            <div className="career-card-image-wrapper">
              <img
                src={getCareerImageUrl(p.id)}
                alt={p.title}
                className="career-card-image"
                loading="lazy"
              />
              <div className="career-card-image-overlay" />
            </div>
            <div className="career-card-body">
              <div className="career-card-emoji">{p.icon_emoji}</div>
              <h2 className="career-card-title">{p.title}</h2>
              <p className="career-card-desc">{p.short_description}</p>
              <div className="career-card-tags">
                {p.tags.map((tag) => (
                  <span key={tag} className="tag">
                    {tag}
                  </span>
                ))}
              </div>
              <span className="career-card-cta">Explore Career &rarr;</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
