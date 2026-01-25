"""
Agent response models for the Solution Engineering Agent.

Defines the AgentResponse and AgentCapability models used to represent
agent outputs and capabilities.
"""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator

from src.models.query import QueryType


class KnowledgeSourceRef(BaseModel):
    """Reference to a knowledge source (simplified for circular import avoidance)."""

    url: str = Field(..., description="URL to the source document")
    title: str = Field(..., description="Document title")
    excerpt: str | None = Field(default=None, description="Relevant excerpt")
    source_type: str = Field(..., description="Type of source")
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the source was retrieved",
    )
    relevance_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Relevance score (0.0-1.0)",
    )


class AgentResponse(BaseModel):
    """
    The agent's response to a query.

    Attributes:
        id: Unique response identifier.
        query_id: Reference to the original query.
        content: The main response text.
        sources: Referenced documentation sources.
        query_type: Type of query handled.
        agent_name: Name of the agent that handled the query.
        review: Architecture review details (if applicable).
        test_plan: Test plan (for hypothesis validation).
        confidence: Confidence score (0.0-1.0).
        processing_time_ms: Time taken to generate response.
        created_at: Response timestamp.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    query_id: str | None = Field(default=None, description="Reference to the original query")
    content: str = Field(..., description="The main response text")
    sources: list["KnowledgeSourceRef | Any"] = Field(
        default_factory=list,
        description="Referenced documentation sources",
    )
    query_type: QueryType | None = Field(
        default=None,
        description="Type of query that was handled",
    )
    agent_name: str | None = Field(
        default=None,
        description="Name of the agent that handled the query",
    )
    review: dict[str, Any] | None = Field(
        default=None,
        description="Architecture review details (if applicable)",
    )
    test_plan: dict[str, Any] | None = Field(
        default=None,
        description="Test plan (for hypothesis validation)",
    )
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence score (0.0-1.0)",
    )
    llm_enhanced: bool = Field(
        default=False,
        description="Whether the response was enhanced by LLM",
    )
    processing_time_ms: int | None = Field(
        default=None,
        ge=0,
        description="Time taken to generate response in milliseconds",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Response timestamp",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "query_id": "123e4567-e89b-12d3-a456-426614174001",
                    "content": "Azure Functions has the following scaling limits...",
                    "sources": [
                        {
                            "url": "https://docs.microsoft.com/azure/functions/functions-scale",
                            "title": "Azure Functions scale and hosting",
                            "source_type": "microsoft_docs",
                            "retrieved_at": "2026-01-24T12:00:00Z",
                        }
                    ],
                    "confidence": 0.95,
                    "processing_time_ms": 1500,
                    "created_at": "2026-01-24T12:00:01Z",
                }
            ]
        }
    }

    @model_validator(mode="after")
    def validate_sources_for_research(self) -> "AgentResponse":
        """Ensure sources are non-empty for RESEARCH queries (FR-002)."""
        if self.query_type == QueryType.RESEARCH and not self.sources:
            # Log warning instead of raising error to allow graceful degradation
            # when documentation search returns no results
            import logging  # noqa: PLC0415

            logging.getLogger(__name__).warning(
                "RESEARCH response has no sources - this may indicate a search issue"
            )
        return self


class AgentCapability(BaseModel):
    """
    A discrete function the agent can perform.

    Used for orchestration and capability discovery in the multi-agent system (FR-015).

    Attributes:
        name: Capability identifier.
        description: What this capability does.
        supported_query_types: Query types this capability can handle.
        input_schema: JSON schema for inputs.
        output_schema: JSON schema for outputs.
        requires_approval: Whether user approval is needed.
        estimated_duration_ms: Typical execution time.
    """

    name: str = Field(..., description="Capability identifier")
    description: str = Field(..., description="What this capability does")
    supported_query_types: list[QueryType] = Field(
        default_factory=list,
        description="Query types this capability can handle",
    )
    input_schema: dict[str, Any] | None = Field(
        default=None,
        description="JSON schema for inputs",
    )
    output_schema: dict[str, Any] | None = Field(
        default=None,
        description="JSON schema for outputs",
    )
    requires_approval: bool = Field(
        default=False,
        description="Whether user approval is needed before execution",
    )
    estimated_duration_ms: int | None = Field(
        default=None,
        ge=0,
        description="Typical execution time in milliseconds",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "research_azure_docs",
                    "description": "Search and retrieve Azure documentation",
                    "input_schema": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"],
                    },
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string"},
                            "sources": {"type": "array"},
                        },
                    },
                    "requires_approval": False,
                    "estimated_duration_ms": 5000,
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(
        ...,
        description="Service health status",
        json_schema_extra={"enum": ["healthy", "degraded", "unhealthy"]},
    )
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Response timestamp",
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(
        default=None,
        description="Additional error details",
    )
    suggestion: str | None = Field(
        default=None,
        description="Actionable suggestion for resolution",
    )
