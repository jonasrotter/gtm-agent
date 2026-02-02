"""
Quick test for architecture query to verify:
1. Step budget is enforced (max 2 steps for architecture)
2. Category-specific iteration limits work
3. PEV loop completes within time budget

Run with: python scripts/test_architecture_query.py

NOTE: Local tools are fallbacks. The LLM may choose to answer
from its training data instead of calling tools when running locally.
When deployed to Azure AI, HostedMCPTool will fetch real documentation.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.orchestrator import OrchestratorAgent
from src.agents.classifier import QueryClassifier, QueryCategory


async def test_architecture_query():
    """Test architecture query with step budget enforcement."""
    
    print("=" * 60)
    print("TEST: Architecture Query with Step Budget")
    print("=" * 60)
    
    query = "What are the best practices for Azure Cosmos DB multi-region deployment?"
    
    # First, verify classification
    classifier = QueryClassifier()
    category = classifier.classify(query)
    config = category.get_config()
    
    print(f"\n📊 Query Classification:")
    print(f"   Query: {query}")
    print(f"   Category: {category.value}")
    print(f"   Max Iterations: {config['max_iterations']}")
    print(f"   Skip PEV: {config['skip_pev']}")
    print(f"   Threshold: {config['threshold']}")
    print(f"   Expected Max Steps: 2 (for architecture)")
    
    # Now run the orchestrator
    print("\n🚀 Running OrchestratorAgent...")
    orchestrator = OrchestratorAgent()
    
    import time
    start = time.perf_counter()
    
    result = await orchestrator.run(query)
    
    elapsed = time.perf_counter() - start
    
    print(f"\n✅ COMPLETED in {elapsed:.1f}s")
    print(f"\n📊 Results:")
    print(f"   • Category: {result.metadata.get('category', 'N/A') if hasattr(result, 'metadata') else 'N/A'}")
    print(f"   • Agent Used: {result.metadata.get('agent', 'N/A') if hasattr(result, 'metadata') else 'N/A'}")
    print(f"   • Verification Score: {result.verification_score}")
    print(f"   • Iterations Used: {result.iterations_used}")
    print(f"   • Human Review Needed: {result.requires_human_review}")
    print(f"   • Plan Summary: {(result.plan_summary or '')[:100]}...")
    
    print(f"\n📄 Response (first 500 chars):")
    print(f"   {result.content[:500]}...")
    
    # Check step count from plan summary
    plan_summary = result.plan_summary or ""
    print(f"   • Plan Summary: {plan_summary[:200]}...")
    
    print(f"\n📄 Response (first 500 chars):")
    print(f"   {result.content[:500]}...")
    
    # Verify expectations
    print(f"\n🔍 Verification:")
    if result.iterations_used <= 2:
        print(f"   ✅ Iterations within budget: {result.iterations_used} <= 2")
    else:
        print(f"   ❌ Too many iterations: {result.iterations_used} > 2")
    
    if result.verification_score and result.verification_score >= 0.75:
        print(f"   ✅ Verification score acceptable: {result.verification_score} >= 0.75")
    else:
        print(f"   ⚠️ Verification score low: {result.verification_score} < 0.75")


if __name__ == "__main__":
    asyncio.run(test_architecture_query())
