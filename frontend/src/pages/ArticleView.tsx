import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { fetchArticle } from "../api/client";
import ErrorBanner from "../components/ErrorBanner";
import FlowDiagram from "../components/FlowDiagram";
import Loader from "../components/Loader";
import type { Article, ErrorDetail } from "../types";

export default function ArticleView() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ErrorDetail | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!sessionStorage.getItem("admin_token")) {
      navigate("/admin/login");
      return;
    }
    if (!id) return;

    setLoading(true);
    fetchArticle(id)
      .then((res) => {
        if (res.success && res.data) {
          setArticle(res.data);
        } else {
          setError(res.error ?? { message: "Article not found" });
        }
      })
      .catch((err) => setError({ message: String(err) }))
      .finally(() => setLoading(false));
  }, [id, navigate]);

  const [copied, setCopied] = useState(false);

  const copyToClipboard = useCallback(() => {
    if (!article) return;
    const md = articleToMarkdown(article);
    navigator.clipboard.writeText(md).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    });
  }, [article]);

  if (loading) return <Loader message="Loading article…" />;
  if (error) return <ErrorBanner error={error} />;
  if (!article) return null;

  return (
    <div className="article-view">
      <div className="article-top-bar">
        <Link to="/admin" className="back-link">
          &larr; Back to Dashboard
        </Link>
        <button
          className={`copy-btn ${copied ? "copied" : ""}`}
          onClick={copyToClipboard}
        >
          {copied ? "Copied to Clipboard!" : "Copy for Medium"}
        </button>
      </div>

      <header className="article-header">
        <h1 className="article-title">{article.title}</h1>
        <p className="article-subtitle">{article.subtitle}</p>
        <p className="article-meta">
          {new Date(article.created_at).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </p>
      </header>

      {article.diagram_nodes.length > 0 && (
        <section className="article-diagram-section">
          <h2 className="diagram-section-title">Architecture / Workflow</h2>
          <p className="diagram-section-subtitle">
            Interactive diagram — drag to pan, scroll to zoom, and click nodes to
            inspect the flow.
          </p>
          <FlowDiagram
            nodes={article.diagram_nodes}
            edges={article.diagram_edges}
          />
          <div className="diagram-legend">
            <span className="legend-item">
              <span className="legend-dot input" /> Entry Point
            </span>
            <span className="legend-item">
              <span className="legend-dot default" /> Process Step
            </span>
            <span className="legend-item">
              <span className="legend-dot decision" /> Decision
            </span>
            <span className="legend-item">
              <span className="legend-dot output" /> Output
            </span>
          </div>
        </section>
      )}

      {article.sections.map((section, i) => (
        <section key={i} className="article-section">
          <h2 className="article-section-heading">{section.heading}</h2>
          <div className="article-body">{renderMarkdown(section.body)}</div>
        </section>
      ))}

      <section className="article-section article-conclusion">
        <h2 className="article-section-heading">Conclusion</h2>
        <div className="article-body">{renderMarkdown(article.conclusion)}</div>
      </section>
    </div>
  );
}

/**
 * Minimal markdown-to-JSX renderer for article bodies.
 * Handles **bold**, *italic*, `code`, bullet lists, and paragraphs.
 */
function renderMarkdown(text: string) {
  const paragraphs = text.split(/\n\n+/);
  return paragraphs.map((para, i) => {
    const trimmed = para.trim();

    // Bullet list
    if (trimmed.match(/^[-*] /m)) {
      const items = trimmed.split(/\n/).filter((l) => l.trim());
      return (
        <ul key={i} className="article-list">
          {items.map((item, j) => (
            <li key={j}>
              <InlineMarkdown text={item.replace(/^[-*]\s*/, "")} />
            </li>
          ))}
        </ul>
      );
    }

    return (
      <p key={i}>
        <InlineMarkdown text={trimmed} />
      </p>
    );
  });
}

/**
 * Convert an Article to clean Markdown suitable for pasting into Medium.
 */
function articleToMarkdown(article: Article): string {
  const lines: string[] = [];
  lines.push(`# ${article.title}`);
  lines.push("");
  lines.push(`*${article.subtitle}*`);
  lines.push("");
  lines.push("---");
  lines.push("");

  for (const section of article.sections) {
    lines.push(`## ${section.heading}`);
    lines.push("");
    lines.push(section.body);
    lines.push("");
  }

  lines.push("## Conclusion");
  lines.push("");
  lines.push(article.conclusion);
  lines.push("");

  return lines.join("\n");
}

function InlineMarkdown({ text }: { text: string }) {
  // Process inline: **bold**, *italic*, `code`
  const parts: React.ReactNode[] = [];
  const regex = /(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }
    if (match[2]) {
      parts.push(<strong key={match.index}>{match[2]}</strong>);
    } else if (match[3]) {
      parts.push(<em key={match.index}>{match[3]}</em>);
    } else if (match[4]) {
      parts.push(<code key={match.index} className="inline-code">{match[4]}</code>);
    }
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  return <>{parts}</>;
}
