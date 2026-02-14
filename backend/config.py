"""
Configuration for the Agentic Security backend.
Supports .env file and environment variable overrides.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root (one level up from backend/)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY_HERE")
OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

# Admin
ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "changeme")
ADMIN_TOKEN_SECRET: str = os.getenv("ADMIN_TOKEN_SECRET", "agentic-security-secret-key-2024")

# Server
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))

# CORS
_default_origins = "http://localhost:5173,http://localhost:5174,http://localhost:3000,https://agentic-security-ui.vercel.app"
CORS_ORIGINS: list[str] = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _default_origins).split(",")
    if origin.strip()
]
