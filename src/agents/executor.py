"""
Executor Agent for the Plan-Execute-Verify pattern.

Executes plan steps by invoking sub-agents as tools.
Receives sub-agent instances via dependency injection.

Supports parallel execution of independent steps using asyncio.gather().
Steps with no dependencies (depends_on=[]) or whose dependencies are already
completed can run concurrently, significantly reducing total execution time.
"""

import asyncio
import time
from typing import TYPE_CHECKING

from agent_framework import ChatAgent

from src.agents.base import create_azure_chat_client
from src.agents.models import (
    ExecutionPlan,
    ExecutionResult,
    PlanStep,
    StepResult,
    StepStatus,
)
from src.config import get_settings
from src.utils.logging import get_logger

if TYPE_CHECKING:
    from src.agents.researcher import ResearcherAgent
    from src.agents.architect import ArchitectAgent
    from src.agents.ghcp_coding_agent import GHCPCodingAgent


logger = get_logger(__name__)


EXECUTOR_INSTRUCTIONS = """You are an Execution Agent that carries out plan steps using specialized tools.

## Your Role
Execute each step in the provided plan by calling the appropriate tool with the given query.

## Available Tools
1. **research** - Search Azure documentation and get information with citations
2. **architecture** - Get Azure architecture guidance and WAF best practices
3. **code** - Generate code, CLI commands, scripts, and deployment templates

## Execution Guidelines

1. **Follow the Plan**: Execute steps in the order specified
2. **Use Exact Queries**: Pass the step's query to the corresponding tool
3. **Capture All Output**: Return complete tool responses
4. **Handle Errors**: If a tool fails, report the error clearly
5. **Respect Dependencies**: Wait for dependent steps to complete

## Response Format
After executing a step, provide the tool's response directly.
Do not add commentary unless the tool fails - then explain the error."""


class ExecutorAgent:
    """
    Executes plan steps using sub-agents as tools.
    
    Receives sub-agent instances via dependency injection to avoid
    duplicate agent creation. Converts sub-agents to tools using .as_tool().
    """
    
    def __init__(
        self,
        researcher: "ResearcherAgent",
        architect: "ArchitectAgent",
        ghcp_coding: "GHCPCodingAgent",
    ):
        """
        Initialize ExecutorAgent with sub-agent dependencies.
        
        Args:
            researcher: ResearcherAgent instance for documentation queries.
            architect: ArchitectAgent instance for architecture guidance.
            ghcp_coding: GHCPCodingAgent instance for code generation.
        """
        self.researcher = researcher
        self.architect = architect
        self.ghcp_coding = ghcp_coding
        
        # Map tool names to sub-agents for tracking
        self._tool_to_agent = {
            "research": "researcher",
            "architecture": "architect",
            "code": "ghcp_coding",
        }
        
        # Create agent with sub-agents as tools
        self.agent = ChatAgent(
            chat_client=create_azure_chat_client(),
            name="Executor",
            description="Executes plan steps using specialized sub-agent tools",
            instructions=EXECUTOR_INSTRUCTIONS,
            tools=[
                researcher.as_tool(),
                architect.as_tool(),
                ghcp_coding.as_tool(),
            ],
        )
        
        logger.info(
            "ExecutorAgent initialized",
            tools=list(self._tool_to_agent.keys()),
        )
    
    async def execute_plan(self, plan: ExecutionPlan, original_query: str) -> ExecutionResult:
        """
        Execute all steps in an execution plan.
        
        Uses parallel execution for independent steps (steps with no unmet dependencies).
        Steps are grouped into execution waves based on their dependency graph.
        
        Args:
            plan: The execution plan with ordered steps.
            original_query: The original user query for context.
            
        Returns:
            ExecutionResult with all step results and consolidated output.
        """
        step_results: dict[int, StepResult] = {}  # Map step_number -> result
        agents_used: set[str] = set()
        total_start = time.perf_counter()
        all_outputs: list[tuple[int, str]] = []  # (step_number, output) for ordering
        
        logger.info(
            "Executing plan",
            summary=plan.summary[:50],
            step_count=len(plan.steps),
        )
        
        # Build dependency graph
        steps_by_number: dict[int, PlanStep] = {s.step_number: s for s in plan.steps}
        remaining_steps: set[int] = {s.step_number for s in plan.steps}
        
        async with self.agent:
            while remaining_steps:
                # Find all steps that can run now (dependencies met)
                ready_steps = self._get_ready_steps(
                    remaining_steps, 
                    steps_by_number, 
                    step_results
                )
                
                if not ready_steps:
                    # Circular dependency or error - break to avoid infinite loop
                    logger.error(
                        "No ready steps but steps remain - possible circular dependency",
                        remaining=list(remaining_steps),
                    )
                    break
                
                # Execute ready steps in parallel
                logger.info(
                    "Executing parallel wave",
                    wave_steps=[s.step_number for s in ready_steps],
                    parallel_count=len(ready_steps),
                )
                
                # Create tasks for parallel execution
                tasks = []
                for step in ready_steps:
                    task = self._execute_step(
                        step=step,
                        original_query=original_query,
                        step_results=step_results,
                    )
                    tasks.append(task)
                
                # Run all ready steps concurrently
                wave_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for step, result in zip(ready_steps, wave_results):
                    if isinstance(result, Exception):
                        # Task raised an exception
                        step_result = StepResult(
                            step_number=step.step_number,
                            tool_used=step.tool.value,
                            status=StepStatus.FAILED,
                            error=str(result),
                            duration_ms=0,
                        )
                        logger.error(
                            "Step failed with exception",
                            step_number=step.step_number,
                            error=str(result),
                        )
                    else:
                        step_result = result
                        if step_result.status == StepStatus.COMPLETED:
                            agents_used.add(
                                self._tool_to_agent.get(step.tool.value, step.tool.value)
                            )
                            all_outputs.append(
                                (step.step_number, f"## Step {step.step_number}: {step.tool.value}\n\n{step_result.output}")
                            )
                    
                    step_results[step.step_number] = step_result
                    remaining_steps.discard(step.step_number)
        
        total_duration = int((time.perf_counter() - total_start) * 1000)
        
        # Sort outputs by step number for consistent ordering
        all_outputs.sort(key=lambda x: x[0])
        final_output = "\n\n---\n\n".join(output for _, output in all_outputs) if all_outputs else ""
        
        # Convert results dict to sorted list
        sorted_results = [step_results[num] for num in sorted(step_results.keys())]
        success = all(r.status == StepStatus.COMPLETED for r in sorted_results)
        
        execution_result = ExecutionResult(
            plan_summary=plan.summary,
            step_results=sorted_results,
            final_output=final_output,
            agents_used=list(agents_used),
            total_duration_ms=total_duration,
            success=success,
        )
        
        logger.info(
            "Plan execution completed",
            success=success,
            steps_completed=sum(1 for r in sorted_results if r.status == StepStatus.COMPLETED),
            total_steps=len(sorted_results),
            duration_ms=total_duration,
        )
        
        return execution_result
    
    def _get_ready_steps(
        self,
        remaining_steps: set[int],
        steps_by_number: dict[int, PlanStep],
        completed_results: dict[int, StepResult],
    ) -> list[PlanStep]:
        """
        Get steps that are ready to execute (all dependencies completed).
        
        Args:
            remaining_steps: Step numbers not yet executed.
            steps_by_number: Map of step number to PlanStep.
            completed_results: Results of already executed steps.
            
        Returns:
            List of PlanSteps ready for execution.
        """
        ready = []
        for step_num in remaining_steps:
            step = steps_by_number[step_num]
            
            # Check if all dependencies are completed successfully
            deps_met = all(
                dep_num in completed_results 
                and completed_results[dep_num].status == StepStatus.COMPLETED
                for dep_num in step.depends_on
            )
            
            if deps_met:
                ready.append(step)
        
        return ready
    
    async def _execute_step(
        self,
        step: PlanStep,
        original_query: str,
        step_results: dict[int, StepResult],
    ) -> StepResult:
        """
        Execute a single plan step.
        
        Args:
            step: The step to execute.
            original_query: The original user query for context.
            step_results: Results of previously completed steps.
            
        Returns:
            StepResult for this step.
        """
        step_start = time.perf_counter()
        
        # Gather context from dependencies
        dependent_outputs = []
        for dep_num in step.depends_on:
            dep_result = step_results.get(dep_num)
            if dep_result and dep_result.status == StepStatus.COMPLETED:
                dependent_outputs.append(dep_result.output)
        
        # Build execution prompt
        context = ""
        if dependent_outputs:
            context = "\n\nCONTEXT FROM PREVIOUS STEPS:\n" + "\n---\n".join(dependent_outputs)
        
        execution_prompt = f"""Execute this step from the plan:

ORIGINAL USER QUERY: {original_query}

STEP {step.step_number}: Use the **{step.tool.value}** tool
QUERY: {step.query}
EXPECTED OUTPUT: {step.expected_output}{context}

Call the {step.tool.value} tool with the query above."""

        settings = get_settings()
        step_timeout = settings.step_execution_timeout_seconds

        try:
            logger.debug(
                "Executing step",
                step_number=step.step_number,
                tool=step.tool.value,
                timeout_seconds=step_timeout,
            )
            
            # Execute with step-level timeout protection
            result = await asyncio.wait_for(
                self.agent.run(execution_prompt),
                timeout=step_timeout,
            )
            
            step_duration = int((time.perf_counter() - step_start) * 1000)
            
            step_result = StepResult(
                step_number=step.step_number,
                tool_used=step.tool.value,
                status=StepStatus.COMPLETED,
                output=result.text,
                duration_ms=step_duration,
            )
            
            logger.debug(
                "Step completed",
                step_number=step.step_number,
                duration_ms=step_duration,
            )
            
            return step_result
        
        except asyncio.TimeoutError:
            step_duration = int((time.perf_counter() - step_start) * 1000)
            
            step_result = StepResult(
                step_number=step.step_number,
                tool_used=step.tool.value,
                status=StepStatus.FAILED,
                error=f"Step timed out after {step_timeout}s",
                duration_ms=step_duration,
            )
            
            logger.warning(
                "Step timed out",
                step_number=step.step_number,
                timeout_seconds=step_timeout,
                duration_ms=step_duration,
            )
            
            return step_result
            
        except Exception as e:
            step_duration = int((time.perf_counter() - step_start) * 1000)
            
            step_result = StepResult(
                step_number=step.step_number,
                tool_used=step.tool.value,
                status=StepStatus.FAILED,
                error=str(e),
                duration_ms=step_duration,
            )
            
            logger.error(
                "Step failed",
                step_number=step.step_number,
                error=str(e),
            )
            
            return step_result
    
    async def execute_single_step(self, tool: str, query: str) -> str:
        """
        Execute a single tool call directly (for simple queries).
        
        Args:
            tool: Tool name ('research', 'architecture', 'code').
            query: The query to pass to the tool.
            
        Returns:
            The tool's response text.
        """
        settings = get_settings()
        execution_prompt = f"Call the {tool} tool with this query: {query}"
        
        async with self.agent:
            result = await asyncio.wait_for(
                self.agent.run(execution_prompt),
                timeout=settings.step_execution_timeout_seconds,
            )
            return result.text
