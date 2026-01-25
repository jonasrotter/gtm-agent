"""
Hypothesis validation models for Solution Engineering Agent.

Models for test plans, executions, and results per data-model.md.
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class TestPlanStatus(str, Enum):
    """Status of a test plan."""

    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionStatus(str, Enum):
    """Status of a test execution."""

    PENDING = "pending"
    DEPLOYING = "deploying"
    RUNNING = "running"
    COLLECTING = "collecting"
    CLEANING_UP = "cleaning_up"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Verdict(str, Enum):
    """Verdict for hypothesis validation result."""

    CONFIRMED = "confirmed"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"
    PARTIAL = "partial"


class AzureResource(BaseModel):
    """An Azure resource to be deployed for testing."""

    resource_type: str = Field(..., description="Azure resource type (e.g., Microsoft.Web/sites)")
    name: str = Field(..., description="Resource name")
    sku: str | None = Field(default=None, description="SKU/tier")
    configuration: dict[str, Any] = Field(..., description="Resource configuration")
    estimated_cost_per_hour: float = Field(..., ge=0, description="Hourly cost estimate")


class Metric(BaseModel):
    """A metric to be collected during testing."""

    name: str = Field(..., description="Metric name")
    description: str = Field(..., description="What this metric measures")
    unit: str = Field(..., description="Unit of measurement")
    collection_method: str = Field(..., description="How it will be collected")


class MetricValue(BaseModel):
    """A collected metric value."""

    metric_name: str = Field(..., description="Name of the metric")
    value: float = Field(..., description="Collected value")
    unit: str = Field(..., description="Unit of measurement")
    timestamp: datetime = Field(..., description="When the value was collected")


class ExecutionLog(BaseModel):
    """An execution log entry."""

    timestamp: datetime = Field(..., description="Log entry timestamp")
    level: str = Field(..., description="Log level (INFO, WARNING, ERROR)")
    message: str = Field(..., description="Log message")
    details: dict[str, Any] | None = Field(default=None, description="Additional details")


class TestConstraints(BaseModel):
    """Constraints for test plan generation."""

    max_cost_usd: float = Field(default=10.0, ge=0, description="Maximum allowed cost in USD")
    max_duration_minutes: int = Field(default=30, ge=1, description="Maximum test duration")
    allowed_regions: list[str] = Field(
        default_factory=lambda: ["eastus"],
        description="Allowed Azure regions",
    )


class TestPlanRequest(BaseModel):
    """Request to create a test plan."""

    hypothesis: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="The hypothesis to validate",
    )
    constraints: TestConstraints | None = Field(
        default=None,
        description="Constraints for test plan generation",
    )


class TestPlan(BaseModel):
    """A proposed approach for validating a hypothesis."""

    id: str = Field(default_factory=lambda: str(uuid4()), description="Test plan identifier")
    hypothesis: str = Field(..., description="The hypothesis being tested")
    methodology: str = Field(..., description="How the test will be conducted")
    resources_required: list[AzureResource] = Field(
        ...,
        description="Azure resources to deploy",
    )
    metrics_to_collect: list[Metric] = Field(
        ...,
        description="What will be measured",
    )
    success_criteria: str = Field(..., description="How to determine if hypothesis is confirmed")
    estimated_cost_usd: float = Field(..., ge=0, description="Estimated Azure cost")
    estimated_duration_minutes: int = Field(..., ge=1, description="How long the test will take")
    cleanup_plan: str = Field(..., description="How resources will be cleaned up")
    status: TestPlanStatus = Field(..., description="Current status of the plan")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When the plan was created",
    )

    @field_validator("estimated_cost_usd")
    @classmethod
    def cost_must_be_positive(cls, v: float) -> float:
        """Validate that cost is non-negative."""
        if v < 0:
            raise ValueError("Estimated cost must be non-negative")
        return v


class ExecuteTestRequest(BaseModel):
    """Request to execute a test plan."""

    subscription_id: str = Field(..., description="Azure subscription ID for resource deployment")
    resource_group: str | None = Field(
        default=None,
        description="Resource group name (created if not exists)",
    )


class TestExecution(BaseModel):
    """Record of a test being executed."""

    id: str = Field(default_factory=lambda: str(uuid4()), description="Execution identifier")
    test_plan_id: str = Field(..., description="Reference to test plan")
    status: ExecutionStatus = Field(..., description="Current execution status")
    started_at: datetime | None = Field(default=None, description="When execution started")
    completed_at: datetime | None = Field(default=None, description="When execution completed")
    deployed_resources: list[str] = Field(
        default_factory=list,
        description="Resource IDs deployed",
    )
    metrics_collected: list[MetricValue] = Field(
        default_factory=list,
        description="Collected metric values",
    )
    logs: list[ExecutionLog] = Field(
        default_factory=list,
        description="Execution log entries",
    )
    error: str | None = Field(default=None, description="Error message if failed")
    progress_percentage: int = Field(default=0, ge=0, le=100, description="Progress percentage")
    current_step: str | None = Field(default=None, description="Current execution step")


class TestResult(BaseModel):
    """Final result of hypothesis validation."""

    id: str = Field(default_factory=lambda: str(uuid4()), description="Result identifier")
    execution_id: str = Field(..., description="Reference to execution")
    hypothesis: str = Field(..., description="Original hypothesis")
    verdict: Verdict = Field(..., description="Whether hypothesis was confirmed")
    summary: str = Field(..., description="Human-readable summary")
    raw_data: dict[str, Any] = Field(..., description="Raw collected data")
    statistical_summary: dict[str, Any] | None = Field(
        default=None,
        description="Statistical analysis",
    )
    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the verdict (0.0-1.0)",
    )
    cleanup_confirmed: bool = Field(..., description="Whether resources were cleaned up")
    actual_cost_usd: float = Field(..., ge=0, description="Actual Azure cost incurred")

    @field_validator("confidence_level")
    @classmethod
    def confidence_in_range(cls, v: float) -> float:
        """Validate confidence level is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Confidence level must be between 0.0 and 1.0")
        return v
