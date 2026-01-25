"""
Pytest configuration and shared fixtures.

Provides common fixtures for all test types:
- Unit tests: Mocked dependencies, isolated components
- Integration tests: Real services, test databases
- Contract tests: API schema validation
"""

import asyncio
from collections.abc import AsyncIterator, Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.api.main import app
from src.config import Settings


# Configure async test mode
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """
    Create test-specific settings.

    Returns settings configured for testing:
    - Disabled external services
    - In-memory storage
    - Debug logging
    """
    return Settings(
        log_level="DEBUG",
        azure_foundry_project_endpoint=None,
        api_key=None,  # Disable auth for tests
    )


@pytest.fixture(scope="module")
def client() -> Iterator[TestClient]:
    """
    Create a synchronous test client for the FastAPI application.

    Use this for simple synchronous tests that don't need async.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_client() -> AsyncIterator[AsyncClient]:
    """
    Create an asynchronous test client for the FastAPI application.

    Use this for async tests and when testing async endpoints.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture
def sample_query() -> dict[str, Any]:
    """Sample query data for testing."""
    return {
        "content": "What are the scaling limits for Azure Functions?",
        "query_type": "research",
    }


@pytest.fixture
def sample_architecture_query() -> dict[str, Any]:
    """Sample architecture query data for testing."""
    return {
        "content": "Review my architecture using App Service with SQL Database",
        "query_type": "architecture",
    }


@pytest.fixture
def sample_hypothesis_query() -> dict[str, Any]:
    """Sample hypothesis validation query for testing."""
    return {
        "content": "I believe Azure Functions with Premium plan can handle 1000 RPS",
        "query_type": "hypothesis",
    }


@pytest.fixture
def invalid_query() -> dict[str, Any]:
    """Invalid query data for testing error handling."""
    return {
        "content": "",  # Empty content should fail validation
    }


# Markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "contract: mark test as a contract test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow-running"
    )
    config.addinivalue_line(
        "markers", "requires_azure: mark test as requiring Azure credentials"
    )
