"""AETHER FastAPI Application Entrypoint.

Configures application lifecycle, CORS, routing, and exception handlers.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings
from backend.routes.health import router as health_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("aether")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for FastAPI application.
    
    Ensures lightweight startup without loading LLM models or heavy state.
    """
    logger.info("Initializing AETHER backend foundation (Environment: %s)", settings.AETHER_ENV)
    yield
    logger.info("Shutting down AETHER backend foundation")


app = FastAPI(
    title="AETHER Backend Foundation",
    description="Adaptive Evaluation and Teaming through Historical Evidence and Reasoning — API & Database Service",
    version="0.3.0",
    lifespan=lifespan,
)

# CORS configuration for local React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register foundational health routes
app.include_router(health_router)
