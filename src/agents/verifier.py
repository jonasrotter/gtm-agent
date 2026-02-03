"""
Verifier Agent for the Plan-Execute-Verify pattern.

Validates execution results against the original query.
Calculates quality scores and provides feedback for re-planning.
"""

from agent_framework import ChatAgent, HostedMCPTool

from src.agents.base import create_azure_chat_client, MICROSOFT_LEARN_MCP_URL
from src.agents.models import (
    ExecutionPlan,
    ExecutionResult,
    VerificationDecision,
    VerificationResult,
    VerificationScore,
)
from src.utils.logging import get_logger


logger = get_logger(__name__)


VERIFIER_INSTRUCTIONS = """You are a Verification Agent that validates execution results.

## Your Role
Evaluate whether the execution result adequately answers the original user query.
Provide objective quality scores and actionable feedback.

## Scoring Dimensions (0.0 to 1.0 each)

1. **Correctness** (40% weight)
   - Are facts accurate?
   - Is code syntactically valid?
   - Are Azure service names/features correct?

2. **Completeness** (35% weight)
   - Were all parts of the query addressed?
   - Are there missing aspects?
   - Is the response thorough enough?

3. **Consistency** (25% weight)
   - Is the response internally coherent?
   - Are there contradictions?
   - Does the flow make sense?

## Decision Rules

- **accept**: Overall score >= 0.8 (response is good enough)
- **retry**: Overall score < 0.8 but issues are fixable (provide feedback)
- **escalate**: Critical issues that require human judgment

## Verification Guidelines

1. **Be Objective**: Score based on evidence, not feelings
2. **Be Specific**: Point to exact issues, not vague concerns
3. **Be Constructive**: Provide actionable feedback for retry
4. **Use MCP**: You can search Microsoft Learn docs to fact-check claims

## CRITICAL: Required JSON Schema
Your response MUST be a JSON object matching this EXACT schema:

{
  "score": {
    "correctness": 0.9,
    "completeness": 0.85,
    "consistency": 0.95,
    "overall": 0.89
  },
  "decision": "accept",
  "issues": [],
  "feedback_for_replanning": "",
  "summary": "Brief summary of verification findings"
}

Required fields:
- score: object with correctness (float 0-1), completeness (float 0-1), consistency (float 0-1), overall (float 0-1)
  - overall = 0.4*correctness + 0.35*completeness + 0.25*consistency
- decision: MUST be one of: "accept", "retry", "escalate"
- issues: array of issue objects (can be empty [])
  - Each issue: {"category": "factual|missing|inconsistent|unclear", "description": "...", "severity": "critical|major|minor", "suggestion": "..."}
- feedback_for_replanning: string with improvement suggestions (empty "" if accept)
- summary: string explaining the verification findings

## Example Accept Response

{
  "score": {
    "correctness": 0.95,
    "completeness": 0.90,
    "consistency": 0.92,
    "overall": 0.925
  },
  "decision": "accept",
  "issues": [],
  "feedback_for_replanning": "",
  "summary": "Response accurately explains Azure Functions with complete coverage of requested aspects"
}

## Example Retry Response

{
  "score": {
    "correctness": 0.80,
    "completeness": 0.60,
    "consistency": 0.85,
    "overall": 0.74
  },
  "decision": "retry",
  "issues": [
    {"category": "missing", "description": "Missing cost optimization details", "severity": "major", "suggestion": "Add specific cost strategies"},
    {"category": "missing", "description": "No comparison with alternatives", "severity": "minor", "suggestion": "Compare with AWS Lambda"}
  ],
  "feedback_for_replanning": "Add specific cost optimization strategies and compare with AWS Lambda or other options",
  "summary": "Response is accurate but incomplete - needs more depth on cost and alternatives"
}

## Output Format
ALWAYS respond with ONLY the JSON object. No markdown code fences. No explanatory text. Just the raw JSON."""


class VerifierAgent:
    """
    Validates execution results and calculates quality scores.
    
    Optionally uses Microsoft Learn MCP for fact-checking.
    Outputs structured VerificationResult with scores and feedback.
    """
    
    # Acceptance threshold
    ACCEPTANCE_THRESHOLD = 0.8
    
    def __init__(self, enable_fact_check: bool = True):
        """
        Initialize VerifierAgent.
        
        Args:
            enable_fact_check: If True, enables MCP tool for fact-checking against docs.
        """
        tools = []
        if enable_fact_check:
            tools.append(
                HostedMCPTool(
                    name="microsoft_learn",
                    url=MICROSOFT_LEARN_MCP_URL,
                    description="Search Microsoft Learn docs to fact-check Azure claims",
                    approval_mode="never_require",
                )
            )
        
        self.agent = ChatAgent(
            chat_client=create_azure_chat_client(),
            name="Verifier",
            description="Validates execution results and calculates quality scores",
            instructions=VERIFIER_INSTRUCTIONS,
            tools=tools if tools else None,
        )
        
        self._fact_check_enabled = enable_fact_check
        
        logger.info(
            "VerifierAgent initialized",
            fact_check_enabled=enable_fact_check,
        )
    
    async def verify(
        self,
        original_query: str,
        plan: ExecutionPlan,
        result: ExecutionResult,
        iteration: int = 1,
    ) -> VerificationResult:
        """
        Verify an execution result against the original query.
        
        Args:
            original_query: The user's original question or request.
            plan: The execution plan that was used.
            result: The execution result to verify.
            iteration: Current iteration number (1-indexed).
            
        Returns:
            VerificationResult with scores, issues, and decision.
        """
        verification_prompt = f"""Verify this execution result against the original query.

## ORIGINAL USER QUERY
{original_query}

## EXECUTION PLAN USED
Summary: {plan.summary}
Steps: {len(plan.steps)}
Complexity: {plan.estimated_complexity}

## EXECUTION RESULT
Success: {result.success}
Agents Used: {', '.join(result.agents_used)}

### Output:
{result.final_output}

## YOUR TASK
1. Evaluate the result against the query
2. Score each dimension (correctness, completeness, consistency)
3. Calculate overall score: 0.4*correctness + 0.35*completeness + 0.25*consistency
4. Identify specific issues (if any)
5. Make a decision: accept (score >= 0.8), retry, or escalate
6. If retry, provide specific feedback for re-planning

This is iteration {iteration}. Be rigorous but fair.

Respond with ONLY a valid VerificationResult JSON object. No additional text before or after the JSON."""

        logger.debug(
            "Verifying execution result",
            query=original_query[:50],
            iteration=iteration,
        )
        
        async with self.agent:
            response = await self.agent.run(
                verification_prompt,
                options={"response_format": VerificationResult},
            )
            
            if response.value and isinstance(response.value, VerificationResult):
                verification = response.value
            else:
                # Fallback: parse from text with robust JSON extraction
                verification = self._parse_verification_from_text(response.text)
            
            # Ensure overall score is correctly calculated
            score = verification.score
            expected_overall = (
                0.4 * score.correctness +
                0.35 * score.completeness +
                0.25 * score.consistency
            )
            
            # Round to avoid floating point issues
            if abs(score.overall - expected_overall) > 0.01:
                verification.score.overall = round(expected_overall, 2)
            
            # Override decision based on threshold if needed
            if verification.score.overall >= self.ACCEPTANCE_THRESHOLD:
                verification.decision = VerificationDecision.ACCEPT
            elif verification.decision == VerificationDecision.ACCEPT:
                # Score too low for accept, change to retry
                verification.decision = VerificationDecision.RETRY
            
            logger.info(
                "Verification completed",
                overall_score=verification.score.overall,
                decision=verification.decision.value,
                issue_count=len(verification.issues),
                iteration=iteration,
            )
            
            return verification
    
    def _parse_verification_from_text(self, text: str) -> VerificationResult:
        """
        Parse VerificationResult from LLM text response with robust JSON extraction.
        """
        import json
        import re
        
        logger.debug("Parsing verification from text", text_preview=text[:500])
        
        # Try to extract JSON from markdown code blocks first
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
        if json_match:
            text = json_match.group(1).strip()
        
        # Find the first { and match to its closing }
        start_idx = text.find('{')
        if start_idx == -1:
            logger.warning("No JSON object found in verifier response", text=text[:200])
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
        logger.debug("Extracted JSON for verification", json_preview=json_str[:300])
        
        data = json.loads(json_str)
        logger.debug("Parsed verification data", data_keys=list(data.keys()))
        
        # Normalize schema to handle LLM variations
        normalized = self._normalize_verification_schema(data)
        logger.debug("Normalized verification data", score=normalized.get("score"))
        
        return VerificationResult(**normalized)
    
    def _normalize_verification_schema(self, data: dict) -> dict:
        """
        Normalize LLM output to match VerificationResult schema.
        
        Maps common alternative field names to expected schema.
        """
        normalized = {}
        
        def safe_float(val, default=0.5) -> float:
            """Safely convert value to float, handling nested dicts."""
            if isinstance(val, dict):
                # Handle nested structures like {"value": 0.8} or {"score": 0.8}
                return float(val.get("value", val.get("score", val.get("rating", default))))
            try:
                return float(val) if val is not None else default
            except (TypeError, ValueError):
                return default
        
        # Handle score object - normalize to VerificationScore format
        # LLM may use "score" or "scores"
        score_data = data.get("score", data.get("scores", {}))
        
        if isinstance(score_data, dict) and score_data:
            correctness = safe_float(score_data.get("correctness", score_data.get("accuracy", 0.5)))
            completeness = safe_float(score_data.get("completeness", score_data.get("coverage", 0.5)))
            consistency = safe_float(score_data.get("consistency", score_data.get("coherence", 0.5)))
            # Overall might be in score_data or at root level
            overall = safe_float(score_data.get("overall", 
                data.get("overall_score", data.get("overall",
                    0.4 * correctness + 0.35 * completeness + 0.25 * consistency))))
            normalized["score"] = {
                "correctness": correctness,
                "completeness": completeness,
                "consistency": consistency,
                "overall": overall,
            }
        elif isinstance(score_data, (int, float)):
            # Single score provided - distribute equally
            val = float(score_data)
            normalized["score"] = {
                "correctness": val,
                "completeness": val,
                "consistency": val,
                "overall": val,
            }
        else:
            # Look for individual score fields at top level or overall_score
            correctness = safe_float(data.get("correctness", data.get("accuracy", 0.5)))
            completeness = safe_float(data.get("completeness", data.get("coverage", 0.5)))
            consistency = safe_float(data.get("consistency", data.get("coherence", 0.5)))
            overall = safe_float(data.get("overall_score", data.get("overall", data.get("total_score",
                0.4 * correctness + 0.35 * completeness + 0.25 * consistency))))
            normalized["score"] = {
                "correctness": correctness,
                "completeness": completeness,
                "consistency": consistency,
                "overall": overall,
            }
        
        # Handle decision field
        decision_raw = str(data.get("decision", data.get("verdict", data.get("result", "retry")))).lower()
        if "accept" in decision_raw or "pass" in decision_raw or "approved" in decision_raw:
            normalized["decision"] = "accept"
        elif "escalate" in decision_raw or "human" in decision_raw:
            normalized["decision"] = "escalate"
        else:
            normalized["decision"] = "retry"
        
        # Handle issues field - normalize to VerificationIssue format
        raw_issues = data.get("issues", data.get("problems", data.get("concerns", [])))
        normalized_issues = []
        
        if isinstance(raw_issues, list):
            for issue in raw_issues:
                if isinstance(issue, dict):
                    # Already structured
                    normalized_issues.append({
                        "category": issue.get("category", "general"),
                        "description": issue.get("description", str(issue)),
                        "severity": issue.get("severity", "minor"),
                        "suggestion": issue.get("suggestion", issue.get("fix", "")),
                    })
                elif isinstance(issue, str) and issue.strip():
                    # Convert string to structured issue
                    normalized_issues.append({
                        "category": "general",
                        "description": issue,
                        "severity": "minor",
                        "suggestion": "",
                    })
        elif isinstance(raw_issues, str) and raw_issues.strip():
            normalized_issues.append({
                "category": "general",
                "description": raw_issues,
                "severity": "minor",
                "suggestion": "",
            })
        
        normalized["issues"] = normalized_issues
        
        # Handle feedback_for_replanning field
        normalized["feedback_for_replanning"] = str(
            data.get("feedback_for_replanning", 
            data.get("retry_feedback",
            data.get("feedback", 
            data.get("suggestions", 
            data.get("recommendation", "")))))
        )
        
        # Handle summary field - LLM may use "evaluation" or other names
        normalized["summary"] = str(
            data.get("summary",
            data.get("evaluation",
            data.get("rationale", 
            data.get("explanation", 
            data.get("reason", "Verification completed")))))
        )
        
        return normalized
    
    async def quick_verify(self, query: str, response: str) -> tuple[float, bool]:
        """
        Quick verification for simple responses (no full structured output).
        
        Args:
            query: The user's query.
            response: The response to verify.
            
        Returns:
            Tuple of (score, is_acceptable).
        """
        quick_prompt = f"""Rate this response on a scale of 0.0 to 1.0.

Query: {query}

Response: {response[:2000]}

Consider: correctness, completeness, and consistency.
Respond with just a number between 0.0 and 1.0."""

        async with self.agent:
            result = await self.agent.run(quick_prompt)
            
            try:
                score = float(result.text.strip())
                score = max(0.0, min(1.0, score))  # Clamp to valid range
            except ValueError:
                score = 0.5  # Default if parsing fails
            
            return score, score >= self.ACCEPTANCE_THRESHOLD
