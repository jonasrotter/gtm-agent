"""
Pydantic models for the evaluation framework.

Defines data structures for:
- Task definitions (parsed from evaluation.xml)
- Evaluation results with metrics
- Tool invocation tracking
- Aggregated reports
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExpectedRouting(str, Enum):
    """Expected routing categories."""
    FACTUAL = "FACTUAL"
    HOWTO = "HOWTO"
    ARCHITECTURE = "ARCHITECTURE"
    CODE = "CODE"
    COMPLEX = "COMPLEX"


class TaskExpectations(BaseModel):
    """Expected outcomes for a task."""
    routing: ExpectedRouting | None = None
    tools: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    has_citations: bool = False
    has_waf_reference: bool = False
    has_code_block: bool = False
    code_patterns: list[str] = Field(default_factory=list)
    min_steps: int | None = None
    max_steps: int | None = None
    max_tool_calls: int | None = None
    max_duration_seconds: float | None = None


class TaskDefinition(BaseModel):
    """Definition of an evaluation task parsed from XML."""
    id: str
    category: str
    prompt: str
    expected: TaskExpectations
    description: str | None = None
    
    class Config:
        frozen = True


class ToolInvocation(BaseModel):
    """Record of a single tool invocation captured by middleware."""
    tool_name: str
    arguments: dict[str, Any]
    result: Any | None = None
    duration_seconds: float
    error: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TaskScores(BaseModel):
    """Individual scores for a task evaluation."""
    routing_score: float = Field(ge=0.0, le=1.0, default=0.0)
    tool_selection_score: float = Field(ge=0.0, le=1.0, default=0.0)
    keyword_coverage_score: float = Field(ge=0.0, le=1.0, default=0.0)
    citation_score: float = Field(ge=0.0, le=1.0, default=0.0)
    code_quality_score: float = Field(ge=0.0, le=1.0, default=0.0)
    performance_score: float = Field(ge=0.0, le=1.0, default=0.0)
    efficiency_score: float = Field(ge=0.0, le=1.0, default=0.0)
    
    @property
    def overall_score(self) -> float:
        """Calculate weighted overall score."""
        weights = {
            "routing_score": 0.20,
            "tool_selection_score": 0.20,
            "keyword_coverage_score": 0.15,
            "citation_score": 0.10,
            "code_quality_score": 0.15,
            "performance_score": 0.10,
            "efficiency_score": 0.10,
        }
        
        total = 0.0
        for field, weight in weights.items():
            total += getattr(self, field) * weight
        return round(total, 4)


class TokenUsage(BaseModel):
    """Token usage statistics."""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    
    def __add__(self, other: "TokenUsage") -> "TokenUsage":
        return TokenUsage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
        )


class EvaluationResult(BaseModel):
    """Result of evaluating a single task."""
    task: TaskDefinition
    
    # Actual outcomes
    actual_routing: str | None = None
    actual_tools: list[str] = Field(default_factory=list)
    response_text: str = ""
    response_preview: str = ""  # Truncated for display
    
    # Metrics
    duration_seconds: float = 0.0
    tool_invocations: list[ToolInvocation] = Field(default_factory=list)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    verification_score: float | None = None
    iterations_used: int = 0
    steps_executed: int = 0
    
    # Scores
    scores: TaskScores = Field(default_factory=TaskScores)
    
    # Feedback
    agent_feedback: str | None = None
    
    # Status
    success: bool = False
    error: str | None = None
    
    @property
    def passed(self) -> bool:
        """Check if task passed based on overall score threshold."""
        return self.success and self.scores.overall_score >= 0.7


class EvaluationConfig(BaseModel):
    """Configuration for evaluation run."""
    timeout_seconds: float = 300.0
    use_middleware: bool = True
    capture_feedback: bool = True
    mode: str = "api"  # "api", "direct", or "both"
    base_url: str = "http://localhost:8000"
    parallel_tasks: int = 1  # Number of tasks to run in parallel
    
    # Scoring thresholds
    routing_threshold: float = 0.9
    tool_selection_threshold: float = 0.85
    keyword_threshold: float = 0.75
    performance_threshold: float = 0.8


class ToolMetrics(BaseModel):
    """Aggregated metrics for a single tool."""
    tool_name: str
    call_count: int = 0
    total_duration_seconds: float = 0.0
    success_count: int = 0
    error_count: int = 0
    
    @property
    def avg_duration_seconds(self) -> float:
        if self.call_count == 0:
            return 0.0
        return self.total_duration_seconds / self.call_count
    
    @property
    def success_rate(self) -> float:
        if self.call_count == 0:
            return 0.0
        return self.success_count / self.call_count


class CategoryMetrics(BaseModel):
    """Aggregated metrics for a task category."""
    category: str
    task_count: int = 0
    passed_count: int = 0
    avg_score: float = 0.0
    avg_duration_seconds: float = 0.0
    avg_tool_calls: float = 0.0


class EvaluationReport(BaseModel):
    """Complete evaluation report."""
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    config: EvaluationConfig
    evaluation_file: str
    
    # Summary
    total_tasks: int = 0
    passed_tasks: int = 0
    failed_tasks: int = 0
    
    # Scores
    overall_accuracy: float = 0.0
    routing_accuracy: float = 0.0
    tool_selection_accuracy: float = 0.0
    avg_keyword_coverage: float = 0.0
    avg_performance_score: float = 0.0
    
    # Token usage
    total_token_usage: TokenUsage = Field(default_factory=TokenUsage)
    
    # Detailed metrics
    tool_metrics: list[ToolMetrics] = Field(default_factory=list)
    category_metrics: list[CategoryMetrics] = Field(default_factory=list)
    
    # Results
    results: list[EvaluationResult] = Field(default_factory=list)
    
    # Feedback summary
    common_issues: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.passed_tasks / self.total_tasks
