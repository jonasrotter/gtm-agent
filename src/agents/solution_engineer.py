"""
Solution Engineer Agent - Orchestrator using sub-agents as tools.

Routes queries to specialized sub-agents based on user intent.
Uses the agent.as_tool() pattern for clean orchestration.
Supports multi-turn conversations via AgentThread management.
"""

import uuid
from collections import OrderedDict
from typing import Any

from agent_framework import ChatAgent, function_middleware, FunctionInvocationContext

from src.agents.base import create_azure_chat_client
from src.agents.models import AgentResponse
from src.agents.researcher import ResearcherAgent
from src.agents.architect import ArchitectAgent
from src.agents.ghcp_coding_agent import GHCPCodingAgent
from src.lib.logging import get_logger


logger = get_logger(__name__)


ORCHESTRATOR_INSTRUCTIONS = """You are a Solution Engineering Agent that ROUTES queries to specialized tools.

**CRITICAL RULE: You are a ROUTER ONLY. You MUST NOT answer questions directly. You MUST ALWAYS call one of your tools.**

You have three specialized tools:

1. **research** - Search Azure documentation and answer questions with source citations
2. **architecture** - Provide Azure architecture guidance and WAF-aligned recommendations  
3. **code** - Generate code, Azure CLI commands, scripts, and test plans

## MANDATORY ROUTING RULES

For EVERY query, you MUST call exactly ONE tool. Pick the best match:

| Query Contains | MUST Call Tool |
|----------------|----------------|
| "what is", "how to", "explain", "documentation" | research |
| "best practice", "architecture", "design", "review", "WAF" | architecture |
| "CLI", "command", "script", "code", "generate", "create", "deploy", "test plan" | code |

## FORBIDDEN BEHAVIORS

❌ NEVER generate code or CLI commands yourself - call the `code` tool
❌ NEVER explain concepts yourself - call the `research` tool  
❌ NEVER give architecture advice yourself - call the `architecture` tool
❌ NEVER respond without first calling a tool

## SCOPE

Only handle Azure-related queries. For non-Azure topics, politely decline.

## YOUR ONLY JOB

1. Read the query
2. Pick the most appropriate tool (research, architecture, or code)
3. Call that tool with the user's query
4. Return the tool's response
"""


class SolutionEngineerAgent:
    """
    Orchestrator that routes to specialized sub-agents.
    
    Uses sub-agents as tools via the .as_tool() pattern:
    - ResearcherAgent → research tool
    - ArchitectAgent → architecture tool  
    - GHCPCodingAgent → code tool
    
    Supports multi-turn conversations via AgentThread caching.
    Sessions are identified by session_id and maintain conversation history.
    """
    
    # Map tool names to user-friendly sub-agent identifiers
    TOOL_TO_AGENT_MAP = {
        "research": "researcher",
        "architecture": "architect",
        "code": "ghcp_coding",
    }
    
    # Maximum number of sessions to keep in memory (LRU eviction)
    MAX_SESSIONS = 1000

    def __init__(self):
        """Initialize SolutionEngineerAgent with sub-agents as tools."""
        # Create sub-agents
        self.researcher = ResearcherAgent()
        self.architect = ArchitectAgent()
        self.ghcp_coding = GHCPCodingAgent()
        
        # Track the last tool called for response metadata
        self._last_tool_called: str | None = None
        
        # Session management: LRU cache of session_id -> (AgentThread, turn_count)
        self._sessions: OrderedDict[str, tuple[Any, int]] = OrderedDict()
        
        # Convert sub-agents to tools
        tools = [
            self.researcher.as_tool(),
            self.architect.as_tool(),
            self.ghcp_coding.as_tool(),
        ]
        
        # Create orchestrator agent with tracking middleware
        self.agent = ChatAgent(
            chat_client=create_azure_chat_client(),
            name="solution_engineer",
            instructions=ORCHESTRATOR_INSTRUCTIONS,
            tools=tools,
            middleware=[self._create_tracking_middleware()],
        )
        
        logger.info(
            "SolutionEngineerAgent initialized",
            tools=["research", "architecture", "code"],
            max_sessions=self.MAX_SESSIONS,
        )
    
    def _create_tracking_middleware(self):
        """
        Create middleware that tracks which tool/sub-agent is invoked.
        
        Uses the official agent_framework @function_middleware pattern.
        """
        agent_ref = self  # Capture reference to self for closure
        
        @function_middleware
        async def tracking_middleware(
            context: FunctionInvocationContext,
            next,
        ) -> None:
            """Track tool invocations and map to sub-agent names."""
            tool_name = context.function.name
            agent_ref._last_tool_called = agent_ref.TOOL_TO_AGENT_MAP.get(
                tool_name, tool_name
            )
            logger.debug(
                "Tool invoked",
                tool_name=tool_name,
                agent_used=agent_ref._last_tool_called,
            )
            await next(context)
        
        return tracking_middleware
    
    def _get_or_create_session(self, session_id: str | None) -> tuple[str, Any | None, int]:
        """
        Get existing session or create a new one.
        
        Args:
            session_id: Optional session ID. If None, creates new session.
            
        Returns:
            Tuple of (session_id, thread_or_None, turn_count).
        """
        # Generate new session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
            logger.debug("Generated new session", session_id=session_id)
            return session_id, None, 1
        
        # Check if session exists
        if session_id in self._sessions:
            # Move to end (most recently used)
            self._sessions.move_to_end(session_id)
            thread, turn_count = self._sessions[session_id]
            logger.debug(
                "Resuming existing session",
                session_id=session_id,
                turn_count=turn_count + 1,
            )
            return session_id, thread, turn_count + 1
        
        # New session with provided ID
        logger.debug("Creating new session with provided ID", session_id=session_id)
        return session_id, None, 1
    
    def _save_session(self, session_id: str, thread: Any, turn_count: int) -> None:
        """
        Save session thread to cache with LRU eviction.
        
        Args:
            session_id: The session identifier.
            thread: The AgentThread to cache.
            turn_count: Current turn count for this session.
        """
        # Evict oldest session if at capacity
        while len(self._sessions) >= self.MAX_SESSIONS:
            evicted_id, _ = self._sessions.popitem(last=False)
            logger.debug("Evicted oldest session", session_id=evicted_id)
        
        self._sessions[session_id] = (thread, turn_count)
        logger.debug(
            "Saved session",
            session_id=session_id,
            turn_count=turn_count,
            active_sessions=len(self._sessions),
        )
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear a specific session from the cache.
        
        Args:
            session_id: The session to clear.
            
        Returns:
            True if session was found and cleared, False otherwise.
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info("Session cleared", session_id=session_id)
            return True
        return False
    
    def get_session_info(self, session_id: str) -> dict[str, Any] | None:
        """
        Get information about a session.
        
        Args:
            session_id: The session to query.
            
        Returns:
            Session info dict or None if not found.
        """
        if session_id in self._sessions:
            _, turn_count = self._sessions[session_id]
            return {
                "session_id": session_id,
                "turn_count": turn_count,
                "active": True,
            }
        return None

    async def run(self, query: str, session_id: str | None = None) -> AgentResponse:
        """
        Process a user query by routing to appropriate sub-agent.
        
        Supports multi-turn conversations when session_id is provided.
        
        Args:
            query: User's question or request.
            session_id: Optional session ID for conversation continuity.
                If provided and session exists, conversation history is preserved.
                If not provided, a new session_id is generated.
            
        Returns:
            AgentResponse containing the response content, which sub-agent was used,
            the session_id for future turns, and the current turn count.
        """
        # Reset tracking before each query
        self._last_tool_called = None
        
        # Clear tool call tracking on the chat client
        chat_client = self.agent.chat_client
        if hasattr(chat_client, "clear_tool_call_tracking"):
            chat_client.clear_tool_call_tracking()
        
        # Get or create session
        session_id, thread, turn_count = self._get_or_create_session(session_id)
        
        async with self.agent:
            # Run agent with thread for multi-turn support
            if thread is not None:
                result = await self.agent.run(query, thread=thread)
            else:
                # First turn: create new thread
                thread = self.agent.get_new_thread()
                result = await self.agent.run(query, thread=thread)
            
            # Save the thread for future turns
            self._save_session(session_id, thread, turn_count)
            
            # Check if middleware tracked a tool call, otherwise check chat client
            agent_used = self._last_tool_called
            if not agent_used:
                # Fall back to checking the chat client's tracked tool calls
                if hasattr(chat_client, "_last_tool_calls") and chat_client._last_tool_calls:
                    first_tool = chat_client._last_tool_calls[0]
                    agent_used = self.TOOL_TO_AGENT_MAP.get(first_tool, first_tool)
            
            return AgentResponse(
                content=result.text,
                agent_used=agent_used,
                session_id=session_id,
                turn_count=turn_count,
            )
    
    async def close(self):
        """Clean up resources (especially GHCPCodingAgent's Copilot session)."""
        await self.ghcp_coding.close()
        logger.info("SolutionEngineerAgent closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# =============================================================================
# Factory Function
# =============================================================================

def get_solution_engineer_agent() -> SolutionEngineerAgent:
    """Get a SolutionEngineerAgent instance."""
    return SolutionEngineerAgent()
