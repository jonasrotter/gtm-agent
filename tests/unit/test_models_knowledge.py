"""
Unit tests for KnowledgeSource and SourceType models.

TDD: These tests should FAIL initially until models are implemented.
"""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError


class TestSourceType:
    """Tests for SourceType enum."""

    def test_microsoft_docs_value(self) -> None:
        """SourceType has MICROSOFT_DOCS value."""
        from src.models.knowledge import SourceType

        assert SourceType.MICROSOFT_DOCS == "microsoft_docs"

    def test_azure_architecture_center_value(self) -> None:
        """SourceType has AZURE_ARCHITECTURE_CENTER value."""
        from src.models.knowledge import SourceType

        assert SourceType.AZURE_ARCHITECTURE_CENTER == "azure_architecture_center"

    def test_well_architected_value(self) -> None:
        """SourceType has WELL_ARCHITECTED value."""
        from src.models.knowledge import SourceType

        assert SourceType.WELL_ARCHITECTED == "well_architected"

    def test_github_value(self) -> None:
        """SourceType has GITHUB value."""
        from src.models.knowledge import SourceType

        assert SourceType.GITHUB == "github"

    def test_other_value(self) -> None:
        """SourceType has OTHER value."""
        from src.models.knowledge import SourceType

        assert SourceType.OTHER == "other"


class TestKnowledgeSource:
    """Tests for KnowledgeSource model."""

    def test_create_minimal_knowledge_source(self) -> None:
        """Create KnowledgeSource with required fields only."""
        from src.models.knowledge import KnowledgeSource, SourceType

        source = KnowledgeSource(
            url="https://docs.microsoft.com/azure/functions",
            title="Azure Functions Overview",
            source_type=SourceType.MICROSOFT_DOCS,
        )

        assert source.url == "https://docs.microsoft.com/azure/functions"
        assert source.title == "Azure Functions Overview"
        assert source.source_type == SourceType.MICROSOFT_DOCS
        assert source.excerpt is None
        assert source.relevance_score is None

    def test_create_full_knowledge_source(self) -> None:
        """Create KnowledgeSource with all fields."""
        from src.models.knowledge import KnowledgeSource, SourceType

        source = KnowledgeSource(
            url="https://docs.microsoft.com/azure/functions",
            title="Azure Functions Overview",
            source_type=SourceType.MICROSOFT_DOCS,
            excerpt="Azure Functions is a serverless compute service...",
            relevance_score=0.95,
        )

        assert source.excerpt == "Azure Functions is a serverless compute service..."
        assert source.relevance_score == 0.95

    def test_retrieved_at_auto_generated(self) -> None:
        """retrieved_at is auto-generated if not provided."""
        from src.models.knowledge import KnowledgeSource, SourceType

        before = datetime.now(UTC)
        source = KnowledgeSource(
            url="https://docs.microsoft.com/azure/functions",
            title="Azure Functions Overview",
            source_type=SourceType.MICROSOFT_DOCS,
        )
        after = datetime.now(UTC)

        assert before <= source.retrieved_at <= after

    def test_url_required(self) -> None:
        """URL is required."""
        from src.models.knowledge import KnowledgeSource, SourceType

        with pytest.raises(ValidationError) as exc_info:
            KnowledgeSource(
                title="Azure Functions Overview",
                source_type=SourceType.MICROSOFT_DOCS,
            )
        assert "url" in str(exc_info.value)

    def test_title_required(self) -> None:
        """Title is required."""
        from src.models.knowledge import KnowledgeSource, SourceType

        with pytest.raises(ValidationError) as exc_info:
            KnowledgeSource(
                url="https://docs.microsoft.com/azure/functions",
                source_type=SourceType.MICROSOFT_DOCS,
            )
        assert "title" in str(exc_info.value)

    def test_source_type_required(self) -> None:
        """source_type is required."""
        from src.models.knowledge import KnowledgeSource

        with pytest.raises(ValidationError) as exc_info:
            KnowledgeSource(
                url="https://docs.microsoft.com/azure/functions",
                title="Azure Functions Overview",
            )
        assert "source_type" in str(exc_info.value)

    def test_relevance_score_valid_range(self) -> None:
        """relevance_score must be between 0.0 and 1.0."""
        from src.models.knowledge import KnowledgeSource, SourceType

        # Valid values
        source_low = KnowledgeSource(
            url="https://docs.microsoft.com/azure/functions",
            title="Azure Functions Overview",
            source_type=SourceType.MICROSOFT_DOCS,
            relevance_score=0.0,
        )
        assert source_low.relevance_score == 0.0

        source_high = KnowledgeSource(
            url="https://docs.microsoft.com/azure/functions",
            title="Azure Functions Overview",
            source_type=SourceType.MICROSOFT_DOCS,
            relevance_score=1.0,
        )
        assert source_high.relevance_score == 1.0

    def test_relevance_score_invalid_below_zero(self) -> None:
        """relevance_score below 0.0 raises ValidationError."""
        from src.models.knowledge import KnowledgeSource, SourceType

        with pytest.raises(ValidationError):
            KnowledgeSource(
                url="https://docs.microsoft.com/azure/functions",
                title="Azure Functions Overview",
                source_type=SourceType.MICROSOFT_DOCS,
                relevance_score=-0.1,
            )

    def test_relevance_score_invalid_above_one(self) -> None:
        """relevance_score above 1.0 raises ValidationError."""
        from src.models.knowledge import KnowledgeSource, SourceType

        with pytest.raises(ValidationError):
            KnowledgeSource(
                url="https://docs.microsoft.com/azure/functions",
                title="Azure Functions Overview",
                source_type=SourceType.MICROSOFT_DOCS,
                relevance_score=1.1,
            )

    def test_serialization_to_dict(self) -> None:
        """KnowledgeSource can be serialized to dict."""
        from src.models.knowledge import KnowledgeSource, SourceType

        source = KnowledgeSource(
            url="https://docs.microsoft.com/azure/functions",
            title="Azure Functions Overview",
            source_type=SourceType.MICROSOFT_DOCS,
            excerpt="Serverless compute",
            relevance_score=0.9,
        )

        data = source.model_dump()
        assert data["url"] == "https://docs.microsoft.com/azure/functions"
        assert data["title"] == "Azure Functions Overview"
        assert data["source_type"] == "microsoft_docs"
        assert data["excerpt"] == "Serverless compute"
        assert data["relevance_score"] == 0.9


class TestSearchResult:
    """Tests for SearchResult model."""

    def test_create_search_result(self) -> None:
        """Create SearchResult with sources and query."""
        from src.models.knowledge import KnowledgeSource, SearchResult, SourceType

        sources = [
            KnowledgeSource(
                url="https://docs.microsoft.com/azure/functions",
                title="Azure Functions Overview",
                source_type=SourceType.MICROSOFT_DOCS,
            ),
        ]

        result = SearchResult(
            query="What is Azure Functions?",
            sources=sources,
            total_results=1,
        )

        assert result.query == "What is Azure Functions?"
        assert len(result.sources) == 1
        assert result.total_results == 1

    def test_search_result_empty_sources_allowed(self) -> None:
        """SearchResult can have empty sources list."""
        from src.models.knowledge import SearchResult

        result = SearchResult(
            query="nonexistent topic",
            sources=[],
            total_results=0,
        )

        assert result.sources == []
        assert result.total_results == 0
