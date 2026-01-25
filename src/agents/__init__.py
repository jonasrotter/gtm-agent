"""
Agents package for specialist agent implementations.

Provides agent implementations using Microsoft Agent Framework:
- SolutionEngineerAgent: Orchestrator routing queries to specialists
- ResearcherAgent: Handles Azure documentation queries via Microsoft Learn MCP
- ArchitectAgent: Provides architecture best practices via Azure MCP
- GHCPCodingAgent: Generates code/CLI commands via GitHub Copilot SDK
- AgentResponse: Response dataclass with content and agent_used tracking
"""

from src.agents.researcher import ResearcherAgent
from src.agents.architect import ArchitectAgent
from src.agents.ghcp_coding_agent import GHCPCodingAgent
from src.agents.solution_engineer import SolutionEngineerAgent, AgentResponse


__all__ = [
    "ResearcherAgent",
    "ArchitectAgent",
    "GHCPCodingAgent",
    "SolutionEngineerAgent",
    "AgentResponse",
]
