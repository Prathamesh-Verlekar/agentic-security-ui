FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . ./backend/

# Expose port (Render sets $PORT)
EXPOSE 8000

# Run uvicorn — Render injects PORT env var
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
