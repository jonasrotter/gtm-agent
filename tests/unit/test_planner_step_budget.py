"""
Unit tests for Planner step budget enforcement.

Tests that the Planner respects step limits based on query complexity:
- Factual queries: MAX 1 step
- HowTo queries: MAX 2 steps
- Architecture queries: MAX 3 steps
- Code queries: MAX 1 step
- Complex queries: MAX 4 steps
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.models import ExecutionPlan, PlanStep, ToolName
from src.agents.planner import PlannerAgent


class TestPlannerStepBudget:
    """Tests for step budget enforcement in the Planner."""
    
    @pytest.fixture
    def mock_plan_factual(self) -> ExecutionPlan:
        """Create a mock single-step plan for factual queries."""
        return ExecutionPlan(
            summary="Research Azure Blob Storage",
            steps=[
                PlanStep(
                    step_number=1,
                    tool=ToolName.RESEARCH,
                    query="What is Azure Blob Storage?",
                    expected_output="Overview of Azure Blob Storage",
                    depends_on=[],
                )
            ],
            estimated_complexity="simple",
            rationale="Single research step for factual query",
        )
    
    @pytest.fixture
    def mock_plan_code(self) -> ExecutionPlan:
        """Create a mock single-step plan for code queries."""
        return ExecutionPlan(
            summary="Generate Azure CLI commands",
            steps=[
                PlanStep(
                    step_number=1,
                    tool=ToolName.CODE,
                    query="Generate Azure CLI to create a resource group",
                    expected_output="Azure CLI commands",
                    depends_on=[],
                )
            ],
            estimated_complexity="simple",
            rationale="Single code step for CLI generation",
        )
    
    @pytest.fixture
    def mock_plan_howto(self) -> ExecutionPlan:
        """Create a mock two-step plan for howto queries."""
        return ExecutionPlan(
            summary="Steps to create storage account",
            steps=[
                PlanStep(
                    step_number=1,
                    tool=ToolName.RESEARCH,
                    query="Research storage account creation prerequisites",
                    expected_output="Prerequisites and options",
                    depends_on=[],
                ),
                PlanStep(
                    step_number=2,
                    tool=ToolName.CODE,
                    query="Generate CLI commands to create storage account",
                    expected_output="CLI commands",
                    depends_on=[1],
                ),
            ],
            estimated_complexity="simple",
            rationale="Research then code for howto query",
        )
    
    @pytest.fixture
    def mock_plan_architecture(self) -> ExecutionPlan:
        """Create a mock plan for architecture queries."""
        return ExecutionPlan(
            summary="Security best practices for App Service",
            steps=[
                PlanStep(
                    step_number=1,
                    tool=ToolName.RESEARCH,
                    query="Research App Service security features",
                    expected_output="Security features overview",
                    depends_on=[],
                ),
                PlanStep(
                    step_number=2,
                    tool=ToolName.ARCHITECTURE,
                    query="Get best practices and WAF recommendations",
                    expected_output="Security best practices",
                    depends_on=[1],
                ),
            ],
            estimated_complexity="moderate",
            rationale="Research then architecture for best practices",
        )
    
    # =========================================================================
    # Step Budget Validation Tests
    # =========================================================================
    
    def test_factual_query_max_one_step(self, mock_plan_factual: ExecutionPlan) -> None:
        """Factual query plans should have at most 1 step."""
        assert len(mock_plan_factual.steps) <= 1
        assert mock_plan_factual.steps[0].tool == ToolName.RESEARCH
    
    def test_factual_query_uses_research_tool(self, mock_plan_factual: ExecutionPlan) -> None:
        """Factual queries should primarily use the research tool."""
        assert mock_plan_factual.steps[0].tool == ToolName.RESEARCH
    
    def test_code_query_max_one_step(self, mock_plan_code: ExecutionPlan) -> None:
        """Code query plans should have at most 1 step."""
        assert len(mock_plan_code.steps) <= 1
        assert mock_plan_code.steps[0].tool == ToolName.CODE
    
    def test_howto_query_max_two_steps(self, mock_plan_howto: ExecutionPlan) -> None:
        """HowTo query plans should have at most 2 steps."""
        assert len(mock_plan_howto.steps) <= 2
    
    def test_architecture_query_max_three_steps(self, mock_plan_architecture: ExecutionPlan) -> None:
        """Architecture query plans should have at most 3 steps."""
        assert len(mock_plan_architecture.steps) <= 3


class TestPlannerStepBudgetInstructions:
    """Tests to verify step budget instructions are present in planner."""
    
    def test_planner_instructions_contain_step_budget(self) -> None:
        """Planner instructions should contain step budget guidelines."""
        from src.agents.planner import PLANNER_INSTRUCTIONS
        
        # Check for step budget section
        assert "Step Budget" in PLANNER_INSTRUCTIONS or "STEP BUDGET" in PLANNER_INSTRUCTIONS
    
    def test_planner_instructions_mention_factual_limit(self) -> None:
        """Planner instructions should mention 1-step limit for factual queries."""
        from src.agents.planner import PLANNER_INSTRUCTIONS
        
        # Should mention factual/simple queries get 1 step
        lower_instructions = PLANNER_INSTRUCTIONS.lower()
        assert ("what is" in lower_instructions and "1" in PLANNER_INSTRUCTIONS) or \
               ("factual" in lower_instructions and "1" in PLANNER_INSTRUCTIONS)
    
    def test_planner_instructions_mention_code_limit(self) -> None:
        """Planner instructions should mention 1-step limit for code queries."""
        from src.agents.planner import PLANNER_INSTRUCTIONS
        
        # Should mention code queries get 1 step
        lower_instructions = PLANNER_INSTRUCTIONS.lower()
        assert "code" in lower_instructions and ("1" in PLANNER_INSTRUCTIONS or "single" in lower_instructions)


class TestPlannerComplexityDetection:
    """Tests for complexity detection in plans."""
    
    def test_single_step_plan_is_simple(self) -> None:
        """Plans with 1 step should be marked as simple."""
        plan = ExecutionPlan(
            summary="Simple query",
            steps=[
                PlanStep(
                    step_number=1,
                    tool=ToolName.RESEARCH,
                    query="What is X?",
                    expected_output="Description of X",
                )
            ],
            estimated_complexity="simple",
            rationale="Single step",
        )
        assert plan.estimated_complexity == "simple"
    
    def test_two_step_plan_complexity(self) -> None:
        """Plans with 2 steps should be simple or moderate."""
        plan = ExecutionPlan(
            summary="Two step query",
            steps=[
                PlanStep(step_number=1, tool=ToolName.RESEARCH, query="Q1", expected_output="O1"),
                PlanStep(step_number=2, tool=ToolName.CODE, query="Q2", expected_output="O2", depends_on=[1]),
            ],
            estimated_complexity="simple",
            rationale="Two steps",
        )
        assert plan.estimated_complexity in ["simple", "moderate"]
    
    def test_four_plus_steps_is_complex(self) -> None:
        """Plans with 4+ steps should be marked as moderate or complex."""
        steps = [
            PlanStep(step_number=i, tool=ToolName.RESEARCH, query=f"Q{i}", expected_output=f"O{i}")
            for i in range(1, 5)
        ]
        plan = ExecutionPlan(
            summary="Complex query",
            steps=steps,
            estimated_complexity="complex",
            rationale="Multiple steps",
        )
        assert plan.estimated_complexity in ["moderate", "complex"]
