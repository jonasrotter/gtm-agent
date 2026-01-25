"""
API routes package.

Registers all route modules with the FastAPI application.

The main endpoint is /agent/query which routes to the SolutionEngineerAgent.
The agent internally routes queries to specialized sub-agents:
- ResearcherAgent for documentation queries
- ArchitectAgent for architecture guidance
- GHCPCodingAgent for code/CLI generation
"""

from fastapi import APIRouter

from src.api.routes.agent import router as agent_router
from src.api.routes.health import router as health_router


# Main API router that includes all sub-routers
api_router = APIRouter()

# Register routes
api_router.include_router(health_router, tags=["health"])
api_router.include_router(agent_router, prefix="/agent", tags=["agent"])


__all__ = ["api_router"]
