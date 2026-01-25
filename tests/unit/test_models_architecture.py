"""
Unit tests for architecture models.

TDD: These tests should FAIL initially until models are implemented.
"""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError


class TestWAFPillar:
    """Tests for WAFPillar enum."""

    def test_reliability_value(self) -> None:
        """WAFPillar has RELIABILITY value."""
        from src.models.architecture import WAFPillar

        assert WAFPillar.RELIABILITY == "reliability"

    def test_security_value(self) -> None:
        """WAFPillar has SECURITY value."""
        from src.models.architecture import WAFPillar

        assert WAFPillar.SECURITY == "security"

    def test_cost_optimization_value(self) -> None:
        """WAFPillar has COST_OPTIMIZATION value."""
        from src.models.architecture import WAFPillar

        assert WAFPillar.COST_OPTIMIZATION == "cost_optimization"

    def test_operational_excellence_value(self) -> None:
        """WAFPillar has OPERATIONAL_EXCELLENCE value."""
        from src.models.architecture import WAFPillar

        assert WAFPillar.OPERATIONAL_EXCELLENCE == "operational_excellence"

    def test_performance_efficiency_value(self) -> None:
        """WAFPillar has PERFORMANCE_EFFICIENCY value."""
        from src.models.architecture import WAFPillar

        assert WAFPillar.PERFORMANCE_EFFICIENCY == "performance_efficiency"


class TestSeverity:
    """Tests for Severity enum."""

    def test_critical_value(self) -> None:
        """Severity has CRITICAL value."""
        from src.models.architecture import Severity

        assert Severity.CRITICAL == "critical"

    def test_high_value(self) -> None:
        """Severity has HIGH value."""
        from src.models.architecture import Severity

        assert Severity.HIGH == "high"

    def test_medium_value(self) -> None:
        """Severity has MEDIUM value."""
        from src.models.architecture import Severity

        assert Severity.MEDIUM == "medium"

    def test_low_value(self) -> None:
        """Severity has LOW value."""
        from src.models.architecture import Severity

        assert Severity.LOW == "low"


class TestPriority:
    """Tests for Priority enum."""

    def test_p1_value(self) -> None:
        """Priority has P1 value."""
        from src.models.architecture import Priority

        assert Priority.P1 == "p1"

    def test_p2_value(self) -> None:
        """Priority has P2 value."""
        from src.models.architecture import Priority

        assert Priority.P2 == "p2"

    def test_p3_value(self) -> None:
        """Priority has P3 value."""
        from src.models.architecture import Priority

        assert Priority.P3 == "p3"

    def test_p4_value(self) -> None:
        """Priority has P4 value."""
        from src.models.architecture import Priority

        assert Priority.P4 == "p4"


class TestPattern:
    """Tests for Pattern model."""

    def test_create_minimal_pattern(self) -> None:
        """Create Pattern with required fields only."""
        from src.models.architecture import Pattern

        pattern = Pattern(
            name="Event Sourcing",
            description="Stores state changes as events",
        )

        assert pattern.name == "Event Sourcing"
        assert pattern.description == "Stores state changes as events"
        assert pattern.waf_pillar is None

    def test_create_full_pattern(self) -> None:
        """Create Pattern with all fields."""
        from src.models.architecture import Pattern, WAFPillar

        pattern = Pattern(
            name="Circuit Breaker",
            description="Prevents cascading failures",
            waf_pillar=WAFPillar.RELIABILITY,
        )

        assert pattern.name == "Circuit Breaker"
        assert pattern.waf_pillar == WAFPillar.RELIABILITY


class TestAntiPattern:
    """Tests for AntiPattern model."""

    def test_create_minimal_antipattern(self) -> None:
        """Create AntiPattern with required fields only."""
        from src.models.architecture import AntiPattern, Severity

        antipattern = AntiPattern(
            name="Single Point of Failure",
            severity=Severity.HIGH,
            description="No redundancy for critical component",
            impact="Complete outage if component fails",
        )

        assert antipattern.name == "Single Point of Failure"
        assert antipattern.severity == Severity.HIGH
        assert antipattern.location is None

    def test_create_full_antipattern(self) -> None:
        """Create AntiPattern with all fields."""
        from src.models.architecture import AntiPattern, Severity

        antipattern = AntiPattern(
            name="Chatty I/O",
            severity=Severity.MEDIUM,
            description="Too many small requests",
            impact="High latency and cost",
            location="Data access layer",
        )

        assert antipattern.location == "Data access layer"

    def test_severity_required(self) -> None:
        """Severity is required."""
        from src.models.architecture import AntiPattern

        with pytest.raises(ValidationError):
            AntiPattern(
                name="Test",
                description="Test",
                impact="Test",
            )


class TestRecommendation:
    """Tests for Recommendation model."""

    def test_create_minimal_recommendation(self) -> None:
        """Create Recommendation with required fields only."""
        from src.models.architecture import Priority, Recommendation

        rec = Recommendation(
            title="Add redundancy",
            description="Deploy across availability zones",
            rationale="Improves reliability",
            priority=Priority.P1,
        )

        assert rec.title == "Add redundancy"
        assert rec.priority == Priority.P1
        assert rec.waf_pillar is None

    def test_create_full_recommendation(self) -> None:
        """Create Recommendation with all fields."""
        from src.models.architecture import Priority, Recommendation, WAFPillar

        rec = Recommendation(
            title="Implement caching",
            description="Use Redis for session state",
            rationale="Reduces database load",
            priority=Priority.P2,
            waf_pillar=WAFPillar.PERFORMANCE_EFFICIENCY,
            related_anti_pattern="N+1 Queries",
        )

        assert rec.related_anti_pattern == "N+1 Queries"


class TestPillarScore:
    """Tests for PillarScore model."""

    def test_create_pillar_score(self) -> None:
        """Create PillarScore with valid values."""
        from src.models.architecture import PillarScore

        score = PillarScore(
            score=0.8,
            findings=["Good use of redundancy", "Could improve monitoring"],
        )

        assert score.score == 0.8
        assert len(score.findings) == 2

    def test_score_range_validation(self) -> None:
        """Score must be between 0.0 and 1.0."""
        from src.models.architecture import PillarScore

        with pytest.raises(ValidationError):
            PillarScore(score=1.5, findings=[])

        with pytest.raises(ValidationError):
            PillarScore(score=-0.1, findings=[])


class TestWAFAlignment:
    """Tests for WAFAlignment model."""

    def test_create_waf_alignment(self) -> None:
        """Create WAFAlignment with all pillars."""
        from src.models.architecture import PillarScore, WAFAlignment

        alignment = WAFAlignment(
            reliability=PillarScore(score=0.9, findings=["Highly available"]),
            security=PillarScore(score=0.7, findings=["Needs encryption"]),
            cost_optimization=PillarScore(score=0.6, findings=["Over-provisioned"]),
            operational_excellence=PillarScore(score=0.8, findings=["Good monitoring"]),
            performance_efficiency=PillarScore(score=0.75, findings=["Acceptable"]),
        )

        assert alignment.reliability.score == 0.9
        assert alignment.security.score == 0.7

    def test_all_pillars_required(self) -> None:
        """All five pillars are required."""
        from src.models.architecture import PillarScore, WAFAlignment

        with pytest.raises(ValidationError):
            WAFAlignment(
                reliability=PillarScore(score=0.9, findings=[]),
                # Missing other pillars
            )


class TestArchitectureReview:
    """Tests for ArchitectureReview model."""

    def test_create_architecture_review(self) -> None:
        """Create ArchitectureReview with all fields."""
        from src.models.architecture import (
            AntiPattern,
            ArchitectureReview,
            Pattern,
            PillarScore,
            Priority,
            Recommendation,
            Severity,
            WAFAlignment,
            WAFPillar,
        )

        review = ArchitectureReview(
            summary="Good overall design with some improvements needed",
            patterns_identified=[
                Pattern(name="Microservices", description="Good service isolation"),
            ],
            anti_patterns=[
                AntiPattern(
                    name="Shared Database",
                    severity=Severity.MEDIUM,
                    description="Services share database",
                    impact="Coupling between services",
                ),
            ],
            recommendations=[
                Recommendation(
                    title="Separate databases",
                    description="Each service owns its data",
                    rationale="Reduces coupling",
                    priority=Priority.P2,
                ),
            ],
            waf_alignment=WAFAlignment(
                reliability=PillarScore(score=0.8, findings=[]),
                security=PillarScore(score=0.7, findings=[]),
                cost_optimization=PillarScore(score=0.6, findings=[]),
                operational_excellence=PillarScore(score=0.8, findings=[]),
                performance_efficiency=PillarScore(score=0.75, findings=[]),
            ),
            overall_score=0.75,
        )

        assert review.overall_score == 0.75
        assert len(review.patterns_identified) == 1
        assert len(review.anti_patterns) == 1

    def test_id_auto_generated(self) -> None:
        """Review ID is auto-generated."""
        from src.models.architecture import (
            ArchitectureReview,
            PillarScore,
            WAFAlignment,
        )

        review = ArchitectureReview(
            summary="Test review",
            patterns_identified=[],
            anti_patterns=[],
            recommendations=[],
            waf_alignment=WAFAlignment(
                reliability=PillarScore(score=0.5, findings=[]),
                security=PillarScore(score=0.5, findings=[]),
                cost_optimization=PillarScore(score=0.5, findings=[]),
                operational_excellence=PillarScore(score=0.5, findings=[]),
                performance_efficiency=PillarScore(score=0.5, findings=[]),
            ),
            overall_score=0.5,
        )

        assert review.id is not None
        assert len(review.id) > 0

    def test_overall_score_range_validation(self) -> None:
        """Overall score must be between 0.0 and 1.0."""
        from src.models.architecture import (
            ArchitectureReview,
            PillarScore,
            WAFAlignment,
        )

        with pytest.raises(ValidationError):
            ArchitectureReview(
                summary="Test",
                patterns_identified=[],
                anti_patterns=[],
                recommendations=[],
                waf_alignment=WAFAlignment(
                    reliability=PillarScore(score=0.5, findings=[]),
                    security=PillarScore(score=0.5, findings=[]),
                    cost_optimization=PillarScore(score=0.5, findings=[]),
                    operational_excellence=PillarScore(score=0.5, findings=[]),
                    performance_efficiency=PillarScore(score=0.5, findings=[]),
                ),
                overall_score=1.5,  # Invalid
            )


class TestArchitectureRequest:
    """Tests for ArchitectureReviewRequest model."""

    def test_create_review_request(self) -> None:
        """Create ArchitectureReviewRequest with required fields."""
        from src.models.architecture import ArchitectureReviewRequest

        request = ArchitectureReviewRequest(
            description="Microservices architecture for e-commerce",
            context={"diagram_url": "https://example.com/arch.png"},
        )

        assert "Microservices" in request.description
        assert request.context is not None

    def test_description_required(self) -> None:
        """Description is required."""
        from src.models.architecture import ArchitectureReviewRequest

        with pytest.raises(ValidationError):
            ArchitectureReviewRequest()
