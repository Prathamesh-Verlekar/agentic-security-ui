import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { fetchCareerTransitions } from "../api/client";
import CareerTransitionGraphView from "../components/CareerTransitionGraph";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { CareerTransitionGraph, ErrorDetail, Region } from "../types";

export default function CareerTransitionsPage() {
  const [searchParams] = useSearchParams();
  const region: Region = (searchParams.get("region") ?? "usa") === "india" ? "india" : "usa";

  const [graph, setGraph] = useState<CareerTransitionGraph | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);

  useEffect(() => {
    fetchCareerTransitions()
      .then((res) => {
        if (res.success && res.data) {
          setGraph(res.data);
        } else {
          setError(res.error ?? { message: "Failed to load transition data" });
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader message="Loading career transitions…" />;
  if (error) return <ErrorBanner error={error} />;
  if (!graph) return null;

  return (
    <div className="transitions-page">
      <Link to={`/careers?region=${region}`} className="back-link">
        &larr; Back to Careers
      </Link>

      <div className="transitions-hero">
        <h1 className="transitions-title">Career Transition Map</h1>
        <p className="transitions-subtitle">
          Click any profession to drill down into its transition paths.
          The side panel shows where you can go and where people come from.
        </p>
      </div>

      <CareerTransitionGraphView
        professions={graph.nodes}
        transitions={graph.edges}
        region={region}
      />
    </div>
  );
}
