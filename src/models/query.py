"""
Query models for the Solution Engineering Agent.

Defines the Query and QueryType models used to represent user requests.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class QueryType(str, Enum):
    """Classification of query intent."""

    RESEARCH = "research"
    ARCHITECTURE = "architecture"
    HYPOTHESIS = "hypothesis"
    GENERAL = "general"


class Query(BaseModel):
    """
    Represents a user's question or request to the agent.

    Attributes:
        id: Unique identifier (UUID).
        content: The user's query text (1-10000 chars).
        query_type: Classification of the query.
        context: Additional context (prior conversation, files, etc.).
        session_id: Session identifier for conversation continuity.
        created_at: Timestamp of query creation.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's query text",
    )
    query_type: QueryType = Field(
        default=QueryType.GENERAL,
        description="Classification of the query",
    )
    context: dict[str, Any] | None = Field(
        default=None,
        description="Additional context for the query",
    )
    session_id: str | None = Field(
        default=None,
        description="Session identifier for conversation continuity",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp of query creation",
    )

    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "examples": [
                {
                    "content": "What are the scaling limits for Azure Functions?",
                    "query_type": "research",
                },
                {
                    "content": "Review my architecture using App Service with SQL Database",
                    "query_type": "architecture",
                },
            ]
        },
    }

    @field_validator("content", mode="before")
    @classmethod
    def strip_content(cls, v: str) -> str:
        """Strip whitespace from content."""
        return v.strip() if isinstance(v, str) else v

    @field_validator("session_id", mode="before")
    @classmethod
    def validate_session_id(cls, v: str | None) -> str | None:
        """Validate session_id is a valid UUID if provided."""
        if v is not None:
            # Basic UUID format validation
            v = v.strip()
            if len(v) != 36 or v.count("-") != 4:
                raise ValueError("session_id must be a valid UUID")
        return v


class QueryRequest(BaseModel):
    """
    API request model for submitting a query.

    This is the request body for POST /agent/query.
    """

    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The query text",
    )
    query_type: QueryType | None = Field(
        default=None,
        description="Type of query (auto-detected if not specified)",
    )
    context: dict[str, Any] | None = Field(
        default=None,
        description="Additional context for the query",
    )
    session_id: str | None = Field(
        default=None,
        description="Session ID for conversation continuity",
    )

    def to_query(self) -> Query:
        """Convert request to Query model."""
        return Query(
            content=self.content,
            query_type=self.query_type or QueryType.GENERAL,
            context=self.context,
            session_id=self.session_id,
        )
