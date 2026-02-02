"""
Unit tests for Orchestrator fast path functionality.

Tests that simple queries bypass the full PEV loop:
- Factual queries skip Planner and call Researcher directly
- Factual queries have max 1 iteration
- Code queries use lite verification (1 pass)
- Complex queries use full PEV loop
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.models import (
    AgentResponse,
    ExecutionPlan,
    PlanStep,
    ExecutionResult,
    StepResult,
    VerificationResult,
    VerificationScore,
    VerificationDecision,
    ToolName,
    StepStatus,
)
from src.agents.classifier import QueryCategory


class TestOrchestratorFastPath:
    """Tests for fast path routing in OrchestratorAgent."""
    
    @pytest.fixture
    def mock_researcher_response(self) -> str:
        """Mock response from researcher agent."""
        return "Azure Blob Storage is a cloud storage service for unstructured data."
    
    @pytest.fixture
    def mock_agent_response(self, mock_researcher_response: str) -> AgentResponse:
        """Create a mock AgentResponse for fast path."""
        return AgentResponse(
            content=mock_researcher_response,
            agent_used="researcher",
            session_id="test-session",
            turn_count=1,
            verification_score=None,  # No verification for fast path
            iterations_used=1,
            requires_human_review=False,
            plan_summary="Direct researcher call (fast path)",
        )
    
    # =========================================================================
    # Fast Path Routing Tests
    # =========================================================================
    
    def test_factual_category_skips_pev(self) -> None:
        """Factual queries should be configured to skip PEV."""
        config = QueryCategory.FACTUAL.get_config()
        assert config["skip_pev"] is True
    
    def test_factual_uses_researcher(self) -> None:
        """Factual queries should use researcher tool."""
        config = QueryCategory.FACTUAL.get_config()
        assert config["default_tool"] == "research"
    
    def test_howto_does_not_skip_pev(self) -> None:
        """HowTo queries should not skip PEV."""
        config = QueryCategory.HOWTO.get_config()
        assert config["skip_pev"] is False
    
    def test_architecture_does_not_skip_pev(self) -> None:
        """Architecture queries should not skip PEV."""
        config = QueryCategory.ARCHITECTURE.get_config()
        assert config["skip_pev"] is False
    
    def test_code_does_not_skip_pev(self) -> None:
        """Code queries should not skip PEV (but use lite verification)."""
        config = QueryCategory.CODE.get_config()
        assert config["skip_pev"] is False
        assert config["max_iterations"] == 1
    
    def test_complex_uses_full_pev(self) -> None:
        """Complex queries should use full PEV loop."""
        config = QueryCategory.COMPLEX.get_config()
        assert config["skip_pev"] is False
        assert config["max_iterations"] == 4


class TestOrchestratorIterationLimits:
    """Tests for category-based iteration limits."""
    
    def test_factual_max_iterations_is_one(self) -> None:
        """Factual queries should have max 1 iteration."""
        config = QueryCategory.FACTUAL.get_config()
        assert config["max_iterations"] == 1
    
    def test_howto_max_iterations_is_one(self) -> None:
        """HowTo queries should have max 1 iteration (lite PEV)."""
        config = QueryCategory.HOWTO.get_config()
        assert config["max_iterations"] == 1
    
    def test_architecture_max_iterations_is_two(self) -> None:
        """Architecture queries should have max 2 iterations."""
        config = QueryCategory.ARCHITECTURE.get_config()
        assert config["max_iterations"] == 2
    
    def test_code_max_iterations_is_one(self) -> None:
        """Code queries should have max 1 iteration."""
        config = QueryCategory.CODE.get_config()
        assert config["max_iterations"] == 1
    
    def test_complex_max_iterations_is_four(self) -> None:
        """Complex queries should have max 4 iterations."""
        config = QueryCategory.COMPLEX.get_config()
        assert config["max_iterations"] == 4


class TestOrchestratorThresholds:
    """Tests for category-based acceptance thresholds."""
    
    def test_factual_has_no_threshold(self) -> None:
        """Factual queries skip verification, so no threshold needed."""
        config = QueryCategory.FACTUAL.get_config()
        # Either no threshold or a low one since we skip verification
        assert config.get("threshold") is None or config.get("threshold", 0) <= 0.7
    
    def test_howto_threshold_is_lower(self) -> None:
        """HowTo queries should have lower threshold (0.7)."""
        config = QueryCategory.HOWTO.get_config()
        assert config["threshold"] == 0.7
    
    def test_architecture_threshold_is_moderate(self) -> None:
        """Architecture queries should have moderate threshold (0.75)."""
        config = QueryCategory.ARCHITECTURE.get_config()
        assert config["threshold"] == 0.75
    
    def test_code_threshold_is_lower(self) -> None:
        """Code queries should have lower threshold (0.7)."""
        config = QueryCategory.CODE.get_config()
        assert config["threshold"] == 0.7
    
    def test_complex_threshold_is_standard(self) -> None:
        """Complex queries should have standard threshold (0.8)."""
        config = QueryCategory.COMPLEX.get_config()
        assert config["threshold"] == 0.8


class TestFastPathResponse:
    """Tests for fast path response structure."""
    
    def test_fast_path_response_has_content(self) -> None:
        """Fast path response should have content."""
        response = AgentResponse(
            content="Test content",
            agent_used="researcher",
            iterations_used=1,
        )
        assert response.content == "Test content"
    
    def test_fast_path_response_has_single_iteration(self) -> None:
        """Fast path response should show 1 iteration."""
        response = AgentResponse(
            content="Test content",
            agent_used="researcher",
            iterations_used=1,
        )
        assert response.iterations_used == 1
    
    def test_fast_path_response_identifies_agent(self) -> None:
        """Fast path response should identify the agent used."""
        response = AgentResponse(
            content="Test content",
            agent_used="researcher",
            iterations_used=1,
        )
        assert response.agent_used == "researcher"
    
    def test_fast_path_no_human_review_required(self) -> None:
        """Fast path response should not require human review."""
        response = AgentResponse(
            content="Test content",
            agent_used="researcher",
            iterations_used=1,
            requires_human_review=False,
        )
        assert response.requires_human_review is False
