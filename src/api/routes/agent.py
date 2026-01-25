"""
Agent query endpoints.

Provides /agent/query endpoint for interacting with the Solution Engineering Agent.
"""

import time
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.api.dependencies import get_solution_engineer_agent
from src.lib.logging import get_logger


if TYPE_CHECKING:
    from src.agents.solution_engineer import SolutionEngineerAgent

router = APIRouter()
logger = get_logger(__name__)


# =============================================================================
# Request/Response Models
# =============================================================================

class QueryRequest(BaseModel):
    """Request model for agent queries."""
    content: str = Field(
        ...,
        description="The user's question or request",
        min_length=1,
        max_length=10000,
    )
    session_id: str | None = Field(
        default=None,
        description="Optional session ID for conversation continuity",
    )


class QueryResponse(BaseModel):
    """Response model for agent queries."""
    content: str = Field(
        ...,
        description="The agent's response",
    )
    processing_time_ms: int = Field(
        ...,
        description="Processing time in milliseconds",
    )
    session_id: str = Field(
        ...,
        description="Session ID for multi-turn conversation continuity. Auto-generated if not provided.",
    )
    agent_used: str | None = Field(
        default=None,
        description="The sub-agent that processed the query: 'researcher', 'architect', 'ghcp_coding', or null if no tool was called",
    )
    turn_count: int = Field(
        default=1,
        description="The number of turns (messages) in this conversation session",
    )


class ErrorResponse(BaseModel):
    """Error response model."""
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")


# =============================================================================
# Endpoints
# =============================================================================

@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit a query to the agent",
    description="Submit a question or request to the Solution Engineering Agent.",
    responses={
        200: {"model": QueryResponse, "description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def query_agent(
    request: QueryRequest,
    agent: Annotated["SolutionEngineerAgent", Depends(get_solution_engineer_agent)],
) -> QueryResponse:
    """
    Process a user query and return an agent response.

    The agent automatically routes queries to the appropriate sub-agent:
    - Research queries → ResearcherAgent (Microsoft Learn MCP)
    - Architecture queries → ArchitectAgent (Azure MCP)
    - Code/CLI queries → GHCPCodingAgent (GitHub Copilot SDK)

    Args:
        request: The query request containing the user's question.
        agent: SolutionEngineerAgent instance (injected).

    Returns:
        QueryResponse with the agent's answer.

    Raises:
        HTTPException: For validation errors or service failures.
    """
    start_time = time.perf_counter()

    try:
        logger.info(
            "Received query",
            content_preview=request.content[:100] if request.content else "",
            session_id=request.session_id,
        )

        # Process query through SolutionEngineerAgent with session support
        agent_response = await agent.run(request.content, session_id=request.session_id)

        processing_time_ms = int((time.perf_counter() - start_time) * 1000)

        logger.info(
            "Query processed",
            processing_time_ms=processing_time_ms,
            session_id=agent_response.session_id,
            agent_used=agent_response.agent_used,
            turn_count=agent_response.turn_count,
        )

        return QueryResponse(
            content=agent_response.content,
            processing_time_ms=processing_time_ms,
            session_id=agent_response.session_id,
            agent_used=agent_response.agent_used,
            turn_count=agent_response.turn_count,
        )

    except Exception as e:
        logger.exception("Unexpected error processing query", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
        ) from e


@router.get(
    "/health",
    summary="Agent health check",
    description="Check if the agent service is healthy.",
)
async def agent_health() -> dict:
    """
    Simple health check for the agent service.

    Returns:
        Health status dictionary.
    """
    return {
        "status": "healthy",
        "service": "solution-engineering-agent",
    }
