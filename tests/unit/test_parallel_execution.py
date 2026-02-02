"""
Unit tests for parallel execution logic in ExecutorAgent.

Tests the dependency graph resolution and parallel wave execution
without making actual API calls.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.agents.models import (
    ExecutionPlan,
    PlanStep,
    StepResult,
    StepStatus,
    ToolName,
)


class TestDependencyGraph:
    """Test the dependency resolution logic."""
    
    def test_no_dependencies_all_ready(self):
        """Steps with no dependencies should all be ready immediately."""
        from src.agents.executor import ExecutorAgent
        
        # Mock sub-agents
        mock_researcher = MagicMock()
        mock_researcher.as_tool.return_value = MagicMock()
        mock_architect = MagicMock()
        mock_architect.as_tool.return_value = MagicMock()
        mock_ghcp = MagicMock()
        mock_ghcp.as_tool.return_value = MagicMock()
        
        with patch('src.agents.executor.create_azure_chat_client'):
            executor = ExecutorAgent(mock_researcher, mock_architect, mock_ghcp)
        
        # Create steps with no dependencies
        steps = {
            1: PlanStep(step_number=1, tool=ToolName.RESEARCH, query="q1", expected_output="o1", depends_on=[]),
            2: PlanStep(step_number=2, tool=ToolName.ARCHITECTURE, query="q2", expected_output="o2", depends_on=[]),
            3: PlanStep(step_number=3, tool=ToolName.CODE, query="q3", expected_output="o3", depends_on=[]),
        }
        
        remaining = {1, 2, 3}
        completed = {}
        
        ready = executor._get_ready_steps(remaining, steps, completed)
        
        assert len(ready) == 3, "All 3 steps should be ready"
        ready_nums = {s.step_number for s in ready}
        assert ready_nums == {1, 2, 3}
    
    def test_linear_dependencies(self):
        """Steps with linear dependencies: 1 -> 2 -> 3."""
        from src.agents.executor import ExecutorAgent
        
        mock_researcher = MagicMock()
        mock_researcher.as_tool.return_value = MagicMock()
        mock_architect = MagicMock()
        mock_architect.as_tool.return_value = MagicMock()
        mock_ghcp = MagicMock()
        mock_ghcp.as_tool.return_value = MagicMock()
        
        with patch('src.agents.executor.create_azure_chat_client'):
            executor = ExecutorAgent(mock_researcher, mock_architect, mock_ghcp)
        
        steps = {
            1: PlanStep(step_number=1, tool=ToolName.RESEARCH, query="q1", expected_output="o1", depends_on=[]),
            2: PlanStep(step_number=2, tool=ToolName.ARCHITECTURE, query="q2", expected_output="o2", depends_on=[1]),
            3: PlanStep(step_number=3, tool=ToolName.CODE, query="q3", expected_output="o3", depends_on=[2]),
        }
        
        # Initially only step 1 is ready
        remaining = {1, 2, 3}
        completed = {}
        ready = executor._get_ready_steps(remaining, steps, completed)
        assert len(ready) == 1
        assert ready[0].step_number == 1
        
        # After step 1 completes, step 2 is ready
        completed[1] = StepResult(step_number=1, tool_used="research", status=StepStatus.COMPLETED)
        remaining = {2, 3}
        ready = executor._get_ready_steps(remaining, steps, completed)
        assert len(ready) == 1
        assert ready[0].step_number == 2
        
        # After step 2 completes, step 3 is ready
        completed[2] = StepResult(step_number=2, tool_used="architecture", status=StepStatus.COMPLETED)
        remaining = {3}
        ready = executor._get_ready_steps(remaining, steps, completed)
        assert len(ready) == 1
        assert ready[0].step_number == 3
    
    def test_diamond_dependencies(self):
        """
        Diamond pattern:
             1
            / \
           2   3
            \ /
             4
        """
        from src.agents.executor import ExecutorAgent
        
        mock_researcher = MagicMock()
        mock_researcher.as_tool.return_value = MagicMock()
        mock_architect = MagicMock()
        mock_architect.as_tool.return_value = MagicMock()
        mock_ghcp = MagicMock()
        mock_ghcp.as_tool.return_value = MagicMock()
        
        with patch('src.agents.executor.create_azure_chat_client'):
            executor = ExecutorAgent(mock_researcher, mock_architect, mock_ghcp)
        
        steps = {
            1: PlanStep(step_number=1, tool=ToolName.RESEARCH, query="q1", expected_output="o1", depends_on=[]),
            2: PlanStep(step_number=2, tool=ToolName.ARCHITECTURE, query="q2", expected_output="o2", depends_on=[1]),
            3: PlanStep(step_number=3, tool=ToolName.CODE, query="q3", expected_output="o3", depends_on=[1]),
            4: PlanStep(step_number=4, tool=ToolName.RESEARCH, query="q4", expected_output="o4", depends_on=[2, 3]),
        }
        
        # Wave 1: Only step 1 is ready
        remaining = {1, 2, 3, 4}
        completed = {}
        ready = executor._get_ready_steps(remaining, steps, completed)
        assert len(ready) == 1
        assert ready[0].step_number == 1
        
        # Wave 2: After step 1, steps 2 and 3 are ready (parallel!)
        completed[1] = StepResult(step_number=1, tool_used="research", status=StepStatus.COMPLETED)
        remaining = {2, 3, 4}
        ready = executor._get_ready_steps(remaining, steps, completed)
        assert len(ready) == 2
        ready_nums = {s.step_number for s in ready}
        assert ready_nums == {2, 3}
        
        # Wave 3: After 2 and 3, step 4 is ready
        completed[2] = StepResult(step_number=2, tool_used="architecture", status=StepStatus.COMPLETED)
        completed[3] = StepResult(step_number=3, tool_used="code", status=StepStatus.COMPLETED)
        remaining = {4}
        ready = executor._get_ready_steps(remaining, steps, completed)
        assert len(ready) == 1
        assert ready[0].step_number == 4
    
    def test_failed_dependency_blocks_downstream(self):
        """If a dependency fails, downstream steps should not be ready."""
        from src.agents.executor import ExecutorAgent
        
        mock_researcher = MagicMock()
        mock_researcher.as_tool.return_value = MagicMock()
        mock_architect = MagicMock()
        mock_architect.as_tool.return_value = MagicMock()
        mock_ghcp = MagicMock()
        mock_ghcp.as_tool.return_value = MagicMock()
        
        with patch('src.agents.executor.create_azure_chat_client'):
            executor = ExecutorAgent(mock_researcher, mock_architect, mock_ghcp)
        
        steps = {
            1: PlanStep(step_number=1, tool=ToolName.RESEARCH, query="q1", expected_output="o1", depends_on=[]),
            2: PlanStep(step_number=2, tool=ToolName.ARCHITECTURE, query="q2", expected_output="o2", depends_on=[1]),
        }
        
        # Step 1 failed
        completed = {
            1: StepResult(step_number=1, tool_used="research", status=StepStatus.FAILED, error="test error")
        }
        remaining = {2}
        
        ready = executor._get_ready_steps(remaining, steps, completed)
        assert len(ready) == 0, "Step 2 should not be ready since step 1 failed"


class TestParallelWaveIdentification:
    """Test that we correctly identify parallel execution waves."""
    
    def test_identify_waves(self):
        """Test wave identification for a complex dependency graph."""
        # This test documents expected behavior
        
        # Graph:
        # 1 (no deps) -> 2 (dep:1) -> 5 (dep:2,4)
        # 3 (no deps) -> 4 (dep:3)
        #
        # Expected waves:
        # Wave 1: [1, 3] - both independent
        # Wave 2: [2, 4] - 2 depends on 1, 4 depends on 3
        # Wave 3: [5] - depends on both 2 and 4
        
        from src.agents.executor import ExecutorAgent
        
        mock_researcher = MagicMock()
        mock_researcher.as_tool.return_value = MagicMock()
        mock_architect = MagicMock()
        mock_architect.as_tool.return_value = MagicMock()
        mock_ghcp = MagicMock()
        mock_ghcp.as_tool.return_value = MagicMock()
        
        with patch('src.agents.executor.create_azure_chat_client'):
            executor = ExecutorAgent(mock_researcher, mock_architect, mock_ghcp)
        
        steps = {
            1: PlanStep(step_number=1, tool=ToolName.RESEARCH, query="q1", expected_output="o1", depends_on=[]),
            2: PlanStep(step_number=2, tool=ToolName.ARCHITECTURE, query="q2", expected_output="o2", depends_on=[1]),
            3: PlanStep(step_number=3, tool=ToolName.RESEARCH, query="q3", expected_output="o3", depends_on=[]),
            4: PlanStep(step_number=4, tool=ToolName.CODE, query="q4", expected_output="o4", depends_on=[3]),
            5: PlanStep(step_number=5, tool=ToolName.CODE, query="q5", expected_output="o5", depends_on=[2, 4]),
        }
        
        # Simulate wave execution
        remaining = {1, 2, 3, 4, 5}
        completed = {}
        
        # Wave 1
        ready = executor._get_ready_steps(remaining, steps, completed)
        wave1 = {s.step_number for s in ready}
        assert wave1 == {1, 3}, f"Wave 1 should be {{1, 3}}, got {wave1}"
        
        # After wave 1 completes
        completed[1] = StepResult(step_number=1, tool_used="research", status=StepStatus.COMPLETED)
        completed[3] = StepResult(step_number=3, tool_used="research", status=StepStatus.COMPLETED)
        remaining = {2, 4, 5}
        
        # Wave 2
        ready = executor._get_ready_steps(remaining, steps, completed)
        wave2 = {s.step_number for s in ready}
        assert wave2 == {2, 4}, f"Wave 2 should be {{2, 4}}, got {wave2}"
        
        # After wave 2 completes
        completed[2] = StepResult(step_number=2, tool_used="architecture", status=StepStatus.COMPLETED)
        completed[4] = StepResult(step_number=4, tool_used="code", status=StepStatus.COMPLETED)
        remaining = {5}
        
        # Wave 3
        ready = executor._get_ready_steps(remaining, steps, completed)
        wave3 = {s.step_number for s in ready}
        assert wave3 == {5}, f"Wave 3 should be {{5}}, got {wave3}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
