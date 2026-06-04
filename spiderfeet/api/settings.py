"""API runtime settings (no secrets)."""

import os

API_PREFIX = "/api/v1"

DEFAULT_HOST = os.environ.get("SPIDERFEET_API_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("SPIDERFEET_API_PORT", "8000"))

# Widget dev server (webpack) — stage 2 CORS
DEFAULT_CORS_ORIGINS = [
    "http://127.0.0.1:4001",
    "http://localhost:4001",
]
