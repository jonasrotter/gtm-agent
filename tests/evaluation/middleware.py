"""
Evaluation Middleware for tracking tool invocations.

Uses agent_framework's FunctionMiddleware to intercept all tool/function
calls and capture metrics for evaluation purposes.
"""

import time
from datetime import datetime
from typing import Any

from agent_framework import FunctionMiddleware, FunctionInvocationContext

from tests.evaluation.models import ToolInvocation


class EvaluationMiddleware(FunctionMiddleware):
    """
    Middleware that captures tool invocations for evaluation.
    
    Tracks:
    - Tool name
    - Arguments passed
    - Result returned
    - Execution duration
    - Any errors encountered
    
    Usage:
        middleware = EvaluationMiddleware()
        agent = ChatAgent(chat_client=client, middleware=middleware)
        
        # After agent execution
        for invocation in middleware.invocations:
            print(f"{invocation.tool_name}: {invocation.duration_seconds}s")
        
        # Reset for next task
        middleware.reset()
    """
    
    def __init__(self):
        """Initialize the middleware with empty invocation list."""
        self._invocations: list[ToolInvocation] = []
        self._start_times: dict[str, float] = {}
    
    @property
    def invocations(self) -> list[ToolInvocation]:
        """Get all captured tool invocations."""
        return self._invocations.copy()
    
    @property
    def tool_names(self) -> list[str]:
        """Get unique tool names that were invoked."""
        return list(set(inv.tool_name for inv in self._invocations))
    
    @property
    def total_duration(self) -> float:
        """Get total duration of all tool invocations."""
        return sum(inv.duration_seconds for inv in self._invocations)
    
    @property
    def call_count(self) -> int:
        """Get total number of tool invocations."""
        return len(self._invocations)
    
    def reset(self) -> None:
        """Reset the middleware for a new evaluation task."""
        self._invocations.clear()
        self._start_times.clear()
    
    def get_tool_metrics(self) -> dict[str, dict[str, Any]]:
        """
        Get aggregated metrics per tool.
        
        Returns:
            Dict mapping tool names to their metrics:
            {
                "tool_name": {
                    "count": int,
                    "total_duration": float,
                    "avg_duration": float,
                    "success_count": int,
                    "error_count": int,
                }
            }
        """
        metrics: dict[str, dict[str, Any]] = {}
        
        for inv in self._invocations:
            if inv.tool_name not in metrics:
                metrics[inv.tool_name] = {
                    "count": 0,
                    "total_duration": 0.0,
                    "durations": [],
                    "success_count": 0,
                    "error_count": 0,
                }
            
            m = metrics[inv.tool_name]
            m["count"] += 1
            m["total_duration"] += inv.duration_seconds
            m["durations"].append(inv.duration_seconds)
            
            if inv.error:
                m["error_count"] += 1
            else:
                m["success_count"] += 1
        
        # Calculate averages
        for tool_name, m in metrics.items():
            m["avg_duration"] = m["total_duration"] / m["count"] if m["count"] > 0 else 0.0
            del m["durations"]  # Remove raw durations from output
        
        return metrics
    
    async def process(
        self,
        context: FunctionInvocationContext,
        next,
    ) -> None:
        """
        Process a function invocation, capturing metrics.
        
        Args:
            context: Function invocation context containing function, arguments, and metadata.
            next: Function to call the next middleware or final function execution.
        """
        start_time = time.perf_counter()
        error_msg: str | None = None
        
        try:
            # Execute the function
            await next(context)
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            raise
        finally:
            duration = time.perf_counter() - start_time
            
            # Extract arguments safely
            try:
                if hasattr(context.arguments, "model_dump"):
                    arguments = context.arguments.model_dump()
                elif hasattr(context.arguments, "dict"):
                    arguments = context.arguments.dict()
                else:
                    arguments = {"raw": str(context.arguments)}
            except Exception:
                arguments = {"raw": str(context.arguments)}
            
            # Extract result safely
            try:
                result = context.result
                if hasattr(result, "model_dump"):
                    result = result.model_dump()
                elif hasattr(result, "dict"):
                    result = result.dict()
                elif isinstance(result, str) and len(result) > 1000:
                    result = result[:1000] + "... [truncated]"
            except Exception:
                result = str(context.result)[:1000] if context.result else None
            
            # Record the invocation
            invocation = ToolInvocation(
                tool_name=context.function.name,
                arguments=arguments,
                result=result,
                duration_seconds=duration,
                error=error_msg,
                timestamp=datetime.utcnow(),
            )
            self._invocations.append(invocation)


class FeedbackCapturingMiddleware(FunctionMiddleware):
    """
    Middleware that injects feedback prompts into tool responses.
    
    This middleware modifies tool responses to request feedback from the agent
    about tool usability, following the Anthropic evaluation pattern.
    """
    
    FEEDBACK_PROMPT = """

Please provide brief feedback on this tool:
1. Was the tool name clear and descriptive?
2. Were the input parameters well-documented?
3. Did the tool return useful results?
4. Any suggestions for improvement?

Wrap your feedback in <tool_feedback> tags."""
    
    def __init__(self, capture_feedback: bool = True):
        """Initialize with feedback capture setting."""
        self._capture_feedback = capture_feedback
        self._feedback_responses: list[str] = []
    
    @property
    def feedback_responses(self) -> list[str]:
        """Get captured feedback responses."""
        return self._feedback_responses.copy()
    
    def reset(self) -> None:
        """Reset captured feedback."""
        self._feedback_responses.clear()
    
    async def process(
        self,
        context: FunctionInvocationContext,
        next,
    ) -> None:
        """Process invocation and optionally inject feedback prompt."""
        await next(context)
        
        if self._capture_feedback and context.result:
            # Append feedback request to result
            if isinstance(context.result, str):
                context.result = context.result + self.FEEDBACK_PROMPT
