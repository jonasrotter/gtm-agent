"""
Agents package for specialist agent implementations.

Provides agent implementations using Microsoft Agent Framework:
- OrchestratorAgent: Plan-Execute-Verify workflow orchestrator (replaces SolutionEngineerAgent)
- QueryClassifier: Intelligent query routing for optimal processing path
- PlannerAgent: Creates structured execution plans
- ExecutorAgent: Executes plans using sub-agent tools
- VerifierAgent: Validates results with quality scoring
- ResearcherAgent: Handles Azure documentation queries via Microsoft Learn MCP
- ArchitectAgent: Provides architecture best practices via Azure MCP
- GHCPCodingAgent: Generates code/CLI commands via GitHub Copilot SDK
"""

from src.agents.researcher import ResearcherAgent
from src.agents.architect import ArchitectAgent
from src.agents.ghcp_coding_agent import GHCPCodingAgent
from src.agents.planner import PlannerAgent
from src.agents.executor import ExecutorAgent
from src.agents.verifier import VerifierAgent
from src.agents.orchestrator import OrchestratorAgent
from src.agents.classifier import QueryClassifier, QueryCategory
from src.agents.models import (
    AgentResponse,
    ExecutionStepDetail,
    VerificationScoreDetail,
)

# Backwards compatibility alias (deprecated - use OrchestratorAgent directly)
SolutionEngineerAgent = OrchestratorAgent


__all__ = [
    # Primary orchestrator
    "OrchestratorAgent",
    # Query classifier
    "QueryClassifier",
    "QueryCategory",
    # PEV agents
    "PlannerAgent",
    "ExecutorAgent", 
    "VerifierAgent",
    # Sub-agents
    "ResearcherAgent",
    "ArchitectAgent",
    "GHCPCodingAgent",
    # Models
    "AgentResponse",
    "ExecutionStepDetail",
    "VerificationScoreDetail",
]
