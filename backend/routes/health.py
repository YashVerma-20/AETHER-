"""AETHER Health and Diagnostic API Endpoints."""

import logging
from fastapi import APIRouter, status, Response
from backend.config import get_settings
from backend.database import check_database_connection
from backend.schemas import HealthStatusResponse, DatabaseHealthResponse

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])


@router.get("", response_model=HealthStatusResponse, status_code=status.HTTP_200_OK)
def get_health() -> HealthStatusResponse:
    """Return overall FastAPI application health status."""
    return HealthStatusResponse(
        status="ok",
        environment=settings.AETHER_ENV,
        version="0.3.0",
    )


@router.get("/database", response_model=DatabaseHealthResponse)
def get_database_health(response: Response) -> DatabaseHealthResponse:
    """Verify live PostgreSQL database connectivity.
    
    Executes a real ping query against the local PostgreSQL cluster on port 5433.
    Returns HTTP 200 if connected, or HTTP 503 if unreachable.
    """
    db_check = check_database_connection()
    if not db_check.get("connected"):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        response.status_code = status.HTTP_200_OK

    return DatabaseHealthResponse(
        status=db_check.get("status", "unhealthy"),
        connected=db_check.get("connected", False),
        database=db_check.get("database", settings.DB_NAME),
        port=db_check.get("port", settings.DB_PORT),
        version=db_check.get("version"),
        error=db_check.get("error"),
    )
