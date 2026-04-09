"""API routes for Echo."""

from src.api.records import router as records_router
from src.api.insights import router as insights_router

__all__ = ["records_router", "insights_router"]
