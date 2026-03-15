"""
Application configuration.
"""
import os
from pathlib import Path


class Settings:
    API_V1_PREFIX: str = "/api/v1"
    # SQLite by default; override with DATABASE_URL for PostgreSQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + str(Path(__file__).resolve().parents[2] / "dentistry.db"),
    )
    UPLOAD_DIR: Path = Path(__file__).resolve().parents[2] / "uploads"
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
