"""
Knowledge and documentation source models.

Defines models for representing documentation sources, search results,
and code samples retrieved from MCP servers.
"""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class SourceType(str, Enum):
    """Type of documentation source."""

    MICROSOFT_DOCS = "microsoft_docs"
    AZURE_ARCHITECTURE_CENTER = "azure_architecture_center"
    WELL_ARCHITECTED = "well_architected"
    GITHUB = "github"
    OTHER = "other"


class FeatureStatus(str, Enum):
    """Status of an Azure feature."""

    GA = "ga"
    PREVIEW = "preview"
    DEPRECATED = "deprecated"
    UNKNOWN = "unknown"


class KnowledgeSource(BaseModel):
    """
    A reference to official documentation or guidance.

    Represents a single documentation source retrieved from MCP servers
    like MicrosoftDocs or Context7.
    """

    url: str = Field(..., description="URL to the source document")
    title: str = Field(..., description="Document title")
    excerpt: str | None = Field(default=None, description="Relevant excerpt from the document")
    source_type: SourceType = Field(..., description="Type of source")
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the source was retrieved",
    )
    relevance_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="How relevant this source is (0.0-1.0)",
    )
    feature_status: FeatureStatus | None = Field(
        default=None,
        description="Status of the feature (GA, preview, deprecated)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://docs.microsoft.com/azure/functions/functions-scale",
                    "title": "Azure Functions scale and hosting",
                    "excerpt": "Azure Functions scales automatically based on demand...",
                    "source_type": "microsoft_docs",
                    "relevance_score": 0.95,
                }
            ]
        }
    }


class SearchResult(BaseModel):
    """
    Result of a documentation search.

    Contains the original query, matched sources, and metadata.
    """

    query: str = Field(..., description="The original search query")
    sources: list[KnowledgeSource] = Field(
        default_factory=list,
        description="Matched documentation sources",
    )
    total_results: int = Field(
        default=0,
        ge=0,
        description="Total number of results found",
    )
    search_time_ms: int | None = Field(
        default=None,
        ge=0,
        description="Time taken to perform the search in milliseconds",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "Azure Functions scaling",
                    "sources": [
                        {
                            "url": "https://docs.microsoft.com/azure/functions/functions-scale",
                            "title": "Azure Functions scale and hosting",
                            "source_type": "microsoft_docs",
                            "retrieved_at": "2026-01-24T12:00:00Z",
                        }
                    ],
                    "total_results": 1,
                    "search_time_ms": 250,
                }
            ]
        }
    }


class DocumentContent(BaseModel):
    """
    Full content of a fetched document.

    Contains the complete document content after fetching from a URL.
    """

    url: str = Field(..., description="URL of the document")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Full document content (markdown)")
    excerpt: str | None = Field(default=None, description="Summary excerpt")
    source_type: SourceType = Field(
        default=SourceType.MICROSOFT_DOCS,
        description="Type of source",
    )
    feature_status: FeatureStatus | None = Field(
        default=None,
        description="Detected feature status",
    )
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the document was fetched",
    )


class CodeSample(BaseModel):
    """
    A code sample from documentation.

    Represents a code snippet retrieved from documentation.
    """

    code: str = Field(..., description="The code snippet")
    language: str = Field(..., description="Programming language")
    title: str | None = Field(default=None, description="Sample title or description")
    source_url: str | None = Field(default=None, description="URL where sample was found")
    context: str | None = Field(default=None, description="Surrounding context")


class CodeSampleSearchResult(BaseModel):
    """
    Result of a code sample search.

    Contains matching code samples from documentation.
    """

    query: str = Field(..., description="The original search query")
    samples: list[CodeSample] = Field(
        default_factory=list,
        description="Matched code samples",
    )
    language_filter: str | None = Field(
        default=None,
        description="Language filter applied (if any)",
    )


# Request models for API endpoints


class SearchRequest(BaseModel):
    """Request model for POST /research/search."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Search query",
    )
    source_types: list[SourceType] | None = Field(
        default=None,
        description="Filter by source types",
    )
    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of results",
    )


class FetchRequest(BaseModel):
    """Request model for POST /research/fetch."""

    url: str = Field(
        ...,
        min_length=1,
        description="URL to fetch",
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format."""
        v = v.strip()
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class CodeSampleSearchRequest(BaseModel):
    """Request model for POST /research/code-samples."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Search query for code samples",
    )
    language: str | None = Field(
        default=None,
        description="Filter by programming language",
    )
    max_results: int = Field(
        default=10,
        ge=1,
        le=20,
        description="Maximum number of samples",
    )
