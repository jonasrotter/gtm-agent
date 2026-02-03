"""
Tool Evaluation Framework for GTM-Agent.

This module provides a comprehensive evaluation framework to test and improve
tool usage in the agentic system. Inspired by Anthropic's tool evaluation cookbook.

Key Components:
- EvaluationRunner: Main orchestrator for running evaluation tasks
- EvaluationMiddleware: agent_framework middleware for tool call tracking
- TaskDefinition: Pydantic model for task specifications
- EvaluationResult: Pydantic model for evaluation results
- Scorers: Functions to calculate evaluation metrics

Usage:
    from tests.evaluation import EvaluationRunner
    
    runner = EvaluationRunner()
    report = await runner.run_evaluation("tests/evaluation/evaluation.xml")
    print(report)
"""

from tests.evaluation.models import (
    TaskDefinition,
    EvaluationResult,
    ToolInvocation,
    EvaluationConfig,
    EvaluationReport,
)
from tests.evaluation.middleware import EvaluationMiddleware
from tests.evaluation.evaluation import EvaluationRunner
from tests.evaluation.scorers import (
    score_routing,
    score_tool_selection,
    score_keywords,
    score_citations,
    score_code_quality,
)

__all__ = [
    "TaskDefinition",
    "EvaluationResult",
    "ToolInvocation",
    "EvaluationConfig",
    "EvaluationReport",
    "EvaluationMiddleware",
    "EvaluationRunner",
    "score_routing",
    "score_tool_selection",
    "score_keywords",
    "score_citations",
    "score_code_quality",
]
