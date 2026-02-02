"""
Planner Agent for the Plan-Execute-Verify pattern.

Creates structured execution plans from user queries.
No tools - pure reasoning agent that outputs JSON plans.
"""

from agent_framework import ChatAgent

from src.agents.base import create_azure_chat_client
from src.agents.models import ExecutionPlan, ToolName
from src.utils.logging import get_logger


logger = get_logger(__name__)


PLANNER_INSTRUCTIONS = """You are a Planning Agent that creates structured execution plans.

## Your Role
Analyze user queries and break them down into discrete, actionable steps that can be executed by specialized tools.

## Available Tools
You can plan steps using these tools:
1. **research** - Search Azure documentation, find information, get explanations with source citations
2. **architecture** - Get Azure architecture guidance, best practices, WAF pillar recommendations
3. **code** - Generate code, Azure CLI commands, scripts, deployment templates, test plans

## Planning Guidelines

1. **Understand Intent**: Identify what the user truly needs
2. **Break Down Complexity**: Split complex queries into logical steps
3. **Order Dependencies**: Ensure steps that depend on others come after their dependencies
4. **Be Specific**: Each step should have a clear, focused query
5. **Minimize Steps**: Use the fewest steps necessary (prefer quality over quantity)

## CRITICAL: Step Budget Rules (MUST FOLLOW)

You MUST respect these step limits based on query type:

| Query Pattern | Max Steps | Primary Tool | Examples |
|---------------|-----------|--------------|----------|
| "What is X?" / "Explain X" | **1** | research | "What is Azure Blob Storage?", "Explain Functions triggers" |
| "How do I X?" / "Steps to X" | **2** | research + code | "How do I create a storage account?" |
| "Best practices for X" | **2** | architecture | "Best practices for App Service security" |
| "Generate/Write code for X" | **1** | code | "Write Azure CLI to create RG", "Generate Bicep template" |
| Design + implement requests | **3-4** | arch + code | "Design architecture and generate Bicep" |

### Query Classification Rules:

**FACTUAL (1 step max, tool: research)**
- Questions starting with "What is", "What are", "Explain", "Describe", "Define"
- Simple informational lookups
- DO NOT add architecture or code steps for factual questions

**HOWTO (2 steps max)**
- Questions starting with "How do I", "How to", "Steps to"
- May combine research + code if procedural

**ARCHITECTURE (2 steps max, tool: architecture)**
- Questions about "Best practices", "Design", "Recommendations"
- Use architecture tool, optionally with research first

**CODE (1 step max, tool: code)**
- Requests starting with "Generate", "Write", "Create script/template"
- Explicit code/CLI/Bicep/Terraform requests
- DO NOT add research steps for pure code generation

**COMPLEX (3-4 steps max)**
- Compound requests with "and", "then", "also"
- Multiple question marks
- Design + implement combinations

### Step Budget Violations to Avoid:
❌ Adding research steps to simple "What is X?" queries (should be 1 step)
❌ Adding verification steps (verification is handled externally)
❌ Creating redundant steps that could be combined
❌ Using more than 1 step for pure code generation requests

## Step Dependency Rules
- If step B needs output from step A, add A's step_number to B's depends_on list
- Independent steps can run in parallel (empty depends_on)
- Research often comes before architecture or code steps

## CRITICAL: Required JSON Schema
Your response MUST be a JSON object matching this EXACT schema:

{
  "summary": "Brief summary of the plan",
  "steps": [
    {
      "step_number": 1,
      "tool": "research",
      "query": "The specific query for this step",
      "expected_output": "What this step should produce",
      "depends_on": []
    }
  ],
  "estimated_complexity": "simple|moderate|complex",
  "rationale": "Why this plan structure was chosen"
}

Required fields for each step:
- step_number: integer starting from 1
- tool: MUST be one of: "research", "architecture", "code"
- query: string with the specific instruction
- expected_output: string describing expected result
- depends_on: array of step numbers (can be empty [])

Required fields at plan level:
- summary: string
- steps: array of step objects
- estimated_complexity: "simple", "moderate", or "complex"
- rationale: string

## Example Response

{
  "summary": "Research Azure Functions basics",
  "steps": [
    {
      "step_number": 1,
      "tool": "research",
      "query": "What is Azure Functions and its key features?",
      "expected_output": "Overview of Azure Functions with main capabilities",
      "depends_on": []
    }
  ],
  "estimated_complexity": "simple",
  "rationale": "Single research step sufficient for basic informational query"
}

## Output Format
ALWAYS respond with ONLY the JSON object. No markdown code fences. No explanatory text. Just the raw JSON."""


class PlannerAgent:
    """
    Creates structured execution plans from user queries.
    
    Uses structured output (response_format) to ensure valid JSON plans.
    No external tools - relies purely on LLM reasoning.
    """
    
    # List of available tools for planning context
    AVAILABLE_TOOLS = [tool.value for tool in ToolName]
    
    def __init__(self):
        """Initialize PlannerAgent with structured output configuration."""
        self.agent = ChatAgent(
            chat_client=create_azure_chat_client(),
            name="Planner",
            description="Creates structured execution plans from user queries",
            instructions=PLANNER_INSTRUCTIONS,
            # No tools - pure reasoning agent
        )
        
        logger.info(
            "PlannerAgent initialized",
            available_tools=self.AVAILABLE_TOOLS,
        )
    
    async def create_plan(self, query: str, max_steps: int = 4, query_category: str = "complex") -> ExecutionPlan:
        """
        Create an execution plan for a user query.
        
        Args:
            query: The user's question or request.
            max_steps: Maximum number of steps allowed (based on query category).
            query_category: The classified category (factual, howto, architecture, code, complex).
            
        Returns:
            ExecutionPlan with ordered steps and metadata.
        """
        # Build step budget guidance based on category
        step_guidance = f"""
CRITICAL CONSTRAINT: This query is classified as "{query_category}".
Maximum allowed steps: {max_steps}
DO NOT create more than {max_steps} step(s).

Category-specific rules:
- factual: 1 step with research tool only
- code: 1 step with code tool only
- howto: 1-2 steps (research or research+code)
- architecture: 1-2 steps (architecture or research+architecture)
- complex: up to {max_steps} steps for multi-part requests
"""

        # Augment query with available tools context and step budget
        planning_prompt = f"""Create an execution plan for this user query:

USER QUERY: {query}

{step_guidance}

AVAILABLE TOOLS: {', '.join(self.AVAILABLE_TOOLS)}

Respond with ONLY a valid ExecutionPlan JSON object. No additional text before or after the JSON."""

        logger.debug("Creating execution plan", query=query[:100], max_steps=max_steps, category=query_category)
        
        async with self.agent:
            result = await self.agent.run(
                planning_prompt,
                options={"response_format": ExecutionPlan},
            )
            
            # Extract structured output
            if result.value and isinstance(result.value, ExecutionPlan):
                plan = result.value
            else:
                # Fallback: parse from text if structured output failed
                plan = self._parse_plan_from_text(result.text)
            
            logger.info(
                "Execution plan created",
                summary=plan.summary[:50],
                step_count=len(plan.steps),
                complexity=plan.estimated_complexity,
            )
            
            return plan
    
    def _parse_plan_from_text(self, text: str) -> ExecutionPlan:
        """
        Parse ExecutionPlan from LLM text response with robust JSON extraction.
        
        Handles:
        - Markdown code blocks
        - Extra text before/after JSON
        - Nested JSON objects
        - Schema normalization (LLM may use different field names)
        """
        import json
        import re
        
        # Try to extract JSON from markdown code blocks first
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if json_match:
            text = json_match.group(1).strip()
        
        # Find the first { and match to its closing }
        start_idx = text.find('{')
        if start_idx == -1:
            raise ValueError("No JSON object found in response")
        
        # Track brace depth to find matching closing brace
        depth = 0
        end_idx = start_idx
        for i, char in enumerate(text[start_idx:], start=start_idx):
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end_idx = i
                    break
        
        json_str = text[start_idx:end_idx + 1]
        plan_data = json.loads(json_str)
        
        # Normalize schema: handle alternative field names the LLM might use
        normalized = self._normalize_plan_schema(plan_data)
        
        return ExecutionPlan(**normalized)
    
    def _normalize_plan_schema(self, data: dict) -> dict:
        """
        Normalize LLM output to match ExecutionPlan schema.
        
        Maps common alternative field names to expected schema.
        """
        # Top-level field mappings
        field_mappings = {
            "description": "summary",
            "title": "summary", 
            "plan_summary": "summary",
            "overview": "summary",
            "complexity": "estimated_complexity",
            "explanation": "rationale",
            "reasoning": "rationale",
            "user_query": "query",  # Ignore user_query as it's input, not output
        }
        
        # Normalize top-level fields
        normalized = {}
        for key, value in data.items():
            normalized_key = field_mappings.get(key, key)
            if normalized_key not in ["query", "user_query"]:  # Skip input fields
                normalized[normalized_key] = value
        
        # Get original query for default summary
        original_query = data.get("query", data.get("user_query", ""))
        
        # Ensure required top-level fields exist
        if "summary" not in normalized:
            # Try to derive from query if present
            normalized["summary"] = f"Execute plan for: {original_query}" if original_query else "Execution plan"
        
        # Handle steps - check various field names
        steps_data = normalized.get("steps", data.get("plan_steps", data.get("actions", data.get("tasks", []))))
        
        if not steps_data or not isinstance(steps_data, list):
            # Create a default single research step if no steps provided
            logger.warning("No steps found in LLM response, creating default research step")
            steps_data = [{
                "step_number": 1,
                "tool": "research",
                "query": original_query if original_query else "Research the topic",
                "expected_output": "Information about the query",
                "depends_on": [],
            }]
        
        if "estimated_complexity" not in normalized:
            # Derive from step count
            step_count = len(steps_data)
            if step_count <= 2:
                normalized["estimated_complexity"] = "simple"
            elif step_count <= 4:
                normalized["estimated_complexity"] = "moderate"
            else:
                normalized["estimated_complexity"] = "complex"
        
        if "rationale" not in normalized:
            normalized["rationale"] = "Plan created based on query analysis"
        
        # Normalize steps
        normalized["steps"] = [
            self._normalize_step_schema(step, idx + 1) 
            for idx, step in enumerate(steps_data)
        ]
        
        return normalized
    
    def _normalize_step_schema(self, step: dict, default_step_num: int) -> dict:
        """Normalize a single step to match PlanStep schema."""
        # Step field mappings
        step_mappings = {
            "id": None,  # Will use step_number
            "number": "step_number",
            "step": "step_number",
            "action": "query",
            "instruction": "query",
            "task": "query",
            "description": "query",
            "expected": "expected_output",
            "output": "expected_output",
            "deliverables": "expected_output",
            "dependencies": "depends_on",
            "requires": "depends_on",
        }
        
        normalized_step = {}
        for key, value in step.items():
            normalized_key = step_mappings.get(key, key)
            if normalized_key is not None:
                normalized_step[normalized_key] = value
        
        # Ensure step_number exists
        if "step_number" not in normalized_step:
            normalized_step["step_number"] = default_step_num
        
        # Ensure tool exists and is valid
        if "tool" in normalized_step:
            tool_val = str(normalized_step["tool"]).lower()
            valid_tools = {"research", "architecture", "code"}
            if tool_val not in valid_tools:
                # Default to research for unknown tools
                normalized_step["tool"] = "research"
            else:
                normalized_step["tool"] = tool_val
        else:
            normalized_step["tool"] = "research"
        
        # Ensure query exists
        if "query" not in normalized_step:
            normalized_step["query"] = step.get("description", step.get("action", "Execute step"))
        
        # Ensure expected_output exists
        if "expected_output" not in normalized_step:
            normalized_step["expected_output"] = "Step output"
        
        # Handle depends_on - could be list of step numbers or IDs
        if "depends_on" not in normalized_step:
            normalized_step["depends_on"] = []
        else:
            deps = normalized_step["depends_on"]
            if isinstance(deps, list):
                # Convert string IDs like "s1" to integers
                normalized_deps = []
                for dep in deps:
                    if isinstance(dep, int):
                        normalized_deps.append(dep)
                    elif isinstance(dep, str):
                        # Try to extract number from strings like "s1", "step1", etc.
                        import re
                        match = re.search(r'\d+', dep)
                        if match:
                            normalized_deps.append(int(match.group()))
                normalized_step["depends_on"] = normalized_deps
            else:
                normalized_step["depends_on"] = []
        
        return normalized_step
    
    async def refine_plan(self, query: str, feedback: str, previous_plan: ExecutionPlan, max_steps: int = 4, query_category: str = "complex") -> ExecutionPlan:
        """
        Refine an existing plan based on verification feedback.
        
        Args:
            query: The original user query.
            feedback: Feedback from the verifier on what to improve.
            previous_plan: The plan that was executed and needs refinement.
            max_steps: Maximum number of steps allowed.
            query_category: The classified category.
            
        Returns:
            Refined ExecutionPlan addressing the feedback.
        """
        refinement_prompt = f"""Refine the execution plan based on verification feedback.

ORIGINAL QUERY: {query}

CRITICAL CONSTRAINT: Maximum {max_steps} steps allowed (query type: {query_category}).
DO NOT exceed {max_steps} steps in the refined plan.

PREVIOUS PLAN:
{previous_plan.model_dump_json(indent=2)}

VERIFIER FEEDBACK:
{feedback}

Create an improved ExecutionPlan that addresses the feedback. You may:
- Add new steps to fill gaps (but stay within {max_steps} step limit)
- Modify existing step queries for better results
- Reorder steps for better flow
- Remove unnecessary steps

## REQUIRED JSON SCHEMA
Respond with a JSON object matching this EXACT schema:

{{
  "summary": "Brief summary of the plan",
  "steps": [
    {{
      "step_number": 1,
      "tool": "research",
      "query": "The specific query for this step",
      "expected_output": "What this step should produce",
      "depends_on": []
    }}
  ],
  "estimated_complexity": "simple|moderate|complex",
  "rationale": "Why this plan structure was chosen"
}}

AVAILABLE TOOLS: {', '.join(self.AVAILABLE_TOOLS)}

Respond with ONLY the JSON object. No markdown code fences. No explanatory text."""

        logger.debug("Refining execution plan", feedback=feedback[:100])
        
        async with self.agent:
            result = await self.agent.run(
                refinement_prompt,
                options={"response_format": ExecutionPlan},
            )
            
            if result.value and isinstance(result.value, ExecutionPlan):
                plan = result.value
            else:
                plan = self._parse_plan_from_text(result.text)
            
            logger.info(
                "Execution plan refined",
                summary=plan.summary[:50],
                step_count=len(plan.steps),
            )
            
            return plan
