"""
FastAPI application entry point.
Mounts API routes and configures CORS.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import engine, Base
from app.models import Content  # noqa: F401 - ensure models are registered

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dentistry API",
    description="Backend API for dentistry content and file management",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Mount uploads directory for file access
uploads_dir = Path(__file__).resolve().parents[2] / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/api/v1/files", StaticFiles(directory=str(uploads_dir)), name="files")

# Optional: serve frontend at /app (e.g. http://127.0.0.1:8000/app/)
frontend_dir = Path(__file__).resolve().parents[2].parent / "frontend"
if frontend_dir.exists():
    app.mount("/app", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


@app.get("/")
def root():
    return {"message": "Dentistry API", "docs": "/docs"}
