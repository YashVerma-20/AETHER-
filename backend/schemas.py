"""AETHER Pydantic Validation Schemas.

Defines schemas for foundational health endpoints and initial data contracts.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class HealthStatusResponse(BaseModel):
    """Schema for basic application health check."""

    status: str = Field(..., description="Application operational status")
    environment: str = Field(..., description="Current running environment")
    version: str = Field(..., description="AETHER application version")


class DatabaseHealthResponse(BaseModel):
    """Schema for live database connectivity check."""

    status: str = Field(..., description="Database connectivity status: healthy or unhealthy")
    connected: bool = Field(..., description="Boolean flag confirming live connection")
    database: str = Field(..., description="Target database name")
    port: int = Field(..., description="PostgreSQL TCP port")
    version: Optional[str] = Field(None, description="PostgreSQL server version string")
    error: Optional[str] = Field(None, description="Error detail if connection fails")
