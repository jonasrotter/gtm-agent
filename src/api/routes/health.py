"""
Health check endpoints.

Provides /health endpoint for service monitoring and readiness checks.
"""

from datetime import UTC, datetime

from fastapi import APIRouter

from src import __version__
from src.models.agent import HealthResponse


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the service.",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns service status for monitoring and load balancer health probes.

    Returns:
        HealthResponse with status, version, and timestamp.
    """
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.now(UTC),
    )
