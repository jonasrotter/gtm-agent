"""
Orchestrator Agent - Unified entry point using Plan-Execute-Verify pattern.

Replaces SolutionEngineerAgent with a GroupChat-based workflow that:
1. Classifies: Determines query complexity for optimal routing
2. Fast Path: Simple queries bypass PEV (direct agent call)
3. Plans: Breaks down queries into structured execution steps
4. Executes: Runs steps via specialized sub-agents
5. Verifies: Validates results with quality scoring

Supports iteration on verification failure and human escalation.
"""

import time
import uuid
from collections import OrderedDict
from typing import Any

from agent_framework import ChatAgent

from src.agents.base import create_azure_chat_client
from src.agents.classifier import QueryClassifier, QueryCategory
from src.agents.models import (
    AgentResponse,
    ExecutionPlan,
    ExecutionResult,
    ExecutionStepDetail,
    HumanEscalationRequest,
    VerificationDecision,
    VerificationResult,
    VerificationScoreDetail,
)
from src.agents.planner import PlannerAgent
from src.agents.executor import ExecutorAgent
from src.agents.verifier import VerifierAgent
from src.agents.researcher import ResearcherAgent
from src.agents.architect import ArchitectAgent
from src.agents.ghcp_coding_agent import GHCPCodingAgent
from src.config import get_settings
from src.utils.logging import get_logger


logger = get_logger(__name__)


COORDINATOR_INSTRUCTIONS = """You are the Coordinator for a Plan-Execute-Verify workflow.

## Your Role
Manage the conversation flow between three specialized agents:
1. **Planner** - Creates execution plans from user queries
2. **Executor** - Executes plan steps using tools
3. **Verifier** - Validates results and provides feedback

## Workflow Rules

### Initial Flow
1. Always start with Planner to create an execution plan
2. Then Executor runs the plan steps
3. Finally Verifier evaluates the results

### On Verification Failure (score < 0.8)
1. Pass verifier feedback back to Planner for refinement
2. Executor runs the refined plan
3. Verifier evaluates again
4. Repeat up to 4 total iterations

### Termination Conditions
- **Accept**: Verifier score >= 0.8 → end conversation
- **Max Iterations**: After 4 iterations → end with best result
- **Escalate**: Verifier recommends escalation → end with human review flag

## Speaker Selection Guidelines
- After user message → Planner
- After Planner → Executor  
- After Executor → Verifier
- After Verifier (retry) → Planner
- After Verifier (accept/escalate) → END

Always explain your speaker selection briefly before choosing."""


class OrchestratorAgent:
    """
    Unified orchestrator using Plan-Execute-Verify pattern with fast path optimization.
    
    Entry point for all queries. Uses query classification to determine optimal path:
    - Fast Path: Simple factual queries bypass PEV (direct researcher call)
    - Lite PEV: HowTo/Code queries use single iteration
    - Full PEV: Complex queries use multi-iteration loop
    
    Supports multi-turn conversations via session management.
    """
    
    # Default configuration (overridden by category config)
    DEFAULT_ACCEPTANCE_THRESHOLD = 0.8
    DEFAULT_MAX_ITERATIONS = 4
    MAX_SESSIONS = 1000
    
    def __init__(self):
        """Initialize OrchestratorAgent with all sub-components."""
        # Query classifier for intelligent routing
        self.classifier = QueryClassifier()
        
        # Create sub-agents (owned here, shared via DI)
        self.researcher = ResearcherAgent()
        self.architect = ArchitectAgent()
        self.ghcp_coding = GHCPCodingAgent()
        
        # Create PEV agents
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent(
            researcher=self.researcher,
            architect=self.architect,
            ghcp_coding=self.ghcp_coding,
        )
        self.verifier = VerifierAgent()
        
        # Session management (LRU cache)
        self._sessions: OrderedDict[str, tuple[Any, int]] = OrderedDict()
        
        logger.info(
            "OrchestratorAgent initialized with fast path support",
            default_max_iterations=self.DEFAULT_MAX_ITERATIONS,
            default_threshold=self.DEFAULT_ACCEPTANCE_THRESHOLD,
            max_sessions=self.MAX_SESSIONS,
        )
    
    def _get_or_create_session(self, session_id: str | None) -> tuple[str, int]:
        """
        Get existing session or create a new one.
        
        Args:
            session_id: Optional session ID. If None, creates new session.
            
        Returns:
            Tuple of (session_id, turn_count).
        """
        if not session_id:
            session_id = str(uuid.uuid4())
            logger.debug("Generated new session", session_id=session_id)
            return session_id, 1
        
        if session_id in self._sessions:
            self._sessions.move_to_end(session_id)
            _, turn_count = self._sessions[session_id]
            logger.debug(
                "Resuming existing session",
                session_id=session_id,
                turn_count=turn_count + 1,
            )
            return session_id, turn_count + 1
        
        logger.debug("Creating new session with provided ID", session_id=session_id)
        return session_id, 1
    
    def _save_session(self, session_id: str, context: Any, turn_count: int) -> None:
        """Save session context to cache with LRU eviction."""
        while len(self._sessions) >= self.MAX_SESSIONS:
            evicted_id, _ = self._sessions.popitem(last=False)
            logger.debug("Evicted oldest session", session_id=evicted_id)
        
        self._sessions[session_id] = (context, turn_count)
        logger.debug(
            "Saved session",
            session_id=session_id,
            turn_count=turn_count,
            active_sessions=len(self._sessions),
        )
    
    async def run(self, query: str, session_id: str | None = None) -> AgentResponse:
        """
        Process a user query through the optimal path based on query classification.
        
        Routing:
        - FACTUAL: Fast path (direct researcher call, no PEV)
        - HOWTO/CODE: Lite PEV (1 iteration, lower threshold)
        - ARCHITECTURE: Standard PEV (2 iterations)
        - COMPLEX: Full PEV (4 iterations)
        
        Args:
            query: User's question or request.
            session_id: Optional session ID for conversation continuity.
            
        Returns:
            AgentResponse with content, verification metadata, and escalation flag.
        """
        session_id, turn_count = self._get_or_create_session(session_id)
        
        # Classify query to determine optimal path
        category = self.classifier.classify(query)
        config = category.get_config()
        
        logger.info(
            "Processing query",
            query=query[:100],
            session_id=session_id,
            turn_count=turn_count,
            category=category.value,
            skip_pev=config["skip_pev"],
            max_iterations=config["max_iterations"],
        )
        
        # Fast path for simple factual queries
        if config["skip_pev"]:
            return await self._fast_path(
                query=query,
                session_id=session_id,
                turn_count=turn_count,
                category=category,
            )
        
        # PEV loop with category-specific configuration
        return await self._run_pev_loop(
            query=query,
            session_id=session_id,
            turn_count=turn_count,
            category=category,
            config=config,
        )
    
    async def _fast_path(
        self,
        query: str,
        session_id: str,
        turn_count: int,
        category: QueryCategory,
    ) -> AgentResponse:
        """
        Fast path for simple queries - bypass PEV loop entirely.
        
        Directly calls the appropriate agent without planning or verification.
        Used for factual queries where full PEV is overkill.
        
        Args:
            query: User's question.
            session_id: Session ID for tracking.
            turn_count: Current turn in conversation.
            category: Query category (determines which agent to call).
            
        Returns:
            AgentResponse from direct agent call.
        """
        logger.info(
            "Using fast path",
            category=category.value,
            query=query[:50],
        )
        
        config = category.get_config()
        tool = config.get("default_tool", "research")
        
        # Call the appropriate agent directly
        if tool == "research":
            result = await self.researcher.run(query)
            agent_used = "researcher"
        elif tool == "architecture":
            result = await self.architect.run(query)
            agent_used = "architect"
        elif tool == "code":
            result = await self.ghcp_coding.run(query)
            agent_used = "ghcp_coding"
        else:
            # Default to researcher
            result = await self.researcher.run(query)
            agent_used = "researcher"
        
        # Get content from result (agents return different types)
        if hasattr(result, 'content'):
            content = result.content
        elif hasattr(result, 'text'):
            content = result.text
        elif isinstance(result, str):
            content = result
        else:
            content = str(result)
        
        # Build response (no verification for fast path)
        response = AgentResponse(
            content=content,
            agent_used=agent_used,
            session_id=session_id,
            turn_count=turn_count,
            verification_score=None,  # No verification
            iterations_used=1,
            requires_human_review=False,
            plan_summary=f"Fast path: direct {agent_used} call ({category.value} query)",
            execution_steps=[
                ExecutionStepDetail(
                    step_number=1,
                    tool=tool,
                    query=query,
                    status="completed",
                    output_preview=content[:500] if content else "",
                )
            ],
            score_details=None,  # No verification scores
            plan_rationale=f"Query classified as {category.value} - bypassed PEV for efficiency",
            query_category=category.value,
        )
        
        # Save session context
        session_context = {
            "last_plan": None,
            "last_result": result,
            "last_verification": None,
            "category": category.value,
            "fast_path": True,
        }
        self._save_session(session_id, session_context, turn_count)
        
        logger.info(
            "Fast path completed",
            session_id=session_id,
            agent_used=agent_used,
            category=category.value,
        )
        
        return response
    
    async def _run_pev_loop(
        self,
        query: str,
        session_id: str,
        turn_count: int,
        category: QueryCategory,
        config: dict[str, Any],
    ) -> AgentResponse:
        """
        Run the Plan-Execute-Verify loop with category-specific configuration.
        
        Args:
            query: User's question or request.
            session_id: Session ID for tracking.
            turn_count: Current turn in conversation.
            category: Query category for logging.
            config: Category-specific configuration (max_iterations, threshold).
            
        Returns:
            AgentResponse with full PEV metadata.
        """
        max_iterations = config.get("max_iterations", self.DEFAULT_MAX_ITERATIONS)
        threshold = config.get("threshold", self.DEFAULT_ACCEPTANCE_THRESHOLD)
        early_accept_threshold = config.get("early_accept_threshold", 0.85)
        settings = get_settings()
        
        # Use extended timeout for complex queries
        if category.value == "complex":
            pev_timeout = settings.pev_complex_timeout_seconds
        else:
            pev_timeout = settings.pev_loop_timeout_seconds
        
        # Estimated time per iteration for time-aware budgeting
        estimated_iteration_time = 45  # seconds
        
        # Determine max steps based on category
        # Reduced complex from 4 to 3 to avoid timeouts
        max_steps_map = {
            "factual": 1,
            "code": 1,
            "howto": 2,
            "architecture": 2,
            "complex": 3,  # Reduced from 4 to fit within timeout budget
        }
        max_steps = max_steps_map.get(category.value, 3)
        
        logger.info(
            f"Running PEV loop",
            category=category.value,
            max_iterations=max_iterations,
            threshold=threshold,
            early_accept_threshold=early_accept_threshold,
            max_steps=max_steps,
            timeout_seconds=pev_timeout,
        )
        
        # Run PEV loop with time budget
        pev_start_time = time.perf_counter()
        iteration = 0
        best_result: ExecutionResult | None = None
        best_verification: VerificationResult | None = None
        current_plan: ExecutionPlan | None = None
        feedback: str = ""
        timeout_reached = False
        
        while iteration < max_iterations:
            # Check cumulative time budget before starting new iteration
            elapsed_time = time.perf_counter() - pev_start_time
            if elapsed_time >= pev_timeout:
                logger.warning(
                    "PEV loop time budget exhausted",
                    elapsed_seconds=elapsed_time,
                    timeout_seconds=pev_timeout,
                    iteration=iteration,
                )
                timeout_reached = True
                break
            
            iteration += 1
            
            logger.info(
                f"PEV iteration {iteration}/{max_iterations}",
                elapsed_seconds=round(elapsed_time, 1),
                remaining_seconds=round(pev_timeout - elapsed_time, 1),
            )
            
            # Phase 1: Plan (pass max_steps and category for enforcement)
            if iteration == 1:
                current_plan = await self.planner.create_plan(
                    query=query,
                    max_steps=max_steps,
                    query_category=category.value,
                )
            else:
                # Refine plan based on feedback
                current_plan = await self.planner.refine_plan(
                    query=query,
                    feedback=feedback,
                    previous_plan=current_plan,
                    max_steps=max_steps,
                    query_category=category.value,
                )
            
            # Phase 2: Execute
            result = await self.executor.execute_plan(current_plan, query)
            
            # Phase 3: Verify
            verification = await self.verifier.verify(
                original_query=query,
                plan=current_plan,
                result=result,
                iteration=iteration,
            )
            
            # Track best result
            if best_verification is None or verification.score.overall > best_verification.score.overall:
                best_result = result
                best_verification = verification
            
            # Check termination conditions (using category-specific threshold)
            if verification.decision == VerificationDecision.ACCEPT:
                logger.info(
                    "Verification accepted",
                    score=verification.score.overall,
                    threshold=threshold,
                    iteration=iteration,
                )
                break
            
            # Early accept: High quality on first try - no need for more iterations
            if early_accept_threshold and verification.score.overall >= early_accept_threshold:
                logger.info(
                    "Early acceptance - high quality response",
                    score=verification.score.overall,
                    early_accept_threshold=early_accept_threshold,
                    iteration=iteration,
                )
                break
            
            # Accept if score meets category threshold even without explicit ACCEPT
            if verification.score.overall >= threshold:
                logger.info(
                    "Score meets category threshold",
                    score=verification.score.overall,
                    threshold=threshold,
                    iteration=iteration,
                )
                break
            
            if verification.decision == VerificationDecision.ESCALATE:
                logger.info(
                    "Verification recommends escalation",
                    score=verification.score.overall,
                    iteration=iteration,
                )
                break
            
            # Check time budget before continuing to next iteration
            elapsed_time = time.perf_counter() - pev_start_time
            remaining_time = pev_timeout - elapsed_time
            
            # Time-aware budget check: Only continue if we have enough time for another iteration
            if remaining_time < estimated_iteration_time:
                logger.info(
                    "Insufficient time for another iteration, accepting current result",
                    remaining_seconds=round(remaining_time, 1),
                    estimated_iteration_time=estimated_iteration_time,
                    iteration=iteration,
                    current_score=verification.score.overall,
                )
                break
            
            if elapsed_time >= pev_timeout:
                logger.warning(
                    "PEV loop time budget exhausted mid-iteration",
                    elapsed_seconds=elapsed_time,
                    timeout_seconds=pev_timeout,
                    iteration=iteration,
                )
                timeout_reached = True
                break
            
            # Prepare feedback for next iteration
            feedback = verification.feedback_for_replanning
            if not feedback:
                feedback = verification.summary
            
            logger.debug(
                "Retrying with feedback",
                iteration=iteration,
                feedback=feedback[:100],
            )
        
        # Build response
        # Mark for human review if timeout reached without good results
        requires_human_review = (
            (best_verification and best_verification.decision == VerificationDecision.ESCALATE) or
            (best_verification and best_verification.score.overall < threshold) or
            timeout_reached
        )
        
        # Log final PEV loop status
        total_pev_time = time.perf_counter() - pev_start_time
        logger.info(
            "PEV loop completed",
            total_time_seconds=round(total_pev_time, 1),
            iterations_completed=iteration,
            timeout_reached=timeout_reached,
            final_score=best_verification.score.overall if best_verification else None,
        )
        
        # Save session context
        session_context = {
            "last_plan": current_plan,
            "last_result": best_result,
            "last_verification": best_verification,
        }
        self._save_session(session_id, session_context, turn_count)
        
        # Build execution step details for response
        execution_steps = []
        if best_result and best_result.step_results:
            for step_result in best_result.step_results:
                # Find the corresponding plan step for the query
                plan_step = next(
                    (s for s in current_plan.steps if s.step_number == step_result.step_number),
                    None
                ) if current_plan else None
                
                execution_steps.append(ExecutionStepDetail(
                    step_number=step_result.step_number,
                    tool=step_result.tool_used,
                    query=plan_step.query if plan_step else "N/A",
                    status=step_result.status.value,
                    output_preview=step_result.output[:500] if step_result.output else "",
                ))
        
        # Build score details
        score_details = None
        if best_verification:
            score_details = VerificationScoreDetail(
                overall=best_verification.score.overall,
                correctness=best_verification.score.correctness,
                completeness=best_verification.score.completeness,
                consistency=best_verification.score.consistency,
            )
        
        response = AgentResponse(
            content=best_result.final_output,
            agent_used=", ".join(best_result.agents_used) if best_result.agents_used else None,
            session_id=session_id,
            turn_count=turn_count,
            verification_score=best_verification.score.overall,
            iterations_used=iteration,
            requires_human_review=requires_human_review,
            plan_summary=current_plan.summary if current_plan else None,
            execution_steps=execution_steps,
            score_details=score_details,
            plan_rationale=current_plan.rationale if current_plan else None,
            query_category=category.value,
        )
        
        logger.info(
            "Query completed",
            session_id=session_id,
            score=response.verification_score,
            iterations=response.iterations_used,
            requires_review=response.requires_human_review,
            category=response.query_category,
        )
        
        return response
    
    def get_escalation_request(
        self,
        query: str,
        result: ExecutionResult,
        verification: VerificationResult,
        iterations: int,
    ) -> HumanEscalationRequest:
        """
        Create a human escalation request for failed verification.
        
        Args:
            query: The original user query.
            result: The best execution result achieved.
            verification: The final verification result.
            iterations: Number of iterations attempted.
            
        Returns:
            HumanEscalationRequest with all context for human review.
        """
        return HumanEscalationRequest(
            query=query,
            partial_result=result.final_output,
            verification_issues=[
                issue.model_dump() for issue in verification.issues
            ],
            iterations_attempted=iterations,
            last_score=verification.score.overall,
        )
    
    def clear_session(self, session_id: str) -> bool:
        """Clear a specific session from the cache."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info("Session cleared", session_id=session_id)
            return True
        return False
    
    def get_session_info(self, session_id: str) -> dict[str, Any] | None:
        """Get information about a session."""
        if session_id in self._sessions:
            context, turn_count = self._sessions[session_id]
            return {
                "session_id": session_id,
                "turn_count": turn_count,
                "has_context": context is not None,
                "active": True,
            }
        return None
    
    async def close(self):
        """Clean up resources (especially GHCPCodingAgent's Copilot session)."""
        await self.ghcp_coding.close()
        logger.info("OrchestratorAgent closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# =============================================================================
# Factory Function
# =============================================================================

def get_orchestrator_agent() -> OrchestratorAgent:
    """Get an OrchestratorAgent instance."""
    return OrchestratorAgent()


# Backwards compatibility alias
def get_solution_engineer_agent() -> OrchestratorAgent:
    """
    Backwards compatibility alias for get_orchestrator_agent.
    
    Deprecated: Use get_orchestrator_agent() instead.
    """
    logger.warning(
        "get_solution_engineer_agent() is deprecated, use get_orchestrator_agent()"
    )
    return get_orchestrator_agent()
