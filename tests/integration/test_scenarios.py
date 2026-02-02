"""
Integration Test Scenarios for GTM-Agent System

This module defines comprehensive test scenarios to evaluate the agent system's:
1. Query Classification accuracy
2. Tool invocation correctness
3. Response quality (via verification scores)
4. Performance characteristics
5. Error handling and edge cases
6. Multi-agent coordination

Evaluation Criteria:
- Duration: Time to complete (target varies by category)
- Iterations: Should match category config (FACTUAL=1, HOWTO=1, ARCH=2, COMPLEX=4)
- Verification Score: Target >= 0.75 for acceptance
- Tool Usage: Correct tools should be invoked
- Response Quality: Content should be relevant and complete
"""

import pytest
import httpx
import time
from dataclasses import dataclass
from typing import Any


# =============================================================================
# Test Configuration
# =============================================================================

BASE_URL = "http://localhost:8000"
DEFAULT_TIMEOUT = 600  # 10 minutes max

# Target metrics by category
CATEGORY_TARGETS = {
    "FACTUAL": {
        "max_duration_seconds": 60,
        "max_iterations": 1,
        "min_score": None,  # Fast path skips verification
        "expected_tools": ["research"],
    },
    "HOWTO": {
        "max_duration_seconds": 300,
        "max_iterations": 1,
        "min_score": 0.70,
        "expected_tools": ["research", "code"],
    },
    "ARCHITECTURE": {
        "max_duration_seconds": 300,
        "max_iterations": 2,
        "min_score": 0.70,
        "expected_tools": ["architecture", "research"],
    },
    "CODE": {
        "max_duration_seconds": 300,
        "max_iterations": 1,
        "min_score": 0.70,
        "expected_tools": ["code"],
    },
    "COMPLEX": {
        "max_duration_seconds": 600,
        "max_iterations": 4,
        "min_score": 0.65,
        "expected_tools": ["research", "architecture", "code"],
    },
}


@dataclass
class TestResult:
    """Container for test results with evaluation metrics."""
    query: str
    category: str
    duration_seconds: float
    iterations_used: int
    verification_score: float | None
    agents_used: list[str]
    steps: list[dict]
    response_preview: str
    success: bool
    error: str | None = None
    
    def evaluate(self, targets: dict) -> dict[str, bool]:
        """Evaluate result against target metrics."""
        evaluations = {}
        
        # Duration check
        if targets.get("max_duration_seconds"):
            evaluations["duration_ok"] = self.duration_seconds <= targets["max_duration_seconds"]
        
        # Iterations check
        if targets.get("max_iterations"):
            evaluations["iterations_ok"] = self.iterations_used <= targets["max_iterations"]
        
        # Score check (if applicable)
        if targets.get("min_score") and self.verification_score is not None:
            evaluations["score_ok"] = self.verification_score >= targets["min_score"]
        
        # Tool usage check (at least one expected tool used)
        if targets.get("expected_tools"):
            used_tools = {s.get("tool") for s in self.steps if s.get("tool")}
            evaluations["tools_ok"] = bool(used_tools & set(targets["expected_tools"]))
        
        return evaluations


# =============================================================================
# Test Scenarios
# =============================================================================

# Category: FACTUAL - Simple fact-based queries
FACTUAL_TESTS = [
    {
        "name": "factual_service_definition",
        "query": "What is Azure Blob Storage?",
        "description": "Basic service definition lookup",
        "expected_category": "FACTUAL",
    },
    {
        "name": "factual_pricing_tiers",
        "query": "What are the pricing tiers for Azure App Service?",
        "description": "Pricing information lookup",
        "expected_category": "FACTUAL",
    },
    {
        "name": "factual_region_availability",
        "query": "What regions is Azure OpenAI available in?",
        "description": "Service availability lookup",
        "expected_category": "FACTUAL",
    },
    {
        "name": "factual_comparison",
        "query": "What is the difference between Azure Functions and Logic Apps?",
        "description": "Service comparison (should be fast path)",
        "expected_category": "FACTUAL",
    },
]

# Category: HOWTO - Step-by-step guidance
HOWTO_TESTS = [
    {
        "name": "howto_deploy_function",
        "query": "How do I deploy an Azure Function using GitHub Actions?",
        "description": "CI/CD deployment steps",
        "expected_category": "HOWTO",
    },
    {
        "name": "howto_configure_vnet",
        "query": "How do I configure VNet integration for Azure App Service?",
        "description": "Network configuration steps",
        "expected_category": "HOWTO",
    },
    {
        "name": "howto_enable_monitoring",
        "query": "How do I enable Application Insights for my Azure Function?",
        "description": "Monitoring setup steps",
        "expected_category": "HOWTO",
    },
    {
        "name": "howto_setup_managed_identity",
        "query": "How do I set up managed identity for Azure App Service to access Key Vault?",
        "description": "Identity and access configuration",
        "expected_category": "HOWTO",
    },
]

# Category: ARCHITECTURE - Best practices and design guidance
ARCHITECTURE_TESTS = [
    {
        "name": "arch_security_best_practices",
        "query": "What are the best practices for Azure App Service security?",
        "description": "Security architecture guidance",
        "expected_category": "ARCHITECTURE",
    },
    {
        "name": "arch_high_availability",
        "query": "How do I design a highly available web application on Azure?",
        "description": "HA architecture patterns",
        "expected_category": "ARCHITECTURE",
    },
    {
        "name": "arch_cost_optimization",
        "query": "What are the cost optimization strategies for Azure Kubernetes Service?",
        "description": "Cost optimization guidance",
        "expected_category": "ARCHITECTURE",
    },
    {
        "name": "arch_waf_pillar",
        "query": "How do I implement the reliability pillar of the Well-Architected Framework for my Azure solution?",
        "description": "WAF pillar implementation",
        "expected_category": "ARCHITECTURE",
    },
]

# Category: CODE - Code generation requests
CODE_TESTS = [
    {
        "name": "code_python_blob",
        "query": "Write Python code to upload a file to Azure Blob Storage using the SDK",
        "description": "SDK code generation",
        "expected_category": "CODE",
    },
    {
        "name": "code_bicep_webapp",
        "query": "Generate Bicep code to deploy an Azure App Service with a SQL Database",
        "description": "IaC code generation",
        "expected_category": "CODE",
    },
    {
        "name": "code_cli_commands",
        "query": "Give me the Azure CLI commands to create a storage account with private endpoint",
        "description": "CLI command generation",
        "expected_category": "CODE",
    },
    {
        "name": "code_terraform_aks",
        "query": "Create Terraform code to deploy an AKS cluster with managed identity",
        "description": "Terraform code generation",
        "expected_category": "CODE",
    },
]

# Category: COMPLEX - Multi-faceted queries requiring multiple agents
COMPLEX_TESTS = [
    {
        "name": "complex_full_architecture",
        "query": "Design a microservices architecture for an e-commerce platform on Azure with API Gateway, message queues, and database recommendations. Include sample code for the API Gateway configuration.",
        "description": "Full architecture with code sample",
        "expected_category": "COMPLEX",
    },
    {
        "name": "complex_migration",
        "query": "Help me plan a migration from on-premises SQL Server to Azure, including best practices, step-by-step approach, and the Azure CLI commands needed",
        "description": "Migration planning with code",
        "expected_category": "COMPLEX",
    },
    {
        "name": "complex_security_implementation",
        "query": "I need to implement zero-trust security for my Azure environment. Provide the architecture, best practices, and Bicep templates for the core infrastructure.",
        "description": "Security architecture with IaC",
        "expected_category": "COMPLEX",
    },
]

# Edge Cases - Testing system robustness
EDGE_CASE_TESTS = [
    {
        "name": "edge_vague_query",
        "query": "Help me with Azure",
        "description": "Very vague query - should ask clarifying questions",
        "expected_category": "COMPLEX",  # Defaults to complex due to ambiguity
    },
    {
        "name": "edge_non_azure",
        "query": "How do I deploy to AWS Lambda?",
        "description": "Non-Azure query - should handle gracefully",
        "expected_category": "HOWTO",
    },
    {
        "name": "edge_mixed_topics",
        "query": "Compare Azure Functions vs AWS Lambda and show me how to deploy to both",
        "description": "Mixed cloud provider query",
        "expected_category": "COMPLEX",
    },
    {
        "name": "edge_very_specific",
        "query": "What is the exact maximum blob size in hot tier for Azure Storage accounts created after 2024?",
        "description": "Very specific factual query",
        "expected_category": "FACTUAL",
    },
    {
        "name": "edge_long_query",
        "query": """I have an existing application that uses Azure App Service with a Basic tier, 
        Azure SQL Database with DTU model, and Azure Blob Storage. The application is experiencing 
        performance issues during peak hours. I need to understand what monitoring tools to use, 
        how to diagnose the bottleneck, what scaling options are available, and if I should consider 
        migrating to a different architecture like Azure Container Apps or AKS. Please also provide 
        estimated costs for different scenarios.""",
        "description": "Long multi-part query",
        "expected_category": "COMPLEX",
    },
]

# Performance Boundary Tests
PERFORMANCE_TESTS = [
    {
        "name": "perf_simple_fast",
        "query": "What is Azure?",
        "description": "Minimal query - should be very fast",
        "expected_category": "FACTUAL",
        "max_duration": 30,
    },
    {
        "name": "perf_medium_complexity",
        "query": "How do I configure Azure Front Door with custom domains and WAF rules?",
        "description": "Medium complexity - should complete in reasonable time",
        "expected_category": "HOWTO",
        "max_duration": 180,
    },
]


# =============================================================================
# Test Execution Functions
# =============================================================================

async def execute_query(query: str, timeout: int = DEFAULT_TIMEOUT) -> TestResult:
    """Execute a query against the agent API and return structured results."""
    start_time = time.perf_counter()
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/agent/query",
                json={"content": query},
            )
            response.raise_for_status()
            data = response.json()
            
            duration = time.perf_counter() - start_time
            
            # Parse execution steps
            steps = []
            if data.get("execution_steps"):
                for step in data["execution_steps"]:
                    steps.append({
                        "step_number": step.get("step_number"),
                        "tool": step.get("tool"),
                        "status": step.get("status"),
                    })
            
            # Parse agents used
            agents = []
            if data.get("agent_used"):
                agents = [a.strip() for a in data["agent_used"].split(",")]
            
            return TestResult(
                query=query,
                category="UNKNOWN",  # Will be determined by classifier
                duration_seconds=duration,
                iterations_used=data.get("iterations_used", 0),
                verification_score=data.get("verification_score"),
                agents_used=agents,
                steps=steps,
                response_preview=data.get("content", "")[:500],
                success=True,
            )
            
        except Exception as e:
            duration = time.perf_counter() - start_time
            return TestResult(
                query=query,
                category="UNKNOWN",
                duration_seconds=duration,
                iterations_used=0,
                verification_score=None,
                agents_used=[],
                steps=[],
                response_preview="",
                success=False,
                error=str(e),
            )


def print_result(test_name: str, result: TestResult, targets: dict) -> None:
    """Print formatted test result with evaluation."""
    evaluations = result.evaluate(targets)
    
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Query: {result.query[:80]}...")
    print(f"Duration: {result.duration_seconds:.1f}s")
    print(f"Iterations: {result.iterations_used}")
    print(f"Score: {result.verification_score}")
    print(f"Agents: {', '.join(result.agents_used)}")
    print(f"Steps: {len(result.steps)}")
    
    print("\nEvaluations:")
    for key, passed in evaluations.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {key}")
    
    if result.error:
        print(f"\n❌ ERROR: {result.error}")
    
    print(f"\nResponse Preview: {result.response_preview[:200]}...")


# =============================================================================
# Pytest Test Classes
# =============================================================================

@pytest.mark.integration
class TestFactualQueries:
    """Test FACTUAL category queries - should use fast path."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", FACTUAL_TESTS, ids=lambda t: t["name"])
    async def test_factual_query(self, test_case):
        result = await execute_query(test_case["query"])
        targets = CATEGORY_TARGETS["FACTUAL"]
        
        assert result.success, f"Query failed: {result.error}"
        assert result.duration_seconds <= targets["max_duration_seconds"], \
            f"Too slow: {result.duration_seconds}s > {targets['max_duration_seconds']}s"
        assert result.iterations_used <= targets["max_iterations"], \
            f"Too many iterations: {result.iterations_used}"


@pytest.mark.integration
class TestHowToQueries:
    """Test HOWTO category queries - step-by-step guidance."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", HOWTO_TESTS, ids=lambda t: t["name"])
    async def test_howto_query(self, test_case):
        result = await execute_query(test_case["query"])
        targets = CATEGORY_TARGETS["HOWTO"]
        
        assert result.success, f"Query failed: {result.error}"
        if result.verification_score is not None:
            assert result.verification_score >= targets["min_score"], \
                f"Score too low: {result.verification_score} < {targets['min_score']}"


@pytest.mark.integration
class TestArchitectureQueries:
    """Test ARCHITECTURE category queries - best practices and design."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", ARCHITECTURE_TESTS, ids=lambda t: t["name"])
    async def test_architecture_query(self, test_case):
        result = await execute_query(test_case["query"])
        targets = CATEGORY_TARGETS["ARCHITECTURE"]
        
        assert result.success, f"Query failed: {result.error}"
        if result.verification_score is not None:
            assert result.verification_score >= targets["min_score"], \
                f"Score too low: {result.verification_score} < {targets['min_score']}"


@pytest.mark.integration
class TestCodeQueries:
    """Test CODE category queries - code generation."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", CODE_TESTS, ids=lambda t: t["name"])
    async def test_code_query(self, test_case):
        result = await execute_query(test_case["query"])
        targets = CATEGORY_TARGETS["CODE"]
        
        assert result.success, f"Query failed: {result.error}"


@pytest.mark.integration
class TestComplexQueries:
    """Test COMPLEX category queries - multi-agent coordination."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", COMPLEX_TESTS, ids=lambda t: t["name"])
    async def test_complex_query(self, test_case):
        result = await execute_query(test_case["query"], timeout=900)
        targets = CATEGORY_TARGETS["COMPLEX"]
        
        assert result.success, f"Query failed: {result.error}"


@pytest.mark.integration
class TestEdgeCases:
    """Test edge cases and error handling."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("test_case", EDGE_CASE_TESTS, ids=lambda t: t["name"])
    async def test_edge_case(self, test_case):
        result = await execute_query(test_case["query"])
        
        # Edge cases should not crash
        assert result.success, f"Query failed: {result.error}"
        # Should return some response
        assert len(result.response_preview) > 0, "Empty response"


# =============================================================================
# Manual Test Runner (for interactive testing)
# =============================================================================

async def run_all_tests():
    """Run all test scenarios and print summary."""
    all_tests = [
        ("FACTUAL", FACTUAL_TESTS),
        ("HOWTO", HOWTO_TESTS),
        ("ARCHITECTURE", ARCHITECTURE_TESTS),
        ("CODE", CODE_TESTS),
        ("COMPLEX", COMPLEX_TESTS),
        ("EDGE_CASE", EDGE_CASE_TESTS),
    ]
    
    results = []
    
    for category, tests in all_tests:
        print(f"\n{'#'*60}")
        print(f"# Running {category} Tests")
        print(f"{'#'*60}")
        
        targets = CATEGORY_TARGETS.get(category, CATEGORY_TARGETS["COMPLEX"])
        
        for test_case in tests:
            result = await execute_query(test_case["query"])
            result.category = category
            results.append((test_case["name"], result, targets))
            print_result(test_case["name"], result, targets)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, r, _ in results if r.success)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    # Category breakdown
    for category, _ in all_tests:
        cat_results = [(n, r, t) for n, r, t in results if r.category == category]
        cat_passed = sum(1 for _, r, _ in cat_results if r.success)
        avg_duration = sum(r.duration_seconds for _, r, _ in cat_results) / len(cat_results) if cat_results else 0
        avg_score = sum(r.verification_score or 0 for _, r, _ in cat_results) / len(cat_results) if cat_results else 0
        
        print(f"\n{category}:")
        print(f"  Pass Rate: {cat_passed}/{len(cat_results)}")
        print(f"  Avg Duration: {avg_duration:.1f}s")
        print(f"  Avg Score: {avg_score:.2f}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_all_tests())
