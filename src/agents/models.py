"""
Agent response models.

Data structures for agent responses with tracking metadata.
"""

from dataclasses import dataclass


@dataclass
class AgentResponse:
    """
    Response from SolutionEngineerAgent with tracking metadata.
    
    Attributes:
        content: The text response from the agent.
        agent_used: The sub-agent that processed the query.
            Values: "researcher", "architect", "ghcp_coding", or None if no tool was called.
        session_id: The session ID for multi-turn conversation continuity.
        turn_count: The number of turns in this conversation session.
    """
    content: str
    agent_used: str | None = None
    session_id: str | None = None
    turn_count: int = 1
