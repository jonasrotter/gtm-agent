"""
Unit tests for hypothesis validation models.

Tests TestPlan, TestExecution, TestResult and related models per data-model.md.
These tests follow TDD - written first, must fail until implementation.
"""

import pytest
from datetime import datetime


class TestTestPlanStatus:
    """Tests for TestPlanStatus enum."""

    def test_draft_value(self) -> None:
        """Test DRAFT status value."""
        from src.models.hypothesis import TestPlanStatus

        assert TestPlanStatus.DRAFT.value == "draft"

    def test_approved_value(self) -> None:
        """Test APPROVED status value."""
        from src.models.hypothesis import TestPlanStatus

        assert TestPlanStatus.APPROVED.value == "approved"

    def test_rejected_value(self) -> None:
        """Test REJECTED status value."""
        from src.models.hypothesis import TestPlanStatus

        assert TestPlanStatus.REJECTED.value == "rejected"

    def test_executing_value(self) -> None:
        """Test EXECUTING status value."""
        from src.models.hypothesis import TestPlanStatus

        assert TestPlanStatus.EXECUTING.value == "executing"

    def test_completed_value(self) -> None:
        """Test COMPLETED status value."""
        from src.models.hypothesis import TestPlanStatus

        assert TestPlanStatus.COMPLETED.value == "completed"

    def test_failed_value(self) -> None:
        """Test FAILED status value."""
        from src.models.hypothesis import TestPlanStatus

        assert TestPlanStatus.FAILED.value == "failed"


class TestExecutionStatus:
    """Tests for ExecutionStatus enum."""

    def test_pending_value(self) -> None:
        """Test PENDING status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.PENDING.value == "pending"

    def test_deploying_value(self) -> None:
        """Test DEPLOYING status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.DEPLOYING.value == "deploying"

    def test_running_value(self) -> None:
        """Test RUNNING status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.RUNNING.value == "running"

    def test_collecting_value(self) -> None:
        """Test COLLECTING status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.COLLECTING.value == "collecting"

    def test_cleaning_up_value(self) -> None:
        """Test CLEANING_UP status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.CLEANING_UP.value == "cleaning_up"

    def test_completed_value(self) -> None:
        """Test COMPLETED status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.COMPLETED.value == "completed"

    def test_failed_value(self) -> None:
        """Test FAILED status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.FAILED.value == "failed"

    def test_cancelled_value(self) -> None:
        """Test CANCELLED status value."""
        from src.models.hypothesis import ExecutionStatus

        assert ExecutionStatus.CANCELLED.value == "cancelled"


class TestVerdict:
    """Tests for Verdict enum."""

    def test_confirmed_value(self) -> None:
        """Test CONFIRMED verdict value."""
        from src.models.hypothesis import Verdict

        assert Verdict.CONFIRMED.value == "confirmed"

    def test_refuted_value(self) -> None:
        """Test REFUTED verdict value."""
        from src.models.hypothesis import Verdict

        assert Verdict.REFUTED.value == "refuted"

    def test_inconclusive_value(self) -> None:
        """Test INCONCLUSIVE verdict value."""
        from src.models.hypothesis import Verdict

        assert Verdict.INCONCLUSIVE.value == "inconclusive"

    def test_partial_value(self) -> None:
        """Test PARTIAL verdict value."""
        from src.models.hypothesis import Verdict

        assert Verdict.PARTIAL.value == "partial"


class TestAzureResource:
    """Tests for AzureResource model."""

    def test_create_minimal_resource(self) -> None:
        """Test creating AzureResource with required fields."""
        from src.models.hypothesis import AzureResource

        resource = AzureResource(
            resource_type="Microsoft.Web/sites",
            name="test-webapp",
            configuration={"location": "eastus"},
            estimated_cost_per_hour=0.05,
        )

        assert resource.resource_type == "Microsoft.Web/sites"
        assert resource.name == "test-webapp"
        assert resource.configuration == {"location": "eastus"}
        assert resource.estimated_cost_per_hour == 0.05
        assert resource.sku is None

    def test_create_full_resource(self) -> None:
        """Test creating AzureResource with all fields."""
        from src.models.hypothesis import AzureResource

        resource = AzureResource(
            resource_type="Microsoft.Storage/storageAccounts",
            name="teststorage123",
            sku="Standard_LRS",
            configuration={"location": "westus2", "kind": "StorageV2"},
            estimated_cost_per_hour=0.02,
        )

        assert resource.resource_type == "Microsoft.Storage/storageAccounts"
        assert resource.name == "teststorage123"
        assert resource.sku == "Standard_LRS"
        assert resource.configuration["kind"] == "StorageV2"
        assert resource.estimated_cost_per_hour == 0.02


class TestMetric:
    """Tests for Metric model."""

    def test_create_metric(self) -> None:
        """Test creating Metric with all fields."""
        from src.models.hypothesis import Metric

        metric = Metric(
            name="response_time",
            description="Average HTTP response time",
            unit="milliseconds",
            collection_method="az monitor metrics list",
        )

        assert metric.name == "response_time"
        assert metric.description == "Average HTTP response time"
        assert metric.unit == "milliseconds"
        assert metric.collection_method == "az monitor metrics list"

    def test_metric_requires_all_fields(self) -> None:
        """Test that Metric requires all fields."""
        from pydantic import ValidationError

        from src.models.hypothesis import Metric

        with pytest.raises(ValidationError):
            Metric(name="test")  # type: ignore[call-arg]


class TestMetricValue:
    """Tests for MetricValue model."""

    def test_create_metric_value(self) -> None:
        """Test creating MetricValue."""
        from src.models.hypothesis import MetricValue

        metric_value = MetricValue(
            metric_name="response_time",
            value=125.5,
            unit="milliseconds",
            timestamp=datetime.now(),
        )

        assert metric_value.metric_name == "response_time"
        assert metric_value.value == 125.5
        assert metric_value.unit == "milliseconds"
        assert metric_value.timestamp is not None


class TestExecutionLog:
    """Tests for ExecutionLog model."""

    def test_create_execution_log(self) -> None:
        """Test creating ExecutionLog."""
        from src.models.hypothesis import ExecutionLog

        log = ExecutionLog(
            timestamp=datetime.now(),
            level="INFO",
            message="Deploying resources",
            details={"resource_group": "test-rg"},
        )

        assert log.level == "INFO"
        assert log.message == "Deploying resources"
        assert log.details["resource_group"] == "test-rg"

    def test_create_log_without_details(self) -> None:
        """Test creating ExecutionLog without optional details."""
        from src.models.hypothesis import ExecutionLog

        log = ExecutionLog(
            timestamp=datetime.now(),
            level="WARNING",
            message="Resource deployment slow",
        )

        assert log.level == "WARNING"
        assert log.details is None


class TestTestPlan:
    """Tests for TestPlan model."""

    def test_create_minimal_test_plan(self) -> None:
        """Test creating TestPlan with required fields."""
        from src.models.hypothesis import (
            AzureResource,
            Metric,
            TestPlan,
            TestPlanStatus,
        )

        plan = TestPlan(
            hypothesis="Azure Functions can handle 1000 concurrent requests",
            methodology="Deploy function, load test with k6, measure response times",
            resources_required=[
                AzureResource(
                    resource_type="Microsoft.Web/sites",
                    name="test-func",
                    configuration={"location": "eastus"},
                    estimated_cost_per_hour=0.05,
                )
            ],
            metrics_to_collect=[
                Metric(
                    name="requests_per_second",
                    description="RPS handled",
                    unit="requests/s",
                    collection_method="az monitor metrics",
                )
            ],
            success_criteria="95% of requests complete under 200ms",
            estimated_cost_usd=5.0,
            estimated_duration_minutes=15,
            cleanup_plan="Delete resource group test-rg",
            status=TestPlanStatus.DRAFT,
        )

        assert "Azure Functions" in plan.hypothesis
        assert len(plan.resources_required) == 1
        assert len(plan.metrics_to_collect) == 1
        assert plan.status == TestPlanStatus.DRAFT

    def test_test_plan_has_auto_id(self) -> None:
        """Test that TestPlan auto-generates an ID."""
        from src.models.hypothesis import (
            AzureResource,
            Metric,
            TestPlan,
            TestPlanStatus,
        )

        plan = TestPlan(
            hypothesis="Test hypothesis",
            methodology="Test method",
            resources_required=[
                AzureResource(
                    resource_type="Microsoft.Web/sites",
                    name="test",
                    configuration={},
                    estimated_cost_per_hour=0.01,
                )
            ],
            metrics_to_collect=[
                Metric(
                    name="test",
                    description="test",
                    unit="ms",
                    collection_method="az monitor",
                )
            ],
            success_criteria="Test passes",
            estimated_cost_usd=1.0,
            estimated_duration_minutes=5,
            cleanup_plan="Delete all",
            status=TestPlanStatus.DRAFT,
        )

        assert plan.id is not None
        assert len(plan.id) > 0

    def test_test_plan_has_created_at(self) -> None:
        """Test that TestPlan has auto-generated created_at."""
        from src.models.hypothesis import (
            AzureResource,
            Metric,
            TestPlan,
            TestPlanStatus,
        )

        plan = TestPlan(
            hypothesis="Test hypothesis",
            methodology="Test method",
            resources_required=[
                AzureResource(
                    resource_type="Microsoft.Web/sites",
                    name="test",
                    configuration={},
                    estimated_cost_per_hour=0.01,
                )
            ],
            metrics_to_collect=[
                Metric(
                    name="test",
                    description="test",
                    unit="ms",
                    collection_method="az monitor",
                )
            ],
            success_criteria="Test passes",
            estimated_cost_usd=1.0,
            estimated_duration_minutes=5,
            cleanup_plan="Delete all",
            status=TestPlanStatus.DRAFT,
        )

        assert plan.created_at is not None

    def test_test_plan_cost_must_be_positive(self) -> None:
        """Test that estimated cost must be positive."""
        from pydantic import ValidationError

        from src.models.hypothesis import (
            AzureResource,
            Metric,
            TestPlan,
            TestPlanStatus,
        )

        with pytest.raises(ValidationError):
            TestPlan(
                hypothesis="Test",
                methodology="Test",
                resources_required=[
                    AzureResource(
                        resource_type="Microsoft.Web/sites",
                        name="test",
                        configuration={},
                        estimated_cost_per_hour=0.01,
                    )
                ],
                metrics_to_collect=[
                    Metric(
                        name="test",
                        description="test",
                        unit="ms",
                        collection_method="az",
                    )
                ],
                success_criteria="Test passes",
                estimated_cost_usd=-5.0,  # Invalid: negative cost
                estimated_duration_minutes=5,
                cleanup_plan="Delete",
                status=TestPlanStatus.DRAFT,
            )


class TestTestPlanRequest:
    """Tests for TestPlanRequest model."""

    def test_create_minimal_request(self) -> None:
        """Test creating TestPlanRequest with minimal fields."""
        from src.models.hypothesis import TestPlanRequest

        request = TestPlanRequest(
            hypothesis="Azure Cosmos DB can handle 10000 RU/s workload",
        )

        assert "Cosmos DB" in request.hypothesis

    def test_create_request_with_constraints(self) -> None:
        """Test creating TestPlanRequest with constraints."""
        from src.models.hypothesis import TestConstraints, TestPlanRequest

        request = TestPlanRequest(
            hypothesis="Test hypothesis",
            constraints=TestConstraints(
                max_cost_usd=20.0,
                max_duration_minutes=60,
                allowed_regions=["eastus", "westus2"],
            ),
        )

        assert request.constraints is not None
        assert request.constraints.max_cost_usd == 20.0
        assert request.constraints.max_duration_minutes == 60
        assert "eastus" in request.constraints.allowed_regions

    def test_request_hypothesis_min_length(self) -> None:
        """Test that hypothesis must meet minimum length."""
        from pydantic import ValidationError

        from src.models.hypothesis import TestPlanRequest

        with pytest.raises(ValidationError):
            TestPlanRequest(hypothesis="Too short")  # Less than 10 chars


class TestTestExecution:
    """Tests for TestExecution model."""

    def test_create_test_execution(self) -> None:
        """Test creating TestExecution."""
        from src.models.hypothesis import ExecutionStatus, TestExecution

        execution = TestExecution(
            test_plan_id="plan-123",
            status=ExecutionStatus.PENDING,
        )

        assert execution.test_plan_id == "plan-123"
        assert execution.status == ExecutionStatus.PENDING
        assert execution.deployed_resources == []
        assert execution.metrics_collected == []
        assert execution.logs == []

    def test_execution_has_auto_id(self) -> None:
        """Test that TestExecution auto-generates an ID."""
        from src.models.hypothesis import ExecutionStatus, TestExecution

        execution = TestExecution(
            test_plan_id="plan-123",
            status=ExecutionStatus.PENDING,
        )

        assert execution.id is not None

    def test_execution_with_full_data(self) -> None:
        """Test TestExecution with all fields populated."""
        from src.models.hypothesis import (
            ExecutionLog,
            ExecutionStatus,
            MetricValue,
            TestExecution,
        )

        now = datetime.now()
        execution = TestExecution(
            test_plan_id="plan-123",
            status=ExecutionStatus.COMPLETED,
            started_at=now,
            completed_at=now,
            deployed_resources=["/subscriptions/abc/resourceGroups/test-rg"],
            metrics_collected=[
                MetricValue(
                    metric_name="latency",
                    value=150.0,
                    unit="ms",
                    timestamp=now,
                )
            ],
            logs=[
                ExecutionLog(
                    timestamp=now,
                    level="INFO",
                    message="Completed",
                )
            ],
        )

        assert execution.status == ExecutionStatus.COMPLETED
        assert len(execution.deployed_resources) == 1
        assert len(execution.metrics_collected) == 1
        assert len(execution.logs) == 1


class TestTestResult:
    """Tests for TestResult model."""

    def test_create_test_result(self) -> None:
        """Test creating TestResult."""
        from src.models.hypothesis import TestResult, Verdict

        result = TestResult(
            execution_id="exec-123",
            hypothesis="Azure Functions can scale to 1000 concurrent",
            verdict=Verdict.CONFIRMED,
            summary="Test confirmed the hypothesis with 99.5% success rate",
            raw_data={"requests": 1000, "success": 995, "failed": 5},
            confidence_level=0.95,
            cleanup_confirmed=True,
            actual_cost_usd=4.50,
        )

        assert result.execution_id == "exec-123"
        assert result.verdict == Verdict.CONFIRMED
        assert result.confidence_level == 0.95
        assert result.cleanup_confirmed is True
        assert result.actual_cost_usd == 4.50

    def test_result_has_auto_id(self) -> None:
        """Test that TestResult auto-generates an ID."""
        from src.models.hypothesis import TestResult, Verdict

        result = TestResult(
            execution_id="exec-123",
            hypothesis="Test",
            verdict=Verdict.INCONCLUSIVE,
            summary="Could not determine",
            raw_data={},
            confidence_level=0.5,
            cleanup_confirmed=True,
            actual_cost_usd=1.0,
        )

        assert result.id is not None

    def test_result_confidence_range_validation(self) -> None:
        """Test that confidence_level must be between 0 and 1."""
        from pydantic import ValidationError

        from src.models.hypothesis import TestResult, Verdict

        with pytest.raises(ValidationError):
            TestResult(
                execution_id="exec-123",
                hypothesis="Test",
                verdict=Verdict.CONFIRMED,
                summary="Test",
                raw_data={},
                confidence_level=1.5,  # Invalid: > 1
                cleanup_confirmed=True,
                actual_cost_usd=1.0,
            )

    def test_result_with_statistical_summary(self) -> None:
        """Test TestResult with statistical summary."""
        from src.models.hypothesis import TestResult, Verdict

        result = TestResult(
            execution_id="exec-123",
            hypothesis="Test",
            verdict=Verdict.CONFIRMED,
            summary="Test passed",
            raw_data={"values": [1, 2, 3, 4, 5]},
            statistical_summary={
                "mean": 3.0,
                "median": 3.0,
                "std_dev": 1.58,
                "p95": 4.8,
            },
            confidence_level=0.99,
            cleanup_confirmed=True,
            actual_cost_usd=2.50,
        )

        assert result.statistical_summary is not None
        assert result.statistical_summary["mean"] == 3.0


class TestExecuteTestRequest:
    """Tests for ExecuteTestRequest model."""

    def test_create_execute_request(self) -> None:
        """Test creating ExecuteTestRequest."""
        from src.models.hypothesis import ExecuteTestRequest

        request = ExecuteTestRequest(
            subscription_id="12345678-1234-1234-1234-123456789012",
        )

        assert request.subscription_id == "12345678-1234-1234-1234-123456789012"
        assert request.resource_group is None

    def test_create_execute_request_with_resource_group(self) -> None:
        """Test creating ExecuteTestRequest with resource group."""
        from src.models.hypothesis import ExecuteTestRequest

        request = ExecuteTestRequest(
            subscription_id="12345678-1234-1234-1234-123456789012",
            resource_group="test-hypothesis-rg",
        )

        assert request.subscription_id == "12345678-1234-1234-1234-123456789012"
        assert request.resource_group == "test-hypothesis-rg"
