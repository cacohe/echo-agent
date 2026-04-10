"""
Echo - Personal Reflection and Decision AI Assistant
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.logger import get_logger
from src.config import config
from src.api import records_router, insights_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    config.ensure_dirs()
    logger.info("Echo starting up...")
    yield
    logger.info("Echo shutting down...")


app = FastAPI(
    title="Echo",
    description="Personal Reflection and Decision AI Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(records_router)
app.include_router(insights_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Echo",
        "version": "0.1.0",
        "description": "Personal Reflection and Decision AI Assistant",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint - used by Render for deploy verification."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host=config.API_HOST, port=config.API_PORT, reload=True)
