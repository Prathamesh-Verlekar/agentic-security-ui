export default function Loader({ message = "Loading…" }: { message?: string }) {
  return (
    <div className="loader-container">
      <div className="spinner" />
      <p className="loader-text">{message}</p>
    </div>
  );
}
