"""
Unit tests for the Plan-Execute-Verify pattern agents.

Tests for:
- PlannerAgent: Plan creation and refinement
- ExecutorAgent: Plan execution with sub-agents
- VerifierAgent: Result verification and scoring
- OrchestratorAgent: Full PEV workflow orchestration
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import asdict

from src.agents.models import (
    PlanStep,
    ExecutionPlan,
    StepResult,
    ExecutionResult,
    VerificationScore,
    VerificationResult,
    VerificationDecision,
    VerificationIssue,
    AgentResponse,
    HumanEscalationRequest,
    ToolName,
    StepStatus,
)


# =============================================================================
# Model Tests
# =============================================================================

class TestPlanModels:
    """Tests for planning data models."""
    
    def test_plan_step_creation(self) -> None:
        """PlanStep can be created with required fields."""
        step = PlanStep(
            step_number=1,
            tool=ToolName.RESEARCH,
            query="What is Azure Functions?",
            expected_output="Description of Azure Functions",
        )
        
        assert step.step_number == 1
        assert step.tool == ToolName.RESEARCH
        assert step.query == "What is Azure Functions?"
        assert step.depends_on == []
    
    def test_plan_step_with_dependencies(self) -> None:
        """PlanStep can have dependencies on other steps."""
        step = PlanStep(
            step_number=2,
            tool=ToolName.CODE,
            query="Generate CLI command",
            expected_output="Azure CLI command",
            depends_on=[1],
        )
        
        assert step.depends_on == [1]
    
    def test_execution_plan_creation(self) -> None:
        """ExecutionPlan can be created with steps."""
        steps = [
            PlanStep(
                step_number=1,
                tool=ToolName.RESEARCH,
                query="Research Azure Functions",
                expected_output="Info about Functions",
            ),
            PlanStep(
                step_number=2,
                tool=ToolName.CODE,
                query="Generate deployment script",
                expected_output="CLI script",
                depends_on=[1],
            ),
        ]
        
        plan = ExecutionPlan(
            summary="Research and deploy Azure Functions",
            steps=steps,
            estimated_complexity="moderate",
            rationale="Need research before code generation",
        )
        
        assert len(plan.steps) == 2
        assert plan.estimated_complexity == "moderate"
    
    def test_execution_plan_serialization(self) -> None:
        """ExecutionPlan can be serialized to JSON."""
        plan = ExecutionPlan(
            summary="Test plan",
            steps=[
                PlanStep(
                    step_number=1,
                    tool=ToolName.ARCHITECTURE,
                    query="Best practices",
                    expected_output="WAF guidance",
                ),
            ],
            estimated_complexity="simple",
            rationale="Single step needed",
        )
        
        json_str = plan.model_dump_json()
        assert "Test plan" in json_str
        assert "architecture" in json_str


class TestExecutionModels:
    """Tests for execution data models."""
    
    def test_step_result_success(self) -> None:
        """StepResult captures successful execution."""
        result = StepResult(
            step_number=1,
            tool_used="research",
            status=StepStatus.COMPLETED,
            output="Azure Functions is a serverless compute service...",
            duration_ms=1500,
        )
        
        assert result.status == StepStatus.COMPLETED
        assert result.error is None
    
    def test_step_result_failure(self) -> None:
        """StepResult captures failed execution."""
        result = StepResult(
            step_number=2,
            tool_used="code",
            status=StepStatus.FAILED,
            error="Tool timeout",
            duration_ms=30000,
        )
        
        assert result.status == StepStatus.FAILED
        assert result.error == "Tool timeout"
    
    def test_execution_result_aggregation(self) -> None:
        """ExecutionResult aggregates step results."""
        steps = [
            StepResult(1, "research", StepStatus.COMPLETED, "Output 1", duration_ms=1000),
            StepResult(2, "code", StepStatus.COMPLETED, "Output 2", duration_ms=2000),
        ]
        
        result = ExecutionResult(
            plan_summary="Test plan",
            step_results=steps,
            final_output="Combined output",
            agents_used=["researcher", "ghcp_coding"],
            total_duration_ms=3000,
            success=True,
        )
        
        assert len(result.step_results) == 2
        assert result.success is True
        assert "researcher" in result.agents_used


class TestVerificationModels:
    """Tests for verification data models."""
    
    def test_verification_score_bounds(self) -> None:
        """VerificationScore enforces 0.0-1.0 bounds."""
        score = VerificationScore(
            correctness=0.9,
            completeness=0.85,
            consistency=0.95,
            overall=0.89,
        )
        
        assert 0.0 <= score.correctness <= 1.0
        assert 0.0 <= score.overall <= 1.0
    
    def test_verification_score_invalid_raises(self) -> None:
        """VerificationScore raises on invalid values."""
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            VerificationScore(
                correctness=1.5,  # Invalid: > 1.0
                completeness=0.8,
                consistency=0.8,
                overall=0.8,
            )
    
    def test_verification_issue_creation(self) -> None:
        """VerificationIssue captures problem details."""
        issue = VerificationIssue(
            category="factual",
            description="Incorrect service name mentioned",
            severity="major",
            suggestion="Replace 'Azure Function' with 'Azure Functions'",
        )
        
        assert issue.category == "factual"
        assert issue.severity == "major"
    
    def test_verification_result_accept(self) -> None:
        """VerificationResult with accept decision."""
        result = VerificationResult(
            score=VerificationScore(
                correctness=0.9,
                completeness=0.85,
                consistency=0.9,
                overall=0.88,
            ),
            decision=VerificationDecision.ACCEPT,
            issues=[],
            feedback_for_replanning="",
            summary="Response meets quality threshold",
        )
        
        assert result.decision == VerificationDecision.ACCEPT
        assert len(result.issues) == 0
    
    def test_verification_result_retry(self) -> None:
        """VerificationResult with retry decision."""
        result = VerificationResult(
            score=VerificationScore(
                correctness=0.7,
                completeness=0.6,
                consistency=0.8,
                overall=0.69,
            ),
            decision=VerificationDecision.RETRY,
            issues=[
                VerificationIssue(
                    category="missing",
                    description="Cost information not provided",
                    severity="major",
                    suggestion="Add cost estimates for recommended services",
                ),
            ],
            feedback_for_replanning="Add a step to research cost information",
            summary="Response incomplete, missing cost details",
        )
        
        assert result.decision == VerificationDecision.RETRY
        assert len(result.issues) == 1
        assert result.feedback_for_replanning != ""


class TestAgentResponseModel:
    """Tests for AgentResponse with PEV metadata."""
    
    def test_agent_response_basic(self) -> None:
        """AgentResponse can be created with basic fields."""
        response = AgentResponse(
            content="Here is the answer...",
            agent_used="researcher",
            session_id="test-session-123",
            turn_count=1,
        )
        
        assert response.content == "Here is the answer..."
        assert response.verification_score is None
    
    def test_agent_response_with_verification(self) -> None:
        """AgentResponse includes verification metadata."""
        response = AgentResponse(
            content="Verified answer...",
            agent_used="researcher, architect",
            session_id="test-session",
            turn_count=2,
            verification_score=0.85,
            iterations_used=2,
            requires_human_review=False,
            plan_summary="Research then architecture",
        )
        
        assert response.verification_score == 0.85
        assert response.iterations_used == 2
        assert response.requires_human_review is False
    
    def test_agent_response_human_escalation(self) -> None:
        """AgentResponse flags human review requirement."""
        response = AgentResponse(
            content="Partial answer...",
            verification_score=0.65,
            iterations_used=4,
            requires_human_review=True,
        )
        
        assert response.requires_human_review is True
        assert response.iterations_used == 4


class TestHumanEscalationRequest:
    """Tests for HumanEscalationRequest."""
    
    def test_escalation_request_creation(self) -> None:
        """HumanEscalationRequest captures escalation context."""
        request = HumanEscalationRequest(
            query="Complex multi-region architecture question",
            partial_result="Here is what I found so far...",
            verification_issues=[
                {"category": "factual", "description": "Uncertain about pricing"},
            ],
            iterations_attempted=4,
            last_score=0.72,
        )
        
        assert request.iterations_attempted == 4
        assert request.last_score == 0.72
        assert len(request.verification_issues) == 1


# =============================================================================
# Agent Tests (with mocked LLM)
# =============================================================================

class TestPlannerAgent:
    """Tests for the PlannerAgent."""
    
    def test_planner_module_imports(self) -> None:
        """PlannerAgent can be imported."""
        from src.agents.planner import PlannerAgent
        assert PlannerAgent is not None
    
    def test_planner_available_tools(self) -> None:
        """PlannerAgent knows available tools."""
        from src.agents.planner import PlannerAgent
        
        assert "research" in PlannerAgent.AVAILABLE_TOOLS
        assert "architecture" in PlannerAgent.AVAILABLE_TOOLS
        assert "code" in PlannerAgent.AVAILABLE_TOOLS
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_planner_initialization(self) -> None:
        """PlannerAgent initializes with expected attributes."""
        from src.agents.planner import PlannerAgent
        
        planner = PlannerAgent()
        
        assert hasattr(planner, 'agent')
        assert hasattr(planner, 'create_plan')
        assert hasattr(planner, 'refine_plan')
    
    @pytest.mark.asyncio
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    async def test_planner_create_plan_mocked(self) -> None:
        """PlannerAgent.create_plan returns ExecutionPlan with mocked LLM."""
        from src.agents.planner import PlannerAgent
        
        # Create mock plan
        mock_plan = ExecutionPlan(
            summary="Test plan",
            steps=[
                PlanStep(
                    step_number=1,
                    tool=ToolName.RESEARCH,
                    query="Test query",
                    expected_output="Test output",
                ),
            ],
            estimated_complexity="simple",
            rationale="Test rationale",
        )
        
        planner = PlannerAgent()
        
        # Mock the agent's run method
        mock_result = MagicMock()
        mock_result.value = mock_plan
        mock_result.text = mock_plan.model_dump_json()
        
        planner.agent.run = AsyncMock(return_value=mock_result)
        planner.agent.__aenter__ = AsyncMock(return_value=planner.agent)
        planner.agent.__aexit__ = AsyncMock(return_value=None)
        
        result = await planner.create_plan("What is Azure Functions?")
        
        assert isinstance(result, ExecutionPlan)
        assert result.summary == "Test plan"


class TestExecutorAgent:
    """Tests for the ExecutorAgent."""
    
    def test_executor_module_imports(self) -> None:
        """ExecutorAgent can be imported."""
        from src.agents.executor import ExecutorAgent
        assert ExecutorAgent is not None
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_executor_initialization_with_di(self) -> None:
        """ExecutorAgent receives sub-agents via dependency injection."""
        from src.agents.executor import ExecutorAgent
        from src.agents.researcher import ResearcherAgent
        from src.agents.architect import ArchitectAgent
        from src.agents.ghcp_coding_agent import GHCPCodingAgent
        
        researcher = ResearcherAgent()
        architect = ArchitectAgent()
        ghcp = GHCPCodingAgent()
        
        executor = ExecutorAgent(
            researcher=researcher,
            architect=architect,
            ghcp_coding=ghcp,
        )
        
        assert executor.researcher is researcher
        assert executor.architect is architect
        assert executor.ghcp_coding is ghcp
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_executor_tool_mapping(self) -> None:
        """ExecutorAgent maps tool names to agent names."""
        from src.agents.executor import ExecutorAgent
        from src.agents.researcher import ResearcherAgent
        from src.agents.architect import ArchitectAgent
        from src.agents.ghcp_coding_agent import GHCPCodingAgent
        
        executor = ExecutorAgent(
            researcher=ResearcherAgent(),
            architect=ArchitectAgent(),
            ghcp_coding=GHCPCodingAgent(),
        )
        
        assert executor._tool_to_agent["research"] == "researcher"
        assert executor._tool_to_agent["architecture"] == "architect"
        assert executor._tool_to_agent["code"] == "ghcp_coding"


class TestVerifierAgent:
    """Tests for the VerifierAgent."""
    
    def test_verifier_module_imports(self) -> None:
        """VerifierAgent can be imported."""
        from src.agents.verifier import VerifierAgent
        assert VerifierAgent is not None
    
    def test_verifier_acceptance_threshold(self) -> None:
        """VerifierAgent has expected threshold."""
        from src.agents.verifier import VerifierAgent
        
        assert VerifierAgent.ACCEPTANCE_THRESHOLD == 0.8
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_verifier_initialization_with_fact_check(self) -> None:
        """VerifierAgent can enable fact-checking."""
        from src.agents.verifier import VerifierAgent
        
        verifier = VerifierAgent(enable_fact_check=True)
        assert verifier._fact_check_enabled is True
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_verifier_initialization_without_fact_check(self) -> None:
        """VerifierAgent can disable fact-checking."""
        from src.agents.verifier import VerifierAgent
        
        verifier = VerifierAgent(enable_fact_check=False)
        assert verifier._fact_check_enabled is False


class TestOrchestratorAgent:
    """Tests for the OrchestratorAgent."""
    
    def test_orchestrator_module_imports(self) -> None:
        """OrchestratorAgent can be imported."""
        from src.agents.orchestrator import OrchestratorAgent, get_orchestrator_agent
        assert OrchestratorAgent is not None
        assert callable(get_orchestrator_agent)
    
    def test_orchestrator_configuration_constants(self) -> None:
        """OrchestratorAgent has expected configuration."""
        from src.agents.orchestrator import OrchestratorAgent
        
        assert OrchestratorAgent.DEFAULT_ACCEPTANCE_THRESHOLD == 0.8
        assert OrchestratorAgent.DEFAULT_MAX_ITERATIONS == 4
        assert OrchestratorAgent.MAX_SESSIONS == 1000
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_orchestrator_initialization(self) -> None:
        """OrchestratorAgent initializes all components."""
        from src.agents.orchestrator import OrchestratorAgent
        
        orchestrator = OrchestratorAgent()
        
        # Check sub-agents exist
        assert orchestrator.researcher is not None
        assert orchestrator.architect is not None
        assert orchestrator.ghcp_coding is not None
        
        # Check PEV agents exist
        assert orchestrator.planner is not None
        assert orchestrator.executor is not None
        assert orchestrator.verifier is not None
        
        # Check session management
        assert hasattr(orchestrator, '_sessions')
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_orchestrator_session_management(self) -> None:
        """OrchestratorAgent manages sessions correctly."""
        from src.agents.orchestrator import OrchestratorAgent
        
        orchestrator = OrchestratorAgent()
        
        # New session
        session_id, turn_count = orchestrator._get_or_create_session(None)
        assert session_id is not None
        assert turn_count == 1
        
        # Save session
        orchestrator._save_session(session_id, {"test": "context"}, turn_count)
        
        # Retrieve session
        session_id_2, turn_count_2 = orchestrator._get_or_create_session(session_id)
        assert session_id_2 == session_id
        assert turn_count_2 == 2
        
        # Clear session
        cleared = orchestrator.clear_session(session_id)
        assert cleared is True
        
        # Session no longer exists
        info = orchestrator.get_session_info(session_id)
        assert info is None
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_orchestrator_backwards_compatibility(self) -> None:
        """get_orchestrator_agent returns OrchestratorAgent."""
        from src.agents.orchestrator import (
            get_orchestrator_agent,
            OrchestratorAgent,
        )
        
        agent = get_orchestrator_agent()
        
        assert isinstance(agent, OrchestratorAgent)
    
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com',
        'AZURE_OPENAI_DEPLOYMENT': 'gpt-4o',
    })
    def test_orchestrator_escalation_request(self) -> None:
        """OrchestratorAgent creates escalation requests."""
        from src.agents.orchestrator import OrchestratorAgent
        
        orchestrator = OrchestratorAgent()
        
        result = ExecutionResult(
            plan_summary="Test plan",
            final_output="Partial result",
            success=True,
        )
        
        verification = VerificationResult(
            score=VerificationScore(
                correctness=0.6,
                completeness=0.5,
                consistency=0.7,
                overall=0.58,
            ),
            decision=VerificationDecision.ESCALATE,
            issues=[
                VerificationIssue(
                    category="factual",
                    description="Test issue",
                    severity="critical",
                    suggestion="Fix it",
                ),
            ],
            summary="Needs human review",
        )
        
        escalation = orchestrator.get_escalation_request(
            query="Test query",
            result=result,
            verification=verification,
            iterations=4,
        )
        
        assert isinstance(escalation, HumanEscalationRequest)
        assert escalation.query == "Test query"
        assert escalation.iterations_attempted == 4
        assert escalation.last_score == 0.58
