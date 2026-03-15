"""
Aggregates all v1 API routes.
"""
from fastapi import APIRouter

from app.api.v1 import contents, upload, health

api_router = APIRouter()

api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
