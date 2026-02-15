import { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { fetchCareers, getCareerImageUrl } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { ErrorDetail, Profession, Region } from "../types";

const REGIONS: { id: Region; label: string; flag: string; desc: string }[] = [
  { id: "usa", label: "United States", flag: "🇺🇸", desc: "US salaries, education, certifications & job market" },
  { id: "india", label: "India", flag: "🇮🇳", desc: "Indian salaries (₹), education system, IITs/IIMs & local market" },
];

export default function CareerLanding() {
  const [searchParams, setSearchParams] = useSearchParams();
  const regionParam = (searchParams.get("region") ?? "usa") as Region;
  const region: Region = regionParam === "india" ? "india" : "usa";

  const [professions, setProfessions] = useState<Profession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  // Transition planner state
  const [fromId, setFromId] = useState("");
  const [toId, setToId] = useState("");
  const navigate = useNavigate();

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

  const setRegion = (r: Region) => {
    setSearchParams({ region: r });
  };

  const canNavigate = fromId && toId && fromId !== toId;

  const handleNavigate = () => {
    if (canNavigate) {
      navigate(`/careers/transition-plan?from=${fromId}&to=${toId}&region=${region}`);
    }
  };

  if (loading) return <Loader message="Loading professions…" />;
  if (error) return <ErrorBanner error={error} />;

  const fromProf = professions.find((p) => p.id === fromId);
  const toProf = professions.find((p) => p.id === toId);
  const activeRegion = REGIONS.find((r) => r.id === region)!;

  return (
    <div className="career-landing">
      <div className="career-hero">
        <h1 className="career-hero-title">Career Counselor</h1>
        <p className="career-hero-subtitle">
          Explore top professions, discover what each career path looks like, and
          chat with an AI career counselor to find your perfect fit.
        </p>
      </div>

      {/* ── Region Selector ────────────────────────────────────────── */}
      <div className="region-selector">
        <span className="region-selector-label">Select your region</span>
        <div className="region-tabs">
          {REGIONS.map((r) => (
            <button
              key={r.id}
              className={`region-tab ${region === r.id ? "active" : ""}`}
              onClick={() => setRegion(r.id)}
            >
              <span className="region-tab-flag">{r.flag}</span>
              <span className="region-tab-name">{r.label}</span>
            </button>
          ))}
        </div>
        <p className="region-selector-hint">
          {activeRegion.flag} {activeRegion.desc}
        </p>
      </div>

      {/* ── Transition Planner ──────────────────────────────────────── */}
      <div className="tp-planner">
        <div className="tp-planner-header">
          <span className="tp-planner-icon">🗺️</span>
          <div>
            <h3 className="tp-planner-title">Plan Your Career Transition</h3>
            <p className="tp-planner-desc">
              Select your current profession and your target — we'll generate a
              step-by-step roadmap customized for {activeRegion.flag} {activeRegion.label}.
            </p>
          </div>
        </div>

        <div className="tp-planner-selectors">
          <div className="tp-select-group">
            <label className="tp-label">Current Profession</label>
            <div className="tp-select-wrapper">
              {fromProf && <span className="tp-select-emoji">{fromProf.icon_emoji}</span>}
              <select className="tp-select" value={fromId} onChange={(e) => setFromId(e.target.value)}>
                <option value="">Select your current role…</option>
                {professions.map((p) => (
                  <option key={p.id} value={p.id} disabled={p.id === toId}>
                    {p.icon_emoji} {p.title}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="tp-select-arrow">→</div>

          <div className="tp-select-group">
            <label className="tp-label">Target Profession</label>
            <div className="tp-select-wrapper">
              {toProf && <span className="tp-select-emoji">{toProf.icon_emoji}</span>}
              <select className="tp-select" value={toId} onChange={(e) => setToId(e.target.value)}>
                <option value="">Select your target role…</option>
                {professions.map((p) => (
                  <option key={p.id} value={p.id} disabled={p.id === fromId}>
                    {p.icon_emoji} {p.title}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button className="tp-navigate-btn" disabled={!canNavigate} onClick={handleNavigate}>
            Generate Roadmap →
          </button>
        </div>

        {fromId && toId && fromId === toId && (
          <p className="tp-error">Please select two different professions.</p>
        )}
      </div>

      {/* ── Transition Map Banner ──────────────────────────────────── */}
      <Link to={`/careers/transitions?region=${region}`} className="transition-map-banner">
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

      {/* ── Career Grid ────────────────────────────────────────────── */}
      <div className="career-grid">
        {professions.map((p) => (
          <Link key={p.id} to={`/careers/${p.id}?region=${region}`} className="career-card">
            <div className="career-card-image-wrapper">
              <img src={getCareerImageUrl(p.id)} alt={p.title} className="career-card-image" loading="lazy" />
              <div className="career-card-image-overlay" />
            </div>
            <div className="career-card-body">
              <div className="career-card-emoji">{p.icon_emoji}</div>
              <h2 className="career-card-title">{p.title}</h2>
              <p className="career-card-desc">{p.short_description}</p>
              <div className="career-card-tags">
                {p.tags.map((tag) => (
                  <span key={tag} className="tag">{tag}</span>
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
