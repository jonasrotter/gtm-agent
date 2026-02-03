"""
Agent response models.

Data structures for agent responses, execution plans, and verification results.
Includes Pydantic models for structured LLM output in the Plan-Execute-Verify pattern.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# =============================================================================
# Enums
# =============================================================================

class ToolName(str, Enum):
    """Available tools for execution planning."""
    RESEARCH = "research"
    ARCHITECTURE = "architecture"
    CODE = "code"


class StepStatus(str, Enum):
    """Execution status for a plan step."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class VerificationDecision(str, Enum):
    """Verifier's decision on the execution result."""
    ACCEPT = "accept"
    RETRY = "retry"
    ESCALATE = "escalate"


# =============================================================================
# Planning Models (Pydantic for structured LLM output)
# =============================================================================

class PlanStep(BaseModel):
    """
    A single step in the execution plan.
    
    Used by the Planner agent to break down user queries into discrete actions.
    """
    step_number: int = Field(description="Sequential step number starting from 1")
    tool: ToolName = Field(description="Which tool/sub-agent to invoke")
    query: str = Field(description="The specific query or instruction for this step")
    expected_output: str = Field(description="Brief description of what this step should produce")
    depends_on: list[int] = Field(
        default_factory=list,
        description="List of step numbers this step depends on (empty if independent)"
    )


class ExecutionPlan(BaseModel):
    """
    Complete execution plan produced by the Planner agent.
    
    Contains ordered steps with dependencies and metadata.
    """
    summary: str = Field(description="Brief summary of what this plan will accomplish")
    steps: list[PlanStep] = Field(description="Ordered list of execution steps")
    estimated_complexity: str = Field(
        description="Complexity estimate: 'simple' (1-2 steps), 'moderate' (3-4 steps), 'complex' (5+ steps)"
    )
    rationale: str = Field(description="Explanation of why this plan structure was chosen")


# =============================================================================
# Execution Models
# =============================================================================

@dataclass
class StepResult:
    """
    Result of executing a single plan step.
    
    Attributes:
        step_number: The step that was executed.
        tool_used: Which tool/sub-agent was invoked.
        status: Execution status (completed, failed, etc.).
        output: The output content from the tool.
        error: Error message if status is 'failed'.
        duration_ms: Execution time in milliseconds.
    """
    step_number: int
    tool_used: str
    status: StepStatus
    output: str = ""
    error: str | None = None
    duration_ms: int = 0


@dataclass
class ExecutionResult:
    """
    Aggregated result from executing all plan steps.
    
    Attributes:
        plan_summary: The original plan summary.
        step_results: Results for each executed step.
        final_output: Consolidated output from all steps.
        agents_used: List of sub-agents that were invoked.
        total_duration_ms: Total execution time.
        success: Whether all required steps completed successfully.
    """
    plan_summary: str
    step_results: list[StepResult] = field(default_factory=list)
    final_output: str = ""
    agents_used: list[str] = field(default_factory=list)
    total_duration_ms: int = 0
    success: bool = True


# =============================================================================
# Verification Models (Pydantic for structured LLM output)
# =============================================================================

class VerificationScore(BaseModel):
    """
    Multi-dimensional quality score for verification.
    
    Each dimension is scored 0.0 to 1.0.
    """
    correctness: float = Field(
        ge=0.0, le=1.0,
        description="Factual accuracy of the response (0.0-1.0)"
    )
    completeness: float = Field(
        ge=0.0, le=1.0,
        description="Whether all aspects of the query were addressed (0.0-1.0)"
    )
    consistency: float = Field(
        ge=0.0, le=1.0,
        description="Internal coherence without contradictions (0.0-1.0)"
    )
    overall: float = Field(
        ge=0.0, le=1.0,
        description="Weighted overall score: 0.4*correctness + 0.35*completeness + 0.25*consistency"
    )


class VerificationIssue(BaseModel):
    """A specific issue identified during verification."""
    category: str = Field(description="Issue category: 'factual', 'missing', 'inconsistent', 'unclear'")
    description: str = Field(description="Detailed description of the issue")
    severity: str = Field(description="Severity level: 'critical', 'major', 'minor'")
    suggestion: str = Field(description="Suggested fix or improvement")


class VerificationResult(BaseModel):
    """
    Complete verification result produced by the Verifier agent.
    
    Includes scoring, identified issues, and a decision.
    """
    score: VerificationScore = Field(description="Multi-dimensional quality score")
    decision: VerificationDecision = Field(
        description="Decision: 'accept' (score >= 0.8), 'retry' (can improve), 'escalate' (needs human)"
    )
    issues: list[VerificationIssue] = Field(
        default_factory=list,
        description="List of identified issues (empty if none)"
    )
    feedback_for_replanning: str = Field(
        default="",
        description="Specific feedback to improve the plan on retry (empty if accepted)"
    )
    summary: str = Field(description="Brief summary of verification findings")


# =============================================================================
# Agent Response Models
# =============================================================================

@dataclass
class ExecutionStepDetail:
    """
    Details about a single executed step for API response.
    
    Attributes:
        step_number: Sequential step number.
        tool: The tool/agent used (research, architecture, code).
        query: The query or instruction for this step.
        status: Execution status (completed, failed, skipped).
        output_preview: First 500 chars of the step output.
    """
    step_number: int
    tool: str
    query: str
    status: str
    output_preview: str = ""


@dataclass
class VerificationScoreDetail:
    """
    Detailed verification scores for API response.
    
    Attributes:
        overall: Weighted overall score (0.0-1.0).
        correctness: Factual accuracy score (0.0-1.0).
        completeness: Coverage score (0.0-1.0).
        consistency: Coherence score (0.0-1.0).
    """
    overall: float
    correctness: float
    completeness: float
    consistency: float


@dataclass
class AgentResponse:
    """
    Response from OrchestratorAgent with tracking and verification metadata.
    
    Attributes:
        content: The text response from the agent.
        agent_used: The sub-agent(s) that processed the query.
            Values: "researcher", "architect", "ghcp_coding", or comma-separated list.
        session_id: The session ID for multi-turn conversation continuity.
        turn_count: The number of turns in this conversation session.
        verification_score: Overall quality score from verification (0.0-1.0).
        iterations_used: Number of Plan-Execute-Verify cycles used.
        requires_human_review: True if verification failed after max iterations.
        plan_summary: Brief summary of the execution plan used.
        execution_steps: Details of each executed step (tool, query, status).
        score_details: Detailed verification scores by dimension.
        plan_rationale: Explanation of why the plan was structured this way.
        query_category: Classification of the query (factual, howto, architecture, code, complex).
    """
    content: str
    agent_used: str | None = None
    session_id: str | None = None
    turn_count: int = 1
    verification_score: float | None = None
    iterations_used: int = 1
    requires_human_review: bool = False
    plan_summary: str | None = None
    execution_steps: list[ExecutionStepDetail] = field(default_factory=list)
    score_details: VerificationScoreDetail | None = None
    plan_rationale: str | None = None
    query_category: str | None = None


@dataclass 
class HumanEscalationRequest:
    """
    Request for human review when verification fails.
    
    Attributes:
        query: The original user query.
        partial_result: The best result achieved before escalation.
        verification_issues: Issues identified by the verifier.
        iterations_attempted: Number of PEV cycles attempted.
        last_score: The verification score from the final iteration.
    """
    query: str
    partial_result: str
    verification_issues: list[dict[str, Any]] = field(default_factory=list)
    iterations_attempted: int = 0
    last_score: float = 0.0
