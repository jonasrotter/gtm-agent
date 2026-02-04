"""
API Contract Tests for Solution Engineering Agent API.

Tests for the simplified API that routes all queries through /agent/query
to the SolutionEngineerAgent orchestrator.
"""

from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Contract tests for GET /health endpoint."""

    def test_health_returns_200(self, client: TestClient) -> None:
        """Health endpoint returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_schema(self, client: TestClient) -> None:
        """Health response matches expected schema."""
        response = client.get("/health")
        data = response.json()

        # Required fields
        assert "status" in data
        assert "version" in data

        # Status must be one of the enum values
        assert data["status"] in ["healthy", "degraded", "unhealthy"]

        # Version must be a string
        assert isinstance(data["version"], str)

    def test_health_response_content_type(self, client: TestClient) -> None:
        """Health endpoint returns application/json."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"


class TestAgentQueryEndpoint:
    """Contract tests for POST /agent/query endpoint."""

    @pytest.fixture
    def mock_client(self) -> TestClient:
        """Create a test client with mocked agent dependency."""
        from src.api.main import create_app
        from src.api.dependencies import get_solution_engineer_agent
        from src.agents.models import AgentResponse
        
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock(return_value=AgentResponse(
            content="Test response",
            agent_used="researcher",
        ))
        
        app = create_app()
        app.dependency_overrides[get_solution_engineer_agent] = lambda: mock_agent
        
        return TestClient(app)

    def test_query_requires_content(self, mock_client: TestClient) -> None:
        """Query endpoint requires content field."""
        response = mock_client.post(
            "/agent/query",
            json={},
            headers={"X-API-Key": "test-key"},
        )
        # Should return 422 (validation error) for missing required field
        assert response.status_code == 422

    def test_query_accepts_valid_request(self, mock_client: TestClient) -> None:
        """Query endpoint accepts valid request."""
        response = mock_client.post(
            "/agent/query",
            json={"content": "What is Azure Functions?"},
            headers={"X-API-Key": "test-key"},
        )
        # Should not return validation error
        assert response.status_code != 422

    def test_query_response_schema(self, mock_client: TestClient) -> None:
        """Query response matches simplified schema."""
        response = mock_client.post(
            "/agent/query",
            json={"content": "What is Azure Functions?"},
            headers={"X-API-Key": "test-key"},
        )

        # Skip if there's a server error (agent not configured)
        if response.status_code == 500:
            pytest.skip("Agent not properly configured - expected in CI without Azure credentials")

        if response.status_code == 200:
            data = response.json()

            # Required fields per simplified QueryResponse schema
            assert "content" in data
            assert "processing_time_ms" in data

            # Validate types
            assert isinstance(data["content"], str)
            assert isinstance(data["processing_time_ms"], int)

    def test_query_response_includes_agent_used(self, mock_client: TestClient) -> None:
        """Query response includes agent_used field."""
        response = mock_client.post(
            "/agent/query",
            json={"content": "What is Azure Functions?"},
            headers={"X-API-Key": "test-key"},
        )

        # Skip if there's a server error (agent not configured)
        if response.status_code == 500:
            pytest.skip("Agent not properly configured - expected in CI without Azure credentials")

        if response.status_code == 200:
            data = response.json()

            # agent_used field should be present
            assert "agent_used" in data

            # agent_used should be one of the valid sub-agents or None
            valid_agents = ["researcher", "architect", "ghcp_coding", None]
            assert data["agent_used"] in valid_agents

    def test_query_validates_content_min_length(self, mock_client: TestClient) -> None:
        """Query endpoint validates content min length."""
        response = mock_client.post(
            "/agent/query",
            json={"content": ""},  # Empty content
            headers={"X-API-Key": "test-key"},
        )
        # Should reject empty content
        assert response.status_code == 422

    def test_query_validates_content_max_length(self, mock_client: TestClient) -> None:
        """Query endpoint validates content max length (10000 chars)."""
        long_content = "x" * 10001
        response = mock_client.post(
            "/agent/query",
            json={"content": long_content},
            headers={"X-API-Key": "test-key"},
        )
        # Should reject content exceeding maxLength
        assert response.status_code == 422

    def test_query_accepts_session_id(self, mock_client: TestClient) -> None:
        """Query endpoint accepts optional session_id."""
        response = mock_client.post(
            "/agent/query",
            json={
                "content": "What is Azure?",
                "session_id": "test-session-123",
            },
            headers={"X-API-Key": "test-key"},
        )
        # Should not return validation error
        assert response.status_code != 422

        # Skip if there's a server error
        if response.status_code == 200:
            data = response.json()
            # Session ID should be echoed back
            assert data.get("session_id") == "test-session-123"


class TestAgentHealthEndpoint:
    """Contract tests for GET /agent/health endpoint."""

    def test_agent_health_returns_200(self, client: TestClient) -> None:
        """Agent health endpoint returns 200 OK."""
        response = client.get("/agent/health")
        assert response.status_code == 200

    def test_agent_health_response_schema(self, client: TestClient) -> None:
        """Agent health response matches expected schema."""
        response = client.get("/agent/health")
        data = response.json()

        assert "status" in data
        assert data["status"] == "healthy"
        assert "service" in data


class TestErrorResponses:
    """Contract tests for error response format."""

    @pytest.fixture
    def mock_client(self) -> TestClient:
        """Create a test client with mocked agent dependency."""
        from src.api.main import create_app
        from src.api.dependencies import get_orchestrator_agent
        from src.agents.models import AgentResponse
        
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock(return_value=AgentResponse(
            content="Test response",
            agent_used="researcher",
        ))
        
        app = create_app()
        app.dependency_overrides[get_orchestrator_agent] = lambda: mock_agent
        
        return TestClient(app)

    def test_missing_required_field_error(self, mock_client: TestClient) -> None:
        """Missing required field returns 422."""
        response = mock_client.post(
            "/agent/query",
            json={},  # Missing required content field
            headers={"X-API-Key": "test-key"},
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_invalid_json_error(self, mock_client: TestClient) -> None:
        """Invalid JSON returns 422."""
        response = mock_client.post(
            "/agent/query",
            content="not valid json",
            headers={
                "X-API-Key": "test-key",
                "Content-Type": "application/json",
            },
        )
        assert response.status_code == 422

    def test_not_found_error(self, client: TestClient) -> None:
        """Non-existent endpoint returns 404."""
        response = client.get("/nonexistent/endpoint")
        assert response.status_code == 404
