import type { ErrorDetail } from "../types";

interface Props {
  error: ErrorDetail;
}

export default function ErrorBanner({ error }: Props) {
  return (
    <div className="error-banner">
      <strong>Error:</strong> {error.message}
      {error.details != null && (
        <pre className="error-details">
          {typeof error.details === "string"
            ? error.details
            : JSON.stringify(error.details, null, 2)}
        </pre>
      )}
    </div>
  );
}
