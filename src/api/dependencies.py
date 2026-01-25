"""
API dependencies for dependency injection.

Provides shared dependencies for route handlers via FastAPI's Depends system.
"""

from functools import lru_cache
from typing import TYPE_CHECKING, Any

from fastapi import Depends, Header, HTTPException, status

from src.config import Settings, get_settings
from src.lib.logging import get_logger


if TYPE_CHECKING:
    from src.agents.researcher import ResearcherAgent
    from src.agents.architect import ArchitectAgent
    from src.agents.ghcp_coding_agent import GHCPCodingAgent
    from src.agents.solution_engineer import SolutionEngineerAgent

logger = get_logger(__name__)


@lru_cache
def get_researcher_agent() -> "ResearcherAgent":
    """
    Get ResearcherAgent singleton.

    Returns:
        Shared ResearcherAgent instance with HostedMCPTool integration.
    """
    from src.agents.researcher import ResearcherAgent  # noqa: PLC0415

    return ResearcherAgent()


@lru_cache
def get_architect_agent() -> "ArchitectAgent":
    """
    Get ArchitectAgent singleton.

    Returns:
        Shared ArchitectAgent instance with HostedMCPTool integration.
    """
    from src.agents.architect import ArchitectAgent  # noqa: PLC0415

    return ArchitectAgent()


@lru_cache
def get_ghcp_coding_agent() -> "GHCPCodingAgent":
    """
    Get GHCPCodingAgent singleton.

    Returns:
        Shared GHCPCodingAgent instance with GitHub Copilot SDK integration.
    """
    from src.agents.ghcp_coding_agent import GHCPCodingAgent  # noqa: PLC0415

    return GHCPCodingAgent()


@lru_cache
def get_solution_engineer_agent() -> "SolutionEngineerAgent":
    """
    Get SolutionEngineerAgent singleton.

    Returns:
        Shared SolutionEngineerAgent orchestrator instance.
    """
    from src.agents.solution_engineer import SolutionEngineerAgent  # noqa: PLC0415

    return SolutionEngineerAgent()


async def verify_api_key(
    x_api_key: str | None = Header(None, alias="X-API-Key"),
    settings: Settings = Depends(get_settings),  # noqa: B008
) -> str | None:
    """
    Verify the API key if authentication is enabled.

    Args:
        x_api_key: The API key from the X-API-Key header.
        settings: Application settings.

    Returns:
        The verified API key or None if auth is disabled.

    Raises:
        HTTPException: If the API key is invalid or missing when required.
    """
    # If no API key is configured, authentication is disabled
    if settings.api_key is None:
        return None

    # API key is configured, so it's required
    if x_api_key is None:
        logger.warning("Missing API key in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "MISSING_API_KEY",
                "message": "API key is required",
                "suggestion": "Include X-API-Key header with your API key",
            },
        )

    if x_api_key != settings.api_key.get_secret_value():
        logger.warning("Invalid API key in request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error_code": "INVALID_API_KEY",
                "message": "Invalid API key",
            },
        )

    return x_api_key


async def get_request_context(
    x_request_id: str | None = Header(None, alias="X-Request-ID"),
    x_session_id: str | None = Header(None, alias="X-Session-ID"),
) -> dict[str, Any]:
    """
    Extract request context from headers.

    Args:
        x_request_id: Optional request ID for tracing.
        x_session_id: Optional session ID for conversation continuity.

    Returns:
        Dictionary with request context.
    """
    return {
        "request_id": x_request_id,
        "session_id": x_session_id,
    }
