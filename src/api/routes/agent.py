"""
Agent query endpoints.

Provides /agent/query endpoint for interacting with the Solution Engineering Agent.
"""

import asyncio
import time
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.api.dependencies import get_orchestrator_agent
from src.agents.classifier import QueryClassifier
from src.config import get_settings
from src.utils.logging import get_logger


if TYPE_CHECKING:
    from src.agents.orchestrator import OrchestratorAgent

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


class ExecutionStepResponse(BaseModel):
    """Details about a single executed step."""
    step_number: int = Field(..., description="Sequential step number")
    tool: str = Field(..., description="The tool/agent used: 'research', 'architecture', or 'code'")
    query: str = Field(..., description="The query or instruction for this step")
    status: str = Field(..., description="Execution status: 'completed', 'failed', 'skipped'")
    output_preview: str = Field(default="", description="First 500 chars of the step output")


class VerificationScoreResponse(BaseModel):
    """Detailed verification scores by dimension."""
    overall: float = Field(..., description="Weighted overall score (0.0-1.0)")
    correctness: float = Field(..., description="Factual accuracy score (0.0-1.0)")
    completeness: float = Field(..., description="Coverage/thoroughness score (0.0-1.0)")
    consistency: float = Field(..., description="Internal coherence score (0.0-1.0)")


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
        description="The sub-agent(s) that processed the query: 'researcher', 'architect', 'ghcp_coding', or comma-separated list",
    )
    turn_count: int = Field(
        default=1,
        description="The number of turns (messages) in this conversation session",
    )
    verification_score: float | None = Field(
        default=None,
        description="Quality score from verification (0.0-1.0). Scores >= 0.8 are considered acceptable.",
    )
    iterations_used: int = Field(
        default=1,
        description="Number of Plan-Execute-Verify cycles used to generate the response",
    )
    requires_human_review: bool = Field(
        default=False,
        description="True if verification failed after max iterations and human review is recommended",
    )
    plan_summary: str | None = Field(
        default=None,
        description="Brief summary of the execution plan used to generate this response",
    )
    plan_rationale: str | None = Field(
        default=None,
        description="Explanation of why the execution plan was structured this way",
    )
    execution_steps: list[ExecutionStepResponse] = Field(
        default_factory=list,
        description="Details of each executed step including tool used, query, and status",
    )
    score_details: VerificationScoreResponse | None = Field(
        default=None,
        description="Detailed verification scores by dimension (correctness, completeness, consistency)",
    )
    query_category: str | None = Field(
        default=None,
        description="Classification of the query: 'factual', 'howto', 'architecture', 'code', or 'complex'",
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
    agent: Annotated["OrchestratorAgent", Depends(get_orchestrator_agent)],
) -> QueryResponse:
    """
    Process a user query and return an agent response.

    The agent automatically routes queries to the appropriate sub-agent:
    - Research queries → ResearcherAgent (Microsoft Learn MCP)
    - Architecture queries → ArchitectAgent (Azure MCP)
    - Code/CLI queries → GHCPCodingAgent (GitHub Copilot SDK)

    Args:
        request: The query request containing the user's question.
        agent: OrchestratorAgent instance (injected).

    Returns:
        QueryResponse with the agent's answer.

    Raises:
        HTTPException: For validation errors or service failures.
    """
    start_time = time.perf_counter()
    settings = get_settings()

    try:
        # Classify query to determine appropriate timeout
        classifier = QueryClassifier()
        category = classifier.classify(request.content)
        
        # Use extended timeout for complex queries
        if category.value == "complex":
            timeout = settings.api_complex_timeout_seconds
        else:
            timeout = settings.api_request_timeout_seconds
        
        logger.info(
            "Received query",
            content_preview=request.content[:100] if request.content else "",
            session_id=request.session_id,
            category=category.value,
            timeout_seconds=timeout,
        )

        # Process query through OrchestratorAgent with timeout protection
        try:
            agent_response = await asyncio.wait_for(
                agent.run(request.content, session_id=request.session_id),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            processing_time_ms = int((time.perf_counter() - start_time) * 1000)
            logger.warning(
                "Query timed out",
                timeout_seconds=timeout,
                processing_time_ms=processing_time_ms,
                category=category.value,
            )
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail={
                    "error_code": "REQUEST_TIMEOUT",
                    "message": f"Query processing timed out after {timeout} seconds",
                    "processing_time_ms": processing_time_ms,
                    "category": category.value,
                },
            )

        processing_time_ms = int((time.perf_counter() - start_time) * 1000)

        logger.info(
            "Query processed",
            processing_time_ms=processing_time_ms,
            session_id=agent_response.session_id,
            agent_used=agent_response.agent_used,
            turn_count=agent_response.turn_count,
            verification_score=agent_response.verification_score,
            iterations_used=agent_response.iterations_used,
        )

        # Convert execution steps to response format
        execution_steps = [
            ExecutionStepResponse(
                step_number=step.step_number,
                tool=step.tool,
                query=step.query,
                status=step.status,
                output_preview=step.output_preview,
            )
            for step in agent_response.execution_steps
        ] if agent_response.execution_steps else []
        
        # Convert score details to response format
        score_details = None
        if agent_response.score_details:
            score_details = VerificationScoreResponse(
                overall=agent_response.score_details.overall,
                correctness=agent_response.score_details.correctness,
                completeness=agent_response.score_details.completeness,
                consistency=agent_response.score_details.consistency,
            )
        
        return QueryResponse(
            content=agent_response.content,
            processing_time_ms=processing_time_ms,
            session_id=agent_response.session_id,
            agent_used=agent_response.agent_used,
            turn_count=agent_response.turn_count,
            verification_score=agent_response.verification_score,
            iterations_used=agent_response.iterations_used,
            requires_human_review=agent_response.requires_human_review,
            plan_summary=agent_response.plan_summary,
            plan_rationale=agent_response.plan_rationale,
            execution_steps=execution_steps,
            score_details=score_details,
            query_category=agent_response.query_category,
        )

    except Exception as e:
        processing_time_ms = int((time.perf_counter() - start_time) * 1000)
        error_type = type(e).__name__
        error_message = str(e)
        
        logger.exception(
            "Unexpected error processing query",
            error_type=error_type,
            error_message=error_message,
            processing_time_ms=processing_time_ms,
            content_preview=request.content[:100] if request.content else "",
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "error_type": error_type,
                "error_details": error_message[:500],  # Include truncated error details
                "processing_time_ms": processing_time_ms,
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
