# Agentic Security — Interactive UI + FastAPI Backend

A full-stack application that visualizes **Agentic Security** as an interactive tree of LLM Guardrails and Evaluations, with detailed AI-generated content powered by OpenAI.

## Architecture

```
agentic-security-ui/
├── backend/          # FastAPI (Python)
│   ├── main.py
│   ├── config.py
│   ├── models/       # Pydantic schemas & seed data
│   ├── services/     # OpenAI client & content generator
│   └── routes/       # API v1 endpoints
├── frontend/         # React + TypeScript (Vite)
│   └── src/
│       ├── api/      # API client
│       ├── types/    # Shared TypeScript types
│       ├── components/
│       └── pages/
├── .env.example      # Environment variable template
└── README.md
```

## Prerequisites

- **Python 3.11+**
- **Node.js 20+**
- **OpenAI API key**

## Quick Start

### 1. Environment Setup

```bash
# From the project root
cp .env.example .env
# Edit .env and paste your real OpenAI API key
```

### 2. Backend

```bash
cd backend

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server (runs on http://localhost:8000)
python -m backend.main
```

> **Tip:** Run from the project root (`agentic-security-ui/`) so that Python resolves the `backend` package correctly:
>
> ```bash
> cd /path/to/agentic-security-ui
> python -m backend.main
> ```

### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server (runs on http://localhost:5173)
npm run dev
```

Open **http://localhost:5173** in your browser.

## API Endpoints

| Method | Path                        | Description                     |
|--------|-----------------------------|---------------------------------|
| GET    | `/api/v1/categories`        | List categories                 |
| GET    | `/api/v1/items?category=…`  | List item summaries             |
| GET    | `/api/v1/items/{id}?category=…` | Get AI-generated item detail |
| GET    | `/health`                   | Health check                    |

## Environment Variables

| Variable           | Default               | Description                |
|--------------------|-----------------------|----------------------------|
| `OPENAI_API_KEY`   | `YOUR_API_KEY_HERE`   | Your OpenAI API key        |
| `OPENAI_MODEL_NAME`| `gpt-4o-mini`         | OpenAI model to use        |
| `HOST`             | `0.0.0.0`             | Backend host               |
| `PORT`             | `8000`                | Backend port               |
| `CORS_ORIGINS`     | `http://localhost:5173,http://localhost:3000` | Allowed CORS origins |

## Tech Stack

- **Backend:** FastAPI, Pydantic v2, OpenAI Python SDK, uvicorn
- **Frontend:** React 19, TypeScript, Vite, React Router v7
- **Styling:** Custom CSS (dark theme, responsive)
