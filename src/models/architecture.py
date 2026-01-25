"""
Architecture models for Solution Engineering Agent.

Models for architecture review, patterns, anti-patterns, recommendations,
and Well-Architected Framework alignment.
"""

from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class WAFPillar(str, Enum):
    """Well-Architected Framework pillars."""

    RELIABILITY = "reliability"
    SECURITY = "security"
    COST_OPTIMIZATION = "cost_optimization"
    OPERATIONAL_EXCELLENCE = "operational_excellence"
    PERFORMANCE_EFFICIENCY = "performance_efficiency"


class Severity(str, Enum):
    """Severity levels for anti-patterns and issues."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Priority(str, Enum):
    """Priority levels for recommendations."""

    P1 = "p1"
    P2 = "p2"
    P3 = "p3"
    P4 = "p4"


class Pattern(BaseModel):
    """A design pattern identified in architecture."""

    name: str = Field(..., description="Name of the pattern")
    description: str = Field(..., description="Description of the pattern")
    waf_pillar: WAFPillar | None = Field(
        None, description="Primary WAF pillar this pattern aligns with"
    )


class AntiPattern(BaseModel):
    """An anti-pattern identified in architecture."""

    name: str = Field(..., description="Name of the anti-pattern")
    severity: Severity = Field(..., description="Severity level of the anti-pattern")
    description: str = Field(..., description="Description of the anti-pattern")
    impact: str = Field(..., description="Impact of the anti-pattern")
    location: str | None = Field(
        None, description="Location in the architecture where this was identified"
    )


class Recommendation(BaseModel):
    """A recommendation for improving architecture."""

    title: str = Field(..., description="Short title for the recommendation")
    description: str = Field(..., description="Detailed description of the recommendation")
    rationale: str = Field(..., description="Why this recommendation is important")
    priority: Priority = Field(..., description="Priority level of this recommendation")
    waf_pillar: WAFPillar | None = Field(
        None, description="WAF pillar this recommendation addresses"
    )
    related_anti_pattern: str | None = Field(
        None, description="Related anti-pattern this recommendation addresses"
    )


class PillarScore(BaseModel):
    """Score and findings for a single WAF pillar."""

    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Score for this pillar (0.0 to 1.0)",
    )
    findings: list[str] = Field(
        default_factory=list, description="Findings for this pillar"
    )


class WAFAlignment(BaseModel):
    """Well-Architected Framework alignment assessment."""

    reliability: PillarScore = Field(..., description="Reliability pillar assessment")
    security: PillarScore = Field(..., description="Security pillar assessment")
    cost_optimization: PillarScore = Field(
        ..., description="Cost Optimization pillar assessment"
    )
    operational_excellence: PillarScore = Field(
        ..., description="Operational Excellence pillar assessment"
    )
    performance_efficiency: PillarScore = Field(
        ..., description="Performance Efficiency pillar assessment"
    )


class ArchitectureReview(BaseModel):
    """Complete architecture review response."""

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for this review",
    )
    summary: str = Field(..., description="Executive summary of the architecture review")
    patterns_identified: list[Pattern] = Field(
        default_factory=list, description="Design patterns identified"
    )
    anti_patterns: list[AntiPattern] = Field(
        default_factory=list, description="Anti-patterns identified"
    )
    recommendations: list[Recommendation] = Field(
        default_factory=list, description="Recommendations for improvement"
    )
    waf_alignment: WAFAlignment = Field(
        ..., description="Well-Architected Framework alignment assessment"
    )
    overall_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall architecture score (0.0 to 1.0)",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the review was created",
    )


class ArchitectureReviewRequest(BaseModel):
    """Request to review an architecture."""

    description: str = Field(
        ..., min_length=1, description="Description of the architecture to review"
    )
    context: dict | None = Field(
        None, description="Additional context for the review"
    )


class BestPracticesRequest(BaseModel):
    """Request to get best practices."""

    query: str = Field(
        ..., min_length=1, description="Query to search for best practices"
    )
    waf_pillar: WAFPillar | None = Field(
        None, description="Filter by WAF pillar"
    )
