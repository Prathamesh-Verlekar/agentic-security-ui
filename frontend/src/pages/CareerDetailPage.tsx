import { useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { fetchCareerDetail, fetchCareerTransitions, getCareerImageUrl } from "../api/client";
import CareerChat from "../components/CareerChat";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { CareerDetail, CareerTransitionEdge, ErrorDetail, Profession, Region } from "../types";

const REGION_FLAGS: Record<Region, string> = { usa: "🇺🇸", india: "🇮🇳" };

export default function CareerDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [searchParams] = useSearchParams();
  const region: Region = (searchParams.get("region") ?? "usa") === "india" ? "india" : "usa";

  const [detail, setDetail] = useState<CareerDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);
  const [transitions, setTransitions] = useState<{ edge: CareerTransitionEdge; target: Profession }[]>([]);

  useEffect(() => {
    if (!id) return;
    setLoading(true);

    const detailP = fetchCareerDetail(id, region);
    const transP = fetchCareerTransitions();

    Promise.all([detailP, transP])
      .then(([detailRes, transRes]) => {
        if (detailRes.success && detailRes.data) {
          setDetail(detailRes.data);
        } else {
          setError(detailRes.error ?? { message: "Career not found" });
        }

        if (transRes.success && transRes.data) {
          const profMap = new Map(transRes.data.nodes.map((p) => [p.id, p]));
          const outgoing = transRes.data.edges
            .filter((e) => e.source === id)
            .map((e) => ({ edge: e, target: profMap.get(e.target)! }))
            .filter((t) => t.target);
          setTransitions(outgoing);
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, [id, region]);

  if (loading) return <Loader message="Generating career insights…" />;
  if (error) return <ErrorBanner error={error} />;
  if (!detail || !id) return null;

  return (
    <div className="career-detail">
      <div style={{ display: "flex", alignItems: "center", gap: "1rem", flexWrap: "wrap" }}>
        <Link to={`/careers?region=${region}`} className="back-link">
          &larr; Back to Careers
        </Link>
        <span className="region-badge">{REGION_FLAGS[region]} {region.toUpperCase()}</span>
      </div>

      {/* Hero section with image */}
      <div className="career-detail-hero">
        <img src={getCareerImageUrl(id)} alt={detail.title} className="career-detail-hero-image" />
        <div className="career-detail-hero-text">
          <h1 className="career-detail-title">{detail.title}</h1>
          <p className="career-detail-salary">{detail.salary_range}</p>
        </div>
      </div>

      {/* Overview */}
      <section className="career-section">
        <h2 className="career-section-title">Overview</h2>
        <p className="career-section-body">{detail.overview}</p>
      </section>

      {/* Key Skills */}
      <section className="career-section">
        <h2 className="career-section-title">Key Skills</h2>
        <div className="career-skills-grid">
          {detail.key_skills.map((skill, i) => (
            <span key={i} className="career-skill-chip">{skill}</span>
          ))}
        </div>
      </section>

      {/* Education Requirements */}
      <section className="career-section">
        <h2 className="career-section-title">Education Requirements</h2>
        <p className="career-section-body">{detail.education_requirements}</p>
      </section>

      {/* Career Path Timeline */}
      <section className="career-section">
        <h2 className="career-section-title">Career Path</h2>
        <div className="career-timeline">
          {detail.career_path.map((stage, i) => (
            <div key={i} className="career-timeline-item">
              <div className="career-timeline-marker">
                <div className="career-timeline-dot" />
                {i < detail.career_path.length - 1 && <div className="career-timeline-line" />}
              </div>
              <div className="career-timeline-content">
                <h3 className="career-timeline-stage">{stage.stage}</h3>
                <span className="career-timeline-years">{stage.years}</span>
                <p className="career-timeline-desc">{stage.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Day in the Life */}
      <section className="career-section">
        <h2 className="career-section-title">A Day in the Life</h2>
        <div className="career-day-narrative">
          {detail.day_in_the_life.split("\n").map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </div>
      </section>

      {/* Pros & Cons */}
      <section className="career-section">
        <h2 className="career-section-title">Pros &amp; Cons</h2>
        <div className="career-proscons">
          <div className="career-proscons-column pros">
            <h3 className="career-proscons-heading">
              <span className="proscons-icon">✓</span> Advantages
            </h3>
            <ul className="career-proscons-list">
              {detail.pros.map((pro, i) => (<li key={i}>{pro}</li>))}
            </ul>
          </div>
          <div className="career-proscons-column cons">
            <h3 className="career-proscons-heading">
              <span className="proscons-icon">✕</span> Challenges
            </h3>
            <ul className="career-proscons-list">
              {detail.cons.map((con, i) => (<li key={i}>{con}</li>))}
            </ul>
          </div>
        </div>
      </section>

      {/* Future Outlook */}
      <section className="career-section">
        <h2 className="career-section-title">Future Outlook</h2>
        <p className="career-section-body">{detail.future_outlook}</p>
      </section>

      {/* Career Transitions */}
      {transitions.length > 0 && (
        <section className="career-section">
          <h2 className="career-section-title">Career Transition Options</h2>
          <p className="career-section-body" style={{ marginBottom: "1rem" }}>
            From {detail.title}, you can transition to these careers at different stages:
          </p>
          <div className="career-transitions-list">
            {transitions.map((t) => (
              <Link
                key={t.edge.id}
                to={`/careers/${t.target.id}?region=${region}`}
                className={`career-transition-card difficulty-${t.edge.difficulty}`}
              >
                <div className="career-transition-card-top">
                  <span className="career-transition-emoji">{t.target.icon_emoji}</span>
                  <div className="career-transition-info">
                    <span className="career-transition-name">{t.target.title}</span>
                    <span className="career-transition-label">{t.edge.label}</span>
                  </div>
                </div>
                <div className="career-transition-card-bottom">
                  <span className="career-transition-stage">{t.edge.stage}</span>
                  <span className={`career-transition-difficulty ${t.edge.difficulty}`}>
                    {t.edge.difficulty}
                  </span>
                </div>
              </Link>
            ))}
          </div>
          <Link to={`/careers/transitions?region=${region}`} className="transition-map-link">
            View full transition map &rarr;
          </Link>
        </section>
      )}

      {/* Chat Agent */}
      <section className="career-section">
        <h2 className="career-section-title">Ask the Career Counselor</h2>
        <CareerChat professionId={id} professionTitle={detail.title} region={region} />
      </section>
    </div>
  );
}
