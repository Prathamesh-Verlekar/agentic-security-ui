import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { fetchArticles, generateArticle } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import Loader from "../components/Loader";
import type { ArticleSummary, ErrorDetail } from "../types";

export default function AdminDashboard() {
  const [topic, setTopic] = useState("");
  const [generating, setGenerating] = useState(false);
  const [articles, setArticles] = useState<ArticleSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);
  const navigate = useNavigate();

  const loadArticles = () => {
    setLoading(true);
    fetchArticles()
      .then((res) => {
        if (res.success && res.data) {
          setArticles(res.data);
        } else if (res.error?.message?.includes("401")) {
          navigate("/admin/login");
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!sessionStorage.getItem("admin_token")) {
      navigate("/admin/login");
      return;
    }
    loadArticles();
  }, [navigate]);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;
    setGenerating(true);
    setError(null);

    try {
      const res = await generateArticle(topic.trim());
      if (res.success && res.data) {
        setTopic("");
        navigate(`/admin/articles/${res.data.id}`);
      } else {
        setError(res.error ?? { message: "Generation failed" });
      }
    } catch (err) {
      setError({ message: String(err) });
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="admin-dashboard">
      <h1 className="page-title">Article Generator</h1>
      <p className="page-subtitle">
        Enter a topic to generate a Medium-style article with an interactive
        architecture diagram.
      </p>

      <form className="article-form" onSubmit={handleGenerate}>
        <input
          type="text"
          className="admin-input article-topic-input"
          placeholder="e.g. Building Secure Agentic AI Systems"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          disabled={generating}
        />
        <button
          type="submit"
          className="admin-btn"
          disabled={generating || !topic.trim()}
        >
          {generating ? "Generating…" : "Generate Article"}
        </button>
      </form>

      {generating && (
        <Loader message="Generating your article — this may take 15-30 seconds…" />
      )}
      {error && <ErrorBanner error={error} />}

      <h2 className="admin-section-title">Previous Articles</h2>

      {loading ? (
        <Loader message="Loading articles…" />
      ) : articles.length === 0 ? (
        <p className="admin-empty">
          No articles yet. Generate your first one above.
        </p>
      ) : (
        <div className="articles-list">
          {articles.map((a) => (
            <Link
              key={a.id}
              to={`/admin/articles/${a.id}`}
              className="article-list-card"
            >
              <h3 className="article-list-title">{a.title}</h3>
              <p className="article-list-meta">
                Topic: {a.topic} &middot;{" "}
                {new Date(a.created_at).toLocaleDateString()}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
